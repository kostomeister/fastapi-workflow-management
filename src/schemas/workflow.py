from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):
    name: str


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    id: int
    file_url: str

    model_config = ConfigDict(from_attributes=True)
