
from cerberus import Validator
from backend.utils.exceptions.http_exception import ValidationError
from rest_framework.parsers import JSONParser

def check_rules_with_request_dot_data(rules,data):
    validator = Validator(rules)
    validator.allow_unknown = True
    if validator.validate(data) == False:
        errors=validator.errors
        first_key = list(errors)[0]
        first_error=first_key + ": " + errors[first_key][0]
        raise ValidationError(first_error, errors)
    return data


def validate(rules, request):
    request_body = JSONParser().parse(request)
    if (request_body is None):
        data = {}
    else:
        data = request_body

    validator = Validator(rules)
    validator.allow_unknown = True
    if validator.validate(data) == False:
        errors=validator.errors
        first_key = list(errors)[0]
        first_error=first_key + ": " + errors[first_key][0]
        raise ValidationError(first_error, errors)
    return request_body