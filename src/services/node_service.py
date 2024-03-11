from src.repositories.node_repository import NodeRepository
from src.schemas.nodes import (
    MessageNode,
    ConditionNode,
    CreateCondition,
    UpdateMessageNode,
    UpdateConditionNode,
)
from src.utils.file_storage import FileStorage


class NodeService:
    def __init__(self, node_repository: NodeRepository, session):
        self.node_repository = node_repository(FileStorage(), session=session)

    async def add_start_node(self, id: int):
        return await self.node_repository.add_start_node(id)

    async def add_message_node(self, workflow_id, node: MessageNode):
        data = node.model_dump()
        return await self.node_repository.add_message_node(workflow_id, **data)

    async def add_condition_node(self, workflow_id, node: ConditionNode):
        data = node.model_dump()
        return await self.node_repository.add_condition_node(workflow_id, **data)

    async def add_yes_node(self, id: int, node: CreateCondition):
        data = node.model_dump()
        return await self.node_repository.add_yes_node(id, data)

    async def add_no_node(self, id: int, node: CreateCondition):
        data = node.model_dump()
        return await self.node_repository.add_no_node(id, data)

    async def add_end_node(self, id: int):
        return await self.node_repository.add_end_node(id)

    async def delete_node(self, workflow_id: int, node_id: int):
        return await self.node_repository.delete_node(workflow_id, node_id)

    async def update_message_node(
        self, workflow_id: int, updated_node_data: UpdateMessageNode
    ):
        data = updated_node_data.dict()
        return await self.node_repository.update_message_node(workflow_id, data)

    async def update_condition_node(
        self, workflow_id: int, updated_node_data: UpdateConditionNode
    ):
        data = updated_node_data.dict()
        return await self.node_repository.update_condition_node(workflow_id, data)
