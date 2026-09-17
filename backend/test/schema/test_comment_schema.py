from uuid import uuid4

from schema.comment_schema import comment_schema, comment_update_schema


def test_comment_schema_accepts_valid_payload():
    errors = comment_schema.validate({
        "message": "Looks good",
        "task_id": uuid4(),
        "user_id": uuid4(),
    })

    assert errors == {}


def test_comment_schema_rejects_short_message():
    errors = comment_schema.validate({
        "message": "Ok",
        "task_id": uuid4(),
        "user_id": uuid4(),
    })

    assert "message" in errors


def test_comment_update_schema_accepts_partial_payload():
    errors = comment_update_schema.validate({"message": "Updated comment"})

    assert errors == {}
