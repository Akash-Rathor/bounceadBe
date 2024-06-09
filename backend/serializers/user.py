# from backend.mails.new_signup import NewSignUpMail
from rest_framework import serializers
from backend.models.user import User
from django.contrib.auth.hashers import make_password
import random, os
from backend.utils.datetime import datetime
from backend.utils.exceptions.http_exception import BadRequestError
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "otp": {"write_only": True},
            "otp_generated_at": {"write_only": True},
            "otp_valid_till": {"write_only": True},
            "blocked_till": {"write_only": True},
            "successive_login_failure_count": {"write_only": True},
            "email": {"required": False},
        }

    def generate_new_otp(self):
        user = self.instance
        if os.getenv("GENERATE_RANDOM_OTP") == "1":
            user.otp = random.randint(99999, 999999)
        user.otp = 123456
        user.otp_generated_at = datetime.get_unix_timestamp()
        print("OTP", user.otp)
        user.otp_valid_till = datetime.get_unix_timestamp() + settings.OTP_VALIDITY
        user.save()
        return user

    def validate_otp(self, otp):
        # def validate_otp(self,request,otp):
        user = self.instance

        otp = int(otp)

        if not user.otp or not user.otp_generated_at:
            raise BadRequestError("OTP has not been generated for this user.")

        if datetime.get_unix_timestamp() > user.otp_valid_till:
            raise BadRequestError("OTP has expired.")

        if otp != user.otp:
            if user.successive_login_failure_count is None:
                user.successive_login_failure_count = 0

            user.successive_login_failure_count += 1

            if user.successive_login_failure_count > 5:
                user.blocked_till = datetime.get_unix_timestamp() + settings.BLOCKED_TIMER
                user.save()
                raise BadRequestError("Too May Wrong OTPs! Blocked till ")

            user.save()
            raise BadRequestError("Invalid OTP.")

        else:
            user.successive_login_failure_count = 0
            user.blocked_till = None
            user.last_login = datetime.get_date_time()
            user.status = "Active"
            user.save()
            return user
