from rest_framework.views import exception_handler
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response
import traceback, json
from backend.queries.api_call_log import ApiCallLogQuery
from backend.enums.base_enum import CustomMessage
import email

"""Return Response

Custom exception handler for modifying error response
"""


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if hasattr(context["request"], "_body_copy"):
            request_body = context["request"]._body_copy
            request_body = convert_request_body_to_json(request_body)
        else:
            request_body = {}
        try:
            path = context["request"].path
        except:
            path = None

        if request_body and not isinstance(request_body, str) and request_body.get("aadhaar_number"):
            request_body["aadhaar_number"] = "xxxxxxxx" + request_body.get("aadhaar_number")[-4::1]

        if request_body and not isinstance(request_body, str) and request_body.get("aadhaar_number"):
            request_body["aadhaar_number"] = "xxxxxxxx" + request_body.get("aadhaar_number")[-4::1]

        log_data = {
            "request_body": json.dumps(request_body) if request_body else {},
            "result_status_code": 404,
            "endpoint": path,
        }
        ApiCallLogQuery().create(log_type="error", data=log_data)
        if isinstance(exc.detail, str):
            if "ErrorDetail" in exc.detail.__str__():
                msg = str(exc.detail).split("=")[1].split(",")[0].replace("'", "")
                response.data = {"msg": msg or ""}
            else:
                response.data = {"msg": exc.detail or ""}
        elif isinstance(exc.detail, ReturnDict):
            first_key = list(exc.detail)[0]
            first_error = first_key + ": " + exc.detail[first_key][0]
            response.data = {"msg": exc.detail[first_key][0], "errors": first_error}
        else:
            response.data = {"msg": "Errors", "errors": exc.detail}

        if hasattr(exc, "errors"):
            response.data["errors"] = exc.errors
    else:
        error_code = 500
        msg = CustomMessage.ExceptionMessage
        custom_data = {"msg": msg, "status_code": error_code}
        error_log_data = {"msg": msg, "status_code": error_code}

        # Capture traceback information
        exc_traceback = traceback.format_exception(type(exc), exc, exc.__traceback__)
        error_log_data["traceback"] = exc_traceback

        if hasattr(exc, "detail"):
            if isinstance(exc.detail, str):
                error_log_data["error_message"] = exc.detail
            elif isinstance(exc.detail, dict):
                first_key = list(exc.detail)[0]
                error_log_data["error_message"] = str(exc.detail[first_key][0])
            elif isinstance(exc.detail, (list, ReturnDict)):
                error_log_data["error_message"] = str(exc.detail)
        else:
            error_log_data["error_message"] = str(exc)

        view_function = context.get("view", None)
        if view_function:
            if hasattr(view_function, "__name__"):
                # Regular function-based view
                error_log_data["error_view"] = f"{view_function.__module__}.{view_function.__name__}"
            elif hasattr(view_function, "__class__"):
                # Class-based view
                error_log_data["error_view"] = (
                    f"{view_function.__class__.__module__}.{view_function.__class__.__name__}"
                )

        # Log the request body if available
        if hasattr(context["request"], "actor"):
            user_details = context["request"].actor
        else:
            user_details = {}

        if hasattr(context["request"], "_body_copy"):
            request_body = context["request"]._body_copy
        else:
            request_body = {}

        if request_body:
            request_body = convert_request_body_to_json(request_body)

        log_data = {
            "api_type": "Method - " + error_log_data["error_view"],
            "request_body": json.dumps(request_body) if request_body else {},
            "method": str(error_log_data["traceback"]),
            "endpoint": context["request"].path,
            "response": error_log_data["error_message"],
            "result_status_code": 500,
        }
        connector_msg = {
            "request_body": json.dumps(request_body) if request_body else {},
            "method": str(error_log_data["traceback"]),
            "endpoint": context["request"].path,
            "response": error_log_data["error_message"],
        }
        # update_team_on_teams = threading.Thread(target=send_message_on_teams,args=(connector_msg,))
        ApiCallLogQuery().create(log_type="error", data=log_data)
        # update_team_on_teams.start()
        response = Response(custom_data, status=error_code)
    return response


def send_message_on_teams(connector_msg):
    pass
    # ConnectorCard = TeamsConnectorCard()
    # connector_msg = json.dumps(connector_msg, default=lambda x: x.decode('utf-8') if isinstance(x, bytes) else x, ensure_ascii=False, indent=2)
    # ConnectorCard.msg_structure(json_payload=connector_msg,title=settings.INTERNAL_SERVER_ERROR)
    # ConnectorCard.send()


def convert_request_body_to_json(request_body):
    if request_body and isinstance(request_body, bytes):
        try:
            data = request_body.decode("utf-8")
            try:
                request_body = json.loads(data)
            except:
                data = email.message_from_string(data)
                request_body = {}
                for part in data.walk():
                    if part.get_content_maintype() == "multipart":
                        continue
                    content_disposition = part.get("Content-Disposition")
                    if content_disposition and "form-data" in content_disposition:
                        name = part.get_param("name", header="content-disposition")
                        value = part.get_payload(decode=True).decode("utf-8")
                        request_body[name] = value
        except:
            request_body = {}

    if request_body and isinstance(request_body, dict):
        if request_body.get("aadhaar_number"):
            request_body["aadhaar_number"] = "xxxxxxxx" + request_body.get("aadhaar_number")[-4::1]

        if request_body.get("password"):
            request_body["password"] = "user_password"

    return request_body
