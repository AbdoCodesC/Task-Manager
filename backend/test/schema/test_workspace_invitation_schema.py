from datetime import datetime, timedelta, timezone
from uuid import uuid4

from schema.workspace_invitation_schema import workspace_invitation_schema, workspace_invitation_update_schema


def test_workspace_invitation_schema_accepts_valid_payload():
    errors = workspace_invitation_schema.validate({
        "email": "member@example.com",
        "role": "member",
        "status": "pending",
        "token": uuid4(),
        "workspace_id": uuid4(),
        "invited_by_id": uuid4(),
    })

    assert errors == {}


def test_workspace_invitation_schema_rejects_invalid_email():
    errors = workspace_invitation_schema.validate({
        "email": "not-an-email",
        "role": "member",
        "status": "pending",
        "token": uuid4(),
        "workspace_id": uuid4(),
        "invited_by_id": uuid4(),
    })

    assert "email" in errors


def test_workspace_invitation_update_schema_accepts_partial_payload():
    errors = workspace_invitation_update_schema.validate({"status": "cancelled"})

    assert errors == {}
