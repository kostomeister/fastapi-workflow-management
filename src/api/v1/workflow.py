from fastapi import APIRouter, Depends

from src.schemas.workflow import WorkflowCreate, WorkflowUpdate
from src.services.workflow_service import WorkflowService
from src.utils.dependencies import get_workflow_service

workflow_router = APIRouter()


@workflow_router.post("/workflows")
async def get_workflows(
    workflow: WorkflowCreate,
    workflow_service: WorkflowService = Depends(get_workflow_service),
):
    return await workflow_service.create_workflow(workflow)


@workflow_router.get("/workflows")
async def get_workflows(
    workflow_service: WorkflowService = Depends(get_workflow_service),
):
    return await workflow_service.get_all_workflows()


@workflow_router.get("/workflows/{workflow_id}")
async def get_workflow(
    workflow_id: int, workflow_service: WorkflowService = Depends(get_workflow_service)
):
    return await workflow_service.get_workflow(workflow_id)


@workflow_router.put("/workflows/{workflow_id}")
async def update_workflow(
    workflow_id: int,
    workflow: WorkflowUpdate,
    workflow_service: WorkflowService = Depends(get_workflow_service),
):
    return await workflow_service.update_workflow(workflow_id, workflow)


@workflow_router.delete("/workflows/{workflow_id}")
async def delete_workflow(
    workflow_id: int, workflow_service: WorkflowService = Depends(get_workflow_service)
):
    return await workflow_service.delete_workflow(workflow_id)


@workflow_router.get("/workflows/{workflow_id}/run")
async def run_workflow(
    workflow_id: int, workflow_service: WorkflowService = Depends(get_workflow_service)
):
    return await workflow_service.run_workflow(workflow_id)
