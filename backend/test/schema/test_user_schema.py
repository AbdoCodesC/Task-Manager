from schema.user_schema import user_schema, user_update_schema


def test_user_validation():
    errors = user_schema.validate({
        "first_name": "Abdo",
        "last_name": "Chaibe",
        "email": "user@example.com",
        "password": "Validpassword1!",
    })

    assert errors == {}


def test_user_update_validation():
    errors = user_update_schema.validate({
        "first_name": "Abdo",
        "last_name": "Chaibe",
    })

    assert errors == {}


def test_invalid_email():
    errors = user_schema.validate({
        "first_name": "Abdo",
        "last_name": "Chaibe",
        "email": "invalid-email",
        "password": "Validpassword1!",
    })

    assert "email" in errors


def test_weak_password():
    errors = user_schema.validate({
        "first_name": "Abdo",
        "last_name": "Chaibe",
        "email": "user@example.com",
        "password": "weak",
    })

    assert "password" in errors


def test_short_names():
    errors = user_schema.validate({
        "first_name": "A",
        "last_name": "B",
        "email": "user@example.com",
        "password": "Validpassword1!",
    })

    assert "first_name" in errors
    assert "last_name" in errors