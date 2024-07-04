from rest_framework.decorators import api_view
from backend.utils import validator
from backend.utils import response
from backend.queries.user import UserQuery
from backend.utils.auth.jwt import JWTAuth


@api_view(["POST"])
def register_view(request):

    if request.method == "POST":
        schema = {
            "mobile": {"type": "integer"},
            "user_type": {"type": "string", "required": True},
            "password": {"type": "string", "required": True},
            "name": {"type": "string", "required": False},
            "email": {"type": "string"},
        }
        rules = {"one_off": ("email", "mobile")}
        request_data = validator.validate(schema, request, rules)
        user = UserQuery().register_user(request_data)
        return response.respond_201(UserQuery().get_user_details_with_token(user))
