import io
import uuid

import networkx as nx
import rule_engine
from matplotlib import pyplot as plt

from src.models.workflow import Workflow
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository
from src.utils.file_storage import FileStorage


class WorkflowRepository(SQLAlchemyRepository):
    model = Workflow

    def __init__(self, file_storage: FileStorage, session):
        super().__init__(session)
        self.file_storage = file_storage

    async def create_one(self, data: dict):
        file_path = self._generate_file_path()
        data["file_url"] = file_path
        workflow = await super().create_one(data)
        await self.file_storage.save_workflow_file(file_path, data["name"])
        return workflow

    async def update_one(self, id: int, data: dict):
        workflow = await super().update_one(id, data)
        await self.file_storage.save_workflow_file(workflow[2], workflow[1])
        return {"id": workflow[0], "file_url": workflow[2], "name": workflow[1]}

    async def delete_one(self, id: int):
        file_path = await super().delete_one(id)
        await self.file_storage.delete_workflow_file(file_path)

    async def run_workflow(self, id: int):
        workflow = await super().get_one(id)
        workflow_graph = self.file_storage.read_workflow_file(workflow.file_url)

        node_list = list(workflow_graph.nodes(data=True))

        start_node_exists = any(node.get("type") == "start" for _, node in node_list)

        end_node_exists = any(node.get("type") == "end" for _, node in node_list)

        if not start_node_exists and not end_node_exists:
            raise ValueError("Workflow must have both Start and End nodes")

        start_node = node_list[0]
        next_node = start_node

        previous_message = None

        while next_node:
            print(next_node)
            if next_node[1].get("type") == "message":
                previous_message = next_node[1]

            if next_node[1].get("type") == "condition":
                rule = rule_engine.Rule(next_node[1].get("condition").split("if ")[1])
                if rule.matches({"previous_message": previous_message}):
                    no_node = self._find_by_id(workflow_graph, next_node[1].get("no"))[
                        0
                    ]
                    if no_node:
                        workflow_graph.remove_node(no_node)
                    next_node = self._find_by_id(
                        workflow_graph, next_node[1].get("yes")
                    )
                else:
                    yes_node = self._find_by_id(
                        workflow_graph, next_node[1].get("yes")
                    )[0]
                    if yes_node:
                        workflow_graph.remove_node(yes_node)
                    next_node = self._find_by_id(workflow_graph, next_node[1].get("no"))
            else:
                next_node = self._find_by_id(
                    workflow_graph, next_node[1].get("outgoing_node")
                )

        return self._generate_graph_image(workflow_graph)

    @staticmethod
    def _generate_graph_image(g: nx.DiGraph):
        fig, ax = plt.subplots()
        nx.draw(
            g,
            with_labels=True,
            edge_color=[d.get("color") if d else "b" for _, _, d in g.edges(data=True)],
        )

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)

        return buf.getvalue()

    @staticmethod
    def _find_by_id(workflow_graph, id):
        for node_id, node_data in workflow_graph.nodes(data=True):
            if node_data.get("id") == id:
                return node_id, node_data
        return None

    @staticmethod
    def _generate_file_path() -> str:
        file_id = str(uuid.uuid4())
        return f"workflows/{file_id}.graphml"
