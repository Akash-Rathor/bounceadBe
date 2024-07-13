from rest_framework import serializers
from backend.models.ads import *


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"


class AdCampaignSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    campaign_type = serializers.SerializerMethodField()
    target_audience = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()

    class Meta:
        model = AdCampaign
        fields = "__all__"

    def get_company(self, obj):
        return {"id": obj.company.id, "name": obj.company.name} if obj.company else None

    def get_campaign_type(self, obj):
        return {"id": obj.campaign_type.id, "type": obj.campaign_type.name} if obj.campaign_type else None

    def get_target_audience(self, obj):
        return [
            {"id": audience.id, "gender": audience.gender, "age_group": audience.age_group}
            for audience in obj.target_audience.all()
        ]

    def get_locations(self, obj):
        return {"id": obj.locations.id, "name": obj.locations.name} if obj.locations else None
