from django.db import models

# Create your models here.
from django.db import models
from backend.managers.user import UserManager

from django.contrib.auth.models import AbstractBaseUser

"""User model"""

user_active_status = [
    ("Active", "Active"),
    ("OtpInitialized", "OtpInitialized"),
    ("Deactivated", "Deactivated"),
    ("Paused", "Paused"),
    ("Deleted", "Deleted"),
    ("OtpVerified", "OtpVerified"),
]


class User(AbstractBaseUser):
    objects = UserManager()

    name = models.CharField(max_length=100, null=True, db_index=True)
    email = models.CharField(max_length=100, blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    user_type = models.CharField(max_length=20, choices=[("Company", "Company")], default="Company")
    status = models.CharField(max_length=20, choices=user_active_status, default="OtpInitialized")
    device_token = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_generated_at = models.PositiveBigIntegerField(blank=True, null=True)
    otp_valid_till = models.PositiveBigIntegerField(blank=True, null=True)
    blocked_till = models.PositiveBigIntegerField(blank=True, null=True)
    successive_login_failure_count = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    profile_pic = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user_type} | {self.name} | {self.mobile} | {self.email}"

    @property
    def is_authenticated(self):
        return True if self.id else False
