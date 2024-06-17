from django.db import models
from backend.utils.datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager, models.Manager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", "Company")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def update_failed_attempt(self, user):
        if user.successive_login_failure_count is None:
            user.successive_login_failure_count = 1
        else:
            user.successive_login_failure_count = user.successive_login_failure_count + 1

        if user.successive_login_failure_count >= 5:
            user.blocked_till = datetime.get_unix_timestamp() + 3600

        user.updated_at = datetime.get_date_time()
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("role", "SuperAdmin")
        extra_fields.setdefault("user_type", "User")
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("status", "Added")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email=email, password=password, **extra_fields)

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Based on the user type, authenticate with different fields

        user_type = "Company"

        if user_type == "User":
            # Authenticate with mobile number
            try:
                user = self.get(email=username)
                return user
            except self.model.DoesNotExist:
                return None

        elif user_type == "Company":
            # Authenticate with email
            try:
                user = self.get(email=username)
                if user and user.check_password(password):
                    return user
            except self.model.DoesNotExist:
                return None

        # If none of the above conditions are met, return None
        return None
