import pytest
from sqlalchemy.ext.asyncio import AsyncSession


async def test_create_workflow(ac: AsyncSession):
    workflow_data = {"name": "Test Workflow"}

    response = await ac.post("/workflows", json=workflow_data)

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Workflow"


async def test_get_all_workflows(ac):
    response = await ac.get("/workflows")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


async def test_get_workflow(ac):
    workflow_data = {"name": "Test Workflow"}

    await ac.post("/workflows", json=workflow_data)

    workflow_id = 1
    response = await ac.get(f"/workflows/{workflow_id}")

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == workflow_id


async def test_update_workflow(ac):
    workflow_id = 1
    updated_data = {"name": "Updated Workflow"}

    response = await ac.put(f"/workflows/{workflow_id}", json=updated_data)

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == workflow_id
    assert response.json()["name"] == "Updated Workflow"


async def test_add_start_node_to_workflow(ac):
    workflow_id = 1

    response = await ac.post(f"/workflows/{workflow_id}/nodes/start")

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["type"] == "start"

    response = await ac.post(f"/workflows/{workflow_id}/nodes/start")
    assert response.status_code == 404


async def test_add_message_node_to_workflow(ac):
    workflow_id = 1
    message_data = {
        "message": "Test Message",
        "status": "Test Status",
        "outgoing_node_ids": [0],
    }

    response = await ac.post(
        f"/workflows/{workflow_id}/nodes/message", json=message_data
    )
    print(response.content)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["type"] == "message"
    assert response.json()["message"] == "Test Message"
    assert response.json()["status"] == "Test Status"


async def test_add_condition_node_to_workflow(ac):
    workflow_id = 1
    node_data = {
        "condition": "Test Condition",
        "outgoing_node_ids": [1],
    }

    response = await ac.post(
        f"/workflows/{workflow_id}/nodes/condition", json=node_data
    )
    print(response.json())
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["condition"] == "Test Condition"


async def test_add_end_node_to_workflow(ac):
    workflow_id = 1

    response = await ac.post(f"/workflows/{workflow_id}/nodes/end")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["type"] == "end"

    response = await ac.post(f"/workflows/{workflow_id}/nodes/end")
    assert response.status_code == 404


async def test_delete_workflow(ac):
    workflow_id = 1

    response = await ac.delete(f"/workflows/{workflow_id}")

    assert response.status_code == 200
