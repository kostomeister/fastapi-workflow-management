from fastapi import APIRouter, Depends
from src.schemas.nodes import CreateCondition, MessageNode, ConditionNode, UpdateMessageNode, UpdateConditionNode
from src.services.node_service import NodeService
from src.utils.dependencies import get_node_service

node_router = APIRouter()


@node_router.post("/workflows/{workflow_id}/nodes/start")
async def add_start_node(
    workflow_id: int, node_service: NodeService = Depends(get_node_service)
):
    return await node_service.add_start_node(workflow_id)


@node_router.post("/workflows/{workflow_id}/nodes/message")
async def add_message_node(
    workflow_id: int,
    node_data: MessageNode,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.add_message_node(workflow_id, node_data)


@node_router.post("/workflows/{workflow_id}/nodes/condition")
async def add_condition_node(
    workflow_id: int,
    node_data: ConditionNode,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.add_condition_node(workflow_id, node_data)


@node_router.post("/workflows/{workflow_id}/nodes/condition/{node_id}/yes")
async def add_yes_node(
    workflow_id: int,
    node_data: CreateCondition,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.add_yes_node(workflow_id, node_data)


@node_router.post("/workflows/{workflow_id}/nodes/condition/{node_id}/no")
async def add_no_node(
    workflow_id: int,
    node_data: CreateCondition,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.add_no_node(workflow_id, node_data)


@node_router.post("/workflows/{workflow_id}/nodes/end")
async def add_end_node(
    workflow_id: int, node_service: NodeService = Depends(get_node_service)
):
    return await node_service.add_end_node(workflow_id)


@node_router.delete("/workflows/{workflow_id}/nodes/{node_id}")
async def delete_node(
    workflow_id: int,
    node_id: int,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.delete_node(workflow_id, node_id)


@node_router.put("/workflows/{workflow_id}/nodes/message/{node_id}")
async def update_message_node(
    workflow_id: int,
    updated_node_data: UpdateMessageNode,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.update_message_node(workflow_id, updated_node_data)


@node_router.put("/workflows/{workflow_id}/nodes/condition/{node_id}")
async def update_condition_node(
    workflow_id: int,
    updated_node_data: UpdateConditionNode,
    node_service: NodeService = Depends(get_node_service),
):
    return await node_service.update_condition_node(workflow_id, updated_node_data)
