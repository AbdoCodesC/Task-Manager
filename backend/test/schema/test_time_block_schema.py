from datetime import datetime, timezone
from uuid import uuid4

from schema.time_block_schema import time_block_schema, time_block_update_schema


def test_time_block_schema_accepts_valid_payload():
    errors = time_block_schema.validate({
        "title": "Focus session",
        "start_time": datetime(2026, 9, 16, 9, 0, tzinfo=timezone.utc),
        "end_time": datetime(2026, 9, 16, 10, 0, tzinfo=timezone.utc),
        "task_id": uuid4(),
    })

    assert errors == {}


def test_time_block_schema_rejects_missing_task_id():
    errors = time_block_schema.validate({"title": "Focus session"})

    assert "task_id" in errors


def test_time_block_update_schema_accepts_partial_payload():
    errors = time_block_update_schema.validate({"title": "Updated session"})

    assert errors == {}
