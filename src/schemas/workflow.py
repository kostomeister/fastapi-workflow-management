from uuid import uuid4

from pydantic import BaseModel


class WorkflowBase(BaseModel):
    name: str


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    id: int
    file_url: str

    class Config:
        orm_mode = True
