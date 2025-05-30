# Generated by Django 4.2.11 on 2024-07-04 00:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CompanyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100, null=True)),
                (
                    "email",
                    models.CharField(blank=True, max_length=100, null=True, unique=True),
                ),
                ("mobile", models.CharField(max_length=10, unique=True)),
                (
                    "user_type",
                    models.CharField(choices=[("Company", "Company")], default="User", max_length=20),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("OtpInitialized", "OtpInitialized"),
                            ("Deactivated", "Deactivated"),
                            ("Paused", "Paused"),
                            ("Deleted", "Deleted"),
                            ("OtpVerified", "OtpVerified"),
                        ],
                        default="OtpInitialized",
                        max_length=20,
                    ),
                ),
                ("password", models.CharField(blank=True, max_length=255, null=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                (
                    "successive_login_failure_count",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
                (
                    "profile_pic",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
            ],
            options={
                "unique_together": {("mobile", "email")},
            },
        ),
    ]
