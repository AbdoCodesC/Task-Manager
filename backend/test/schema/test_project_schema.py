from uuid import uuid4

from schema.project_schema import project_schema, project_update_schema


def test_project_schema_accepts_valid_payload():
    errors = project_schema.validate({
        "name": "Website",
        "description": "Marketing website",
        "status": "todo",
    })

    assert errors == {}


def test_project_schema_rejects_short_name():
    errors = project_schema.validate({
        "name": "A",
        "description": None,
        "status": "todo",
    })

    assert "name" in errors


def test_project_update_schema_accepts_partial_payload():
    errors = project_update_schema.validate({"description": "Updated description"})

    assert errors == {}
