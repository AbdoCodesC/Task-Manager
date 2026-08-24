from marshmallow import ValidationError
from backend.schema import user_schema

try:
    result = user_schema.load({"id": 1, "email": "foo"})
except ValidationError as err:
    print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
    print(err.valid_data)  # => {"name": "John"}