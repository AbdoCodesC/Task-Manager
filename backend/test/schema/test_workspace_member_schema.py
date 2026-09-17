from uuid import uuid4

from schema.workspace_member_schema import workspace_member_schema, workspace_member_update_schema


def test_workspace_member_schema_accepts_valid_payload():
    errors = workspace_member_schema.validate({
        "role": "member",
        "user_id": uuid4(),
        "workspace_id": uuid4(),
    })

    assert errors == {}


def test_workspace_member_schema_rejects_invalid_role():
    errors = workspace_member_schema.validate({
        "role": "superuser",
        "user_id": uuid4(),
        "workspace_id": uuid4(),
    })

    assert "role" in errors


def test_workspace_member_update_schema_accepts_partial_payload():
    errors = workspace_member_update_schema.validate({"role": "admin"})

    assert errors == {}
