from backend.models.user import CompanyUser
from backend.utils.exceptions.http_exception import BadRequestError
from backend.serializers.user import UserSerializer
from backend.utils.auth.jwt import JWTAuth
import json


class UserQuery:
    def __init__(self):
        self.queryset = CompanyUser.objects

    def get_or_fail(self, id=None, email=None, mobile=None):
        if id:
            try:
                return self.queryset.get(id=id)
            except:  # noqa:E722
                raise BadRequestError("User does not exits")
        elif email:
            try:
                return self.queryset.get(email=email)
            except:  # noqa:E722
                raise BadRequestError(f"User with {email} does not exits")
        elif mobile:
            try:
                return self.queryset.get(mobile=mobile)
            except:  # noqa:E722
                raise BadRequestError(f"User with mobile no. {mobile} does not exits")

        raise BadRequestError("unable to find user")

    def __get_or_create_user(self, mobile):
        user, created = self.queryset.get_or_create(mobile=mobile)
        return user

    def generate_new_otp(self, data):
        user_instance = self.__get_or_create_user(mobile=data.get("mobile"))
        if user_instance and user_instance.status != "OtpVerified" and user_instance.user_type != data.get("user_type"):
            raise BadRequestError(
                "This mobile is already registered with another account, please try with another number"
            )
        user_serializer = UserSerializer(instance=user_instance, data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.generate_new_otp()
        user_serializer.save()
        return user_serializer.data

    def verify_otp(self, request, data):
        user_instance = self.get_or_fail(mobile=data.get("mobile"))
        user_serializer = UserSerializer(instance=user_instance, data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.validate_otp(data["otp"])

        # if user_instance.user_type!='User':
        #     return user_instance

        token, user_payload = JWTAuth().generate(user=user_instance)

        if user_instance.user_type != "User":
            request.session["actor"] = json.dumps({**user_payload})
        data = {"session": {"token": token}, "user": {**user_payload}}
        return data

    def get_user_details(self, data):
        if isinstance(data, dict):
            if data.get("user_id"):
                user_instance = self.get_or_fail(id=data.get("user_id"))
            elif data.get("email"):
                user_instance = self.get_or_fail(email=data.get("email"))
            else:
                user_instance = self.get_or_fail(mobile=data.get("mobile"))
        else:
            user_instance = data
        data = {
            "id": user_instance.id,
            "name": user_instance.name,
            "email": user_instance.email,
            "profile_pic": user_instance.profile_pic,
            "is_superuser": user_instance.is_superuser,
            "user_type": user_instance.user_type,
            "status": user_instance.status,
            "mobile": user_instance.mobile,
        }
        return data

    def get_user_details_with_token(self, user):
        token, user_payload = JWTAuth().generate(user)
        return {"session": {"token": token}, "user": {**user_payload}}

    def update_user_details(self, request, data):
        if request.actor.get("id") != data.get("user_id"):
            raise BadRequestError("You don't permission to update the details")

        user_instance = self.get_or_fail(id=data.pop("user_id"))
        user_serializer = UserSerializer(instance=user_instance, data=data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return user_serializer.data

    def register_user(self, data):
        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        validated_data = user_serializer.validated_data
        email = user_serializer.validated_data.pop("email")
        password = user_serializer.validated_data.pop("password")
        user = self.queryset.create_user(email, password, **validated_data)
        return user
