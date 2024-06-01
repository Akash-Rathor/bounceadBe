from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from backend.utils.datetime import datetime


@api_view(['GET'])
def health_check(request):
    data = {
        'status':'OK',
        'current date and time':datetime.get_date_time()
    }
    return Response(data=data,status=status.HTTP_200_OK)