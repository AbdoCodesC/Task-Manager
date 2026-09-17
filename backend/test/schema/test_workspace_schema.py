from uuid import uuid4

from schema.workspace_schema import workspace_schema, workspace_update_schema


def test_workspace_schema_accepts_valid_payload():
    errors = workspace_schema.validate({
        "name": "Engineering",
        "slug": "engineering",
        "owner_id": uuid4(),
    })

    assert errors == {}


def test_workspace_schema_rejects_short_slug():
    errors = workspace_schema.validate({
        "name": "Engineering",
        "slug": "x",
        "owner_id": uuid4(),
    })

    assert "slug" in errors


def test_workspace_update_schema_accepts_partial_payload():
    errors = workspace_update_schema.validate({"name": "Product"})

    assert errors == {}
