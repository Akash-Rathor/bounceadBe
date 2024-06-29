from django.db import models

# Create your models here.
from time import timezone
from django.db import models
from backend.managers.user import UserManager
from django_mysql.models import EnumField
# from backend.utils.fields import DateTimeWithoutTZField
from django.contrib.auth.models import AbstractBaseUser,AbstractUser

"""User model"""

user_active_status = [
    ('Active','Active'),
    ('OtpInitialized','OtpInitialized'),
    ('Deactivated','Deactivated'),
    ('Paused','Paused'),
    ('Deleted','Deleted'),
    ('OtpVerified','OtpVerified'),
]
class User(AbstractBaseUser): #company
    REQUIRED_FIELDS = ('mobile')
    USERNAME_FIELD = 'mobile'
    
    objects = UserManager()
    
    name = models.CharField(max_length=100,null=True,db_index=True)
    email = models.CharField(max_length=100, blank=True, null=True,unique=True)
    mobile = models.CharField(max_length=10,unique=True)
    # user_type = models.CharField(max_length=20,choices=[('Company','Company')],default='User')
    status = models.CharField(max_length=20,choices=user_active_status,default='OtpInitialized')
    password = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    successive_login_failure_count = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    profile_pic = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        unique_together = [('mobile','email')]