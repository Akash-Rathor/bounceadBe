from rest_framework.decorators import api_view
from backend.utils import validator
from backend.utils import response
from backend.models.ads import Location, AdCampaign
from backend.serializers.ads import LocationSerializer, AdCampaignSerializer
from django.db.utils import IntegrityError
import logging

logger = logging.getLogger(__name__)

@api_view(["GET", "POST", "DELETE"])
def location_view(request, id=None):
    if request.method == "GET":
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return response.respond_200(serializer.data)

    if request.method == "POST":
        schema = {"name": {"type": "string", "required": True}}
        request_data = validator.validate(schema, request)
        request_data["name"] = request_data["name"].title()
        try:
            location = Location.objects.create(**request_data)
            serializer = LocationSerializer(location)
            return response.respond_201(serializer.data)
        except IntegrityError:
            return response.respond_with_error(f"Location already exists")


    if request.method == "DELETE":
        try:
            location = Location.objects.get(id=id)
            location.delete()
            return response.respond_with_msg(msg="deleted successfully")
        except Location.DoesNotExist:
            return response.respond_with_error(f"Location with id {id} does not exist")

@api_view(["GET", "POST"])
def ad_campaign_view(request, id=None):
    if request.method == "GET":
        ads = AdCampaign.objects.all()
        serializer = AdCampaignSerializer(ads, many=True)
        return response.respond_200(serializer.data)

    # if request.method == "POST":
    #     schema = {
    #         "title": {"type": "string", "required": True},
    #         "description": {"type": "string", "required": True},
    #         "media_type": {"type": "string", "required": True},
    #         "file_path": {"type": "string", "required": True},
    #         "duration": {"type": "integer", "required": True},
    #         "bid_amount": {"type": "number", "required": True},
    #         "location": {"type": "integer", "required": True}
    #     }
    #     request_data = validator.validate(schema, request)
    #     try:
    #         location = Location.objects.get(id=request_data