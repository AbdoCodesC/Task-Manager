from uuid import uuid4

from schema.task_activity_schema import task_activity_schema, task_activity_update_schema


def test_task_activity_schema_accepts_valid_payload():
    errors = task_activity_schema.validate({
        "task_id": uuid4(),
        "user_id": uuid4(),
        "activity_type": "status_changed",
        "field_name": "status",
        "old_value": "todo",
        "new_value": "done",
        "details": {"source": "test"},
    })

    assert errors == {}


def test_task_activity_schema_rejects_invalid_activity_type():
    errors = task_activity_schema.validate({
        "task_id": uuid4(),
        "user_id": uuid4(),
        "activity_type": "unknown",
    })

    assert "activity_type" in errors


def test_task_activity_update_schema_accepts_partial_payload():
    errors = task_activity_update_schema.validate({"details": {"source": "test"}})

    assert errors == {}
