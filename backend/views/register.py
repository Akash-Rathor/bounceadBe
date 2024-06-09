from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.serializers.register import RegistrationSerializer
from rest_framework.permissions import AllowAny


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user_id": user.id,
                    "email": user.email,
                    "name": user.name,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
