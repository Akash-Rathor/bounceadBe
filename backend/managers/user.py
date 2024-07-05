from django.db import models
from backend.utils.datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager, models.Manager):

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

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        print("called custom create_superuser")
        extra_fields.setdefault("role", "SuperAdmin")
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", "Added")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def authenticate(self, username=None, password=None, **kwargs):
        # Based on the user type, authenticate with different fields
        if len(username) == 10 and "@" not in str(username):
            try:
                user = self.get(mobile=username)
                if user and user.check_password(password):
                    return user
                return user
            except self.model.DoesNotExist:
                return None

        else:
            # Authenticate with email
            try:
                user = self.get(email=username)
                if user and user.check_password(password):
                    return user
            except self.model.DoesNotExist:
                return None

        # If none of the above conditions are met, return None
        return None

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("status", "Added")
        extra_fields.setdefault("user_type", "Company")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
