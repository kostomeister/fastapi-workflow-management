from fastapi import Response

from src.repositories.workflow_repository import WorkflowRepository, FileStorage
from src.schemas.workflow import WorkflowUpdate


class WorkflowService:
    def __init__(self, workflow_repository: WorkflowRepository, session):
        self.workflow_repository = workflow_repository(FileStorage(), session=session)

    async def create_workflow(self, WorkflowCreate):
        data = WorkflowCreate.model_dump()
        return await self.workflow_repository.create_one(data)

    async def update_workflow(self, workflow_id: int, data: WorkflowUpdate):
        data = data.model_dump()
        return await self.workflow_repository.update_one(workflow_id, data)

    async def delete_workflow(self, workflow_id: int):
        return await self.workflow_repository.delete_one(workflow_id)

    async def get_workflow(self, workflow_id: int):
        return await self.workflow_repository.get_one(workflow_id)

    async def get_all_workflows(self):
        return await self.workflow_repository.get_all()

    async def run_workflow(self, workflow_id: int):
        content = await self.workflow_repository.run_workflow(workflow_id)
        return Response(content=content, media_type="image/png")
