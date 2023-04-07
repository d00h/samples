from typing import Any

import yaml

raw_schema = """
ResponsePayonlineAuthFailProfileNotFound:
    description: "Payment profile not found"
    type: object
    properties:
      success:
        type: boolean
        example: false
      code:
        type: string
        example: "PAYMENT_PROFILE_NOT_FOUND"
      message:
        type: string
        example: "Не найден платежный профиль при заданных параметрах"
      status_code:
        type: integer
        example: 400
      data:
        type: object
        properties:
          currency:
            type: string
            example: "USD"
"""


def check_object_shema(obj: Any, schema: dict, schema_path: str):
    schema_one_of = schema.get("oneOf")
    if schema_one_of is not None:
        for child_schema in schema_one_of:
            try:
                check_object_shema(obj, check_object_shema, schema_path)
                return
            except AssertionError:
                continue
        raise AssertionError(f"{schema_path} not found oneof")
    else:
        schema_type = schema.get("type")
        assert schema_type is not None, f"{schema_path} schema not defined"
        if schema_type == "object":
            assert isinstance(obj, dict), f"{schema_path} is not object({obj}: {type(obj)}"
            schema_obj_properties = schema.get("properties") or {}
            fields = set([*schema_obj_properties.keys(), *obj.keys()])
            assert len(fields) > 0, f"{schema_path} has not fields?"
            for field in fields:
                assert field in obj, f"{schema_path} response has no {field}"
                assert field in schema_obj_properties, f"{schema_path} schema has no {field}"
                check_object_shema(obj[field], schema_obj_properties[field], f"{schema_path}.{field}")
        elif schema_type == "string":
            assert isinstance(obj, str), f"{schema_path} response is not str"
        elif schema_type == "boolean":
            assert isinstance(obj, bool), f"{schema_path} response is not bool"
        elif schema_type == "integer":
            assert isinstance(obj, int), f"{schema_path} response is not int"
        else:
            NotImplementedError(schema_type)


obj_schema = yaml.load(raw_schema, yaml.SafeLoader)
obj = {
    "success": True,
    "code": "SOME_CODE",
    "message": "Some messages",
    "status_code": 1223,
    "data": {"currency": "ru" }
}

check_object_shema(
    obj,
    obj_schema["ResponsePayonlineAuthFailProfileNotFound"],
    "payonline_auth.response.200"
)
