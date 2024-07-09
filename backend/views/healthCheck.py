from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from backend.utils.datetime import datetime


@api_view(["GET"])
def health_check(request):
    data = {
        "status": "OK", 
        "current date and time": datetime.get_date_time(),
        "current date time in epoch": datetime.get_unix_timestamp()
        }
    return Response(data=data, status=status.HTTP_200_OK)
