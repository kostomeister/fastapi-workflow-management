from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.node_repository import NodeRepository
from src.repositories.workflow_repository import WorkflowRepository
from src.services.node_service import NodeService
from src.services.workflow_service import WorkflowService
from src.utils.get_session import get_session


def get_workflow_service(session: AsyncSession = Depends(get_session)):
    return WorkflowService(WorkflowRepository, session=session)


def get_node_service(session: AsyncSession = Depends(get_session)):
    return NodeService(NodeRepository, session=session)
