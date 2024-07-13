from django.db import models
from backend.models.user import CompanyUser


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class CampaignType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_path = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class TargetAudience(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    AGE_GROUP_CHOICES = [
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('55+', '55+'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)

    def __str__(self):
        return f"{self.gender}, {self.age_group}"

class AdCampaign(models.Model):
    budget_type = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("cumulative", "Cumulative")
    ]
    name = models.CharField(max_length=255)
    company = models.ForeignKey(CompanyUser, blank=True, null=True, related_name="company", on_delete=models.SET_NULL)
    campaign_type = models.ForeignKey(CampaignType, on_delete=models.SET_NULL, null=True)
    target_audience = models.ManyToManyField(TargetAudience)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    budget_type = models.CharField(max_length=20, choices=budget_type, default="cumulative")
    currency = models.CharField(max_length=20, default="INR")
    locations = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed')
    ], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Ads(models.Model):
    ad_types = [
        ("Video", "Video"),
        ("Image", "Image"),
    ]
    ad_status = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    media_type = models.CharField(max_length=50, choices=ad_types)
    file_path = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=ad_status, default="draft")
    duration = models.IntegerField(default=None, )
    bid_amount = models.DecimalField(max_digits=2, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.media_type} | {self.status}"
