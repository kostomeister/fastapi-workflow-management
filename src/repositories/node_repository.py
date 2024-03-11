from src.models.workflow import Workflow
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository
from src.utils.edge_validator import EdgeValidator
from src.utils.file_storage import FileStorage
from src.utils.nodes import StartNode, MessageNode, ConditionNode, EndNode
from src.utils.validators import async_value_error_handler, sync_value_error_handler


class NodeRepository(SQLAlchemyRepository):
    model = Workflow

    def __init__(self, file_storage: FileStorage, session):
        super().__init__(session)
        self.file_storage = file_storage

    @async_value_error_handler()
    async def add_start_node(self, id: int):
        workflow = await super().get_one(id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))
        start_node_exists = any(
            node.get("type") == "start" for _, node in workflow_graph.nodes(data=True)
        )
        if not start_node_exists:
            start_node_id = len(node_list)
            start = StartNode(start_node_id)
            workflow_graph.add_node(start, **start.__dict__)
            await self.file_storage.save_workflow_file(
                workflow.file_url, workflow_graph.name, workflow_graph
            )
        else:
            raise ValueError("Start node already exists in the workflow graph.")
        await self.file_storage.save_workflow_file(
            workflow.file_url, workflow_graph.name, workflow_graph
        )
        return start

    @async_value_error_handler()
    async def add_message_node(
        self,
        id: int,
        message: str,
        status: str,
        outgoing_node_ids: list[int],
        decision: str = None,
    ):
        workflow = await super().get_one(id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))

        message_node_id = node_list[-1][1].get("id") + 1
        message_node = MessageNode(message_node_id, status, message)

        updated_workflow_graph = self._add_edge(
            workflow_graph, message_node, outgoing_node_ids, decision
        )

        await self.file_storage.save_workflow_file(
            workflow.file_url, workflow_graph.name, updated_workflow_graph
        )

        return message_node

    @async_value_error_handler()
    async def add_condition_node(
        self,
        id: int,
        condition: str,
        outgoing_node_ids: list[int],
        decision: str = None,
    ):
        workflow = await super().get_one(id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))

        condition_node_id = node_list[-1][1].get("id") + 1
        condition_node = ConditionNode(condition_node_id, condition)

        updated_workflow_graph = self._add_edge(
            workflow_graph, condition_node, outgoing_node_ids, decision
        )

        await self.file_storage.save_workflow_file(
            workflow.file_url, workflow_graph.name, updated_workflow_graph
        )

        return condition_node

    @async_value_error_handler()
    async def add_yes_node(self, id: int, data: dict):
        decision = "yes"

        outgoing_node_id = [data.pop("outgoing_node_id")]

        node_type = data.pop("type")

        node = None

        if node_type == "message":
            message = data.pop("message")
            status = data.pop("status")
            node = await self.add_message_node(
                id, message, status, outgoing_node_id, decision
            )

        if node_type == "condition":
            condition = data.pop("condition")
            node = await self.add_condition_node(
                id, condition, outgoing_node_id, decision
            )

        return node

    @async_value_error_handler()
    async def add_no_node(self, id: int, data: dict):
        decision = "no"

        outgoing_node_id = [data.pop("outgoing_node_id")]

        node_type = data.pop("type")

        node = None

        if node_type == "message":
            message = data.pop("message")
            status = data.pop("status")
            node = await self.add_message_node(
                id, message, status, outgoing_node_id, decision
            )

        if node_type == "condition":
            condition = data.pop("condition")
            node = await self.add_condition_node(
                id, condition, outgoing_node_id, decision
            )

        return node

    @async_value_error_handler()
    async def add_end_node(self, id: int):
        workflow = await super().get_one(id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))

        end_node_exists = any(node.get("type") == "end" for _, node in node_list)

        if end_node_exists:
            raise ValueError("End not already exists")

        message_nodes_without_outgoing = [
            (node_id, node_data)
            for node_id, node_data in node_list
            if node_data.get("type") == "message" and "outgoing_node" not in node_data
        ]

        end_node_id = node_list[-1][1].get("id") + 1
        end_node = EndNode(end_node_id)
        workflow_graph.add_node(end_node, **end_node.__dict__)

        for message_node_id, message_node_data in message_nodes_without_outgoing:
            EdgeValidator.add_edge(
                (message_node_id, message_node_data), end_node.__dict__, workflow_graph
            )
            workflow_graph.add_edge(message_node_id, end_node)

        await self.file_storage.save_workflow_file(
            workflow.file_url, workflow_graph.name, workflow_graph
        )

        return end_node

    @async_value_error_handler()
    async def delete_node(self, workflow_id: int, node_id: int):
        workflow = await super().get_one(workflow_id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))

        node_to_delete = None
        for node, data in node_list:
            if data.get("id") == node_id:
                node_to_delete = node
                break

        if node_to_delete is not None:
            for incoming_node in workflow_graph.predecessors(node_to_delete):
                incoming_node_data = workflow_graph.nodes[incoming_node]
                if "outgoing_node" in incoming_node_data:
                    del incoming_node_data["outgoing_node"]
                elif (
                    "yes" in incoming_node_data and incoming_node_data["yes"] == node_id
                ):
                    del incoming_node_data["yes"]
                elif "no" in incoming_node_data and incoming_node_data["no"] == node_id:
                    del incoming_node_data["no"]

            workflow_graph.remove_node(node_to_delete)

            await self.file_storage.save_workflow_file(
                workflow.file_url, workflow_graph.name, workflow_graph
            )
        else:
            raise ValueError("Node with the specified ID does not exist.")

    @async_value_error_handler()
    async def update_message_node(self, workflow_id: int, updated_node_data: dict):
        workflow = await super().get_one(workflow_id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))

        for node, data in node_list:
            if (
                data.get("id") == updated_node_data["id"]
                and data.get("type") == "message"
            ):
                data["message"] = updated_node_data["message"]
                data["status"] = updated_node_data["status"]
                await self.file_storage.save_workflow_file(
                    workflow.file_url, workflow_graph.name, workflow_graph
                )
                return data
        raise ValueError(
            "Message node with the specified ID not found in the workflow."
        )

    @async_value_error_handler()
    async def update_condition_node(self, workflow_id: int, updated_node_data: dict):
        workflow = await super().get_one(workflow_id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)
        node_list = list(workflow_graph.nodes(data=True))

        for node, data in node_list:
            if (
                data.get("id") == updated_node_data["id"]
                and data.get("type") == "condition"
            ):
                data["condition"] = updated_node_data["condition"]
                await self.file_storage.save_workflow_file(
                    workflow.file_url, workflow_graph.name, workflow_graph
                )
                return data
        raise ValueError(
            "Condition node with the specified ID not found in the workflow."
        )

    @staticmethod
    @sync_value_error_handler
    def _add_edge(workflow_graph, node, outgoing_node_ids, decision: str = None):
        node_data = node.__dict__

        for outgoing_node_id in outgoing_node_ids:
            outgoing_node = None

            for out_node_id, out_node_data in workflow_graph.nodes(data=True):
                if out_node_data.get("id") == outgoing_node_id:
                    outgoing_node = out_node_id, out_node_data
                    break

            if outgoing_node:
                EdgeValidator.add_edge(
                    outgoing_node, node_data, workflow_graph, decision
                )

                if decision == "yes":
                    outgoing_node[1]["yes"] = node_data["id"]
                elif decision == "no":
                    outgoing_node[1]["no"] = node_data["id"]
                else:
                    outgoing_node[1]["outgoing_node"] = node_data["id"]

                workflow_graph.add_node(node, **node_data)
                workflow_graph.add_edge(outgoing_node[0], node)
            else:
                raise ValueError(f"Outgoing node with ID {outgoing_node_id} not found.")

        return workflow_graph
