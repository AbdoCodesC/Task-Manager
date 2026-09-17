from schema.task_schema import task_schema, task_update_schema


def test_task_schema_accepts_valid_payload():
    errors = task_schema.validate({
        "title": "Implement login",
        "description": "Add cookie-based authentication",
        "priority": "high",
        "status": "todo",
    })

    assert errors == {}


def test_task_schema_rejects_invalid_priority():
    errors = task_schema.validate({
        "title": "Implement login",
        "description": None,
        "priority": "critical",
        "status": "todo",
    })

    assert "priority" in errors


def test_task_schema_rejects_long_description():
    errors = task_schema.validate({
        "title": "Implement login",
        "description": "x" * 1001,
        "priority": "medium",
        "status": "todo",
    })

    assert "description" in errors


def test_task_update_schema_accepts_partial_payload():
    errors = task_update_schema.validate({"status": "done"})

    assert errors == {}
