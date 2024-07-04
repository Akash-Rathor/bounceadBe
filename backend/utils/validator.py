from cerberus import Validator
from backend.utils.exceptions.http_exception import ValidationError
from rest_framework.parsers import JSONParser


def check_rules_with_request_dot_data(rules, data):
    validator = Validator(rules)
    validator.allow_unknown = True
    if validator.validate(data) == False:
        errors = validator.errors
        first_key = list(errors)[0]
        first_error = first_key + ": " + errors[first_key][0]
        raise ValidationError(first_error, errors)
    return data


def validate(schema, request, rules=None):
    request_body = JSONParser().parse(request)
    if request_body is None:
        data = {}
    else:
        data = request_body
    if rules and "one_of" in rules:
        one_of_fields = rules["one_of"]
        if not any(field in data for field in one_of_fields):
            raise ValidationError(f"At least one of {one_of_fields} must be present.")
    validator = Validator(schema)
    validator.allow_unknown = True
    if validator.validate(data) == False:
        errors = validator.errors
        first_key = list(errors)[0]
        first_error = first_key + ": " + errors[first_key][0]
        raise ValidationError(first_error, errors)
    return request_body
