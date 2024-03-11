from typing import Optional
from pydantic import BaseModel


class CreateCondition(BaseModel):
    type: str
    message: Optional[str] = None
    status: Optional[str] = None
    condition: Optional[str] = None
    outgoing_node_id: int


class MessageNode(BaseModel):
    message: str
    status: str
    outgoing_node_ids: list[int]


class ConditionNode(BaseModel):
    condition: str
    outgoing_node_ids: list[int]


class UpdateMessageNode(BaseModel):
    id: int
    message: str
    status: str


class UpdateConditionNode(BaseModel):
    id: int
    condition: str
