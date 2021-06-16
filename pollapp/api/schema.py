

GET_RESULT_JSON_SCHEMA: dict = {
    "type": "object",
    "properties": {
            "poll_id": {"type": "string", "format": "uuid"},
    },
    "required": ["poll_id"],
    "additionalProperties": False
}


POLL_JSON_SCHEMA: dict = {
    "type": "object",
    "properties": {
            "poll_id": {"type": "string", "format": "uuid"},
            "choice": {"type": "string"},
    },
    "required": ["poll_id", "choice"],
    "additionalProperties": False
}

CREATE_POLL_JSON_SCHEMA: dict = {
    "type": "object",
    "properties": {
            "name": {"type": "string", "minLength": 1},
            "answers": {"type": "array", "items": {
                "type": "string"
            }, "minItems": 1},
    },
    "required": ["name", "answers"],
    "additionalProperties": False
}
