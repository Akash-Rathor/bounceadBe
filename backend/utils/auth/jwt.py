import jwt
import os
from backend.utils.datetime import datetime
from backend.utils.exceptions.http_exception import BadRequestError
from django.conf import settings


class JWTAuth:
    user = None

    def getAlgorithm(self):
        return "HS256"

    def get_user_payload(self, user, expiry_in_seconds):
        payload = {
            "exp": expiry_in_seconds,
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
            "type": user.user_type,
            "status": user.status,
            "super_admin_status": user.is_superuser,
            "profile_pic": user.profile_pic,
            "app_version": os.getenv("LATEST_APP_VERSION"),
        }

        return payload

    def generate(self, user, expiry_in_seconds=datetime.get_unix_timestamp() + settings.TOKEN_EXPIRY + 2):
        """Generate User Token"""
        payload = self.get_user_payload(user, expiry_in_seconds)
        token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=self.getAlgorithm())

        # self.__setUserDetails(payload=payload,rm_bm=rm_bm)

        return token, payload

    def decode(self, token, secret):
        """Decode User Token"""
        payload = jwt.decode(token, secret, algorithms=[self.getAlgorithm()], verify=False)

        # self.__setUserDetails(payload=payload,rm_bm=rm_bm)

        return payload

    # def __setUserDetails(self, payload,rm_bm=False):
    #     common_data={
    #         'id': payload['id'],
    #         'name': payload['name'],
    #         'email': payload['email'],
    #         'mobile': payload['mobile'],
    #         'role':payload['role'],
    #         'status': payload['status'],
    #         'super_admin_status':payload['super_admin_status'],
    #         'employee_code': payload['employee_code'],
    #         'profile_pic':payload.get('profile_pic',None),
    #         'token_origin':'PRAGATI_V2',
    #         "mobile_app_version":os.getenv('LATEST_APP_VERSION'),
    #         "v2_mobile_app_version":os.getenv('V2_MOBILE_APP_VERSION'),
    #     }

    def getUser(self):
        return self.user
