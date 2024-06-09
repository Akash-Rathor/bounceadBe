from backend.queries.api_call_log import ApiCallLogQuery
from backend.utils.exceptions.http_exception import BadRequestError
import random, os
from backend.enums.content_type import ImageType, FileType
from backend.utils.s3 import MediaStorage
from backend.utils import validator
from django.conf import settings

SIGNED_URL_EXPIRY = settings.SIGNED_URL_EXPIRY


class S3Upload:

    def __init__(self):
        self.s3 = MediaStorage()
        self.to_remov = "!@#$%^&*()+=\/ "

    def s3_upload(self, request, filenameinp=None):
        try:
            input = {
                "file": request.FILES.get("file"),
                "upload_path": request.data.get("upload_path"),
            }
            if input.get("file") is None:
                raise BadRequestError("File not Found")

            if input.get("file").size >= settings.S3_RESTRICT_FILE:
                raise BadRequestError("File size can be maximum of 2 MB")

            elif input.get("upload_path") is None:
                raise BadRequestError("Upload path not Found")
        except BadRequestError as e:
            raise e
        except:
            # ConnectorCard = TeamsConnectorCard()
            # ConnectorCard.msg_structure(json_payload={'status':'S3 upload failed as memory exceeded'},title='Memory Error')
            # ConnectorCard.send()
            raise BadRequestError("Service is down, Please try again later")

        try:
            if not filenameinp:
                filename = self.__validate_filename(input.get("file").name)
            else:
                filename = filenameinp
            if "/" == input.get("upload_path")[-1]:
                location = input.get("upload_path") + filename
            else:
                location = os.path.join(input.get("upload_path"), filename)
            # location = input.get('upload_path')+"_" + str(random.randint(1, 9999999)) + "_" + str(datetime.get_unix_timestamp()) + filename

            s3_url = self.s3.upload(file_path=location, content=input.get("file"))

            if "com/" in s3_url:
                filepath = s3_url.split("com/")[-1]
            content = filepath.split(".")[-1]
            content_type = "application/json"
            # if content in ImageType.Image.value:
            #     content_type = f"image/{content}"
            if content in FileType.File.value:
                content_type = f"application/{content}"
            signed_url = self.s3.generate_signed_url_for_read(filepath, content_type, expiration=SIGNED_URL_EXPIRY)

            data = None
            data = {"s3_url": s3_url, "signed_url": signed_url}

            ApiCallLogQuery().create({"third_party": "AWS", "api_type": "S3_Upload", "response": data}, log_type="info")
            return data
        except Exception as e:
            ApiCallLogQuery().create({"third_party": "AWS", "api_type": "S3_Upload", "response": e}, log_type="error")
            raise BadRequestError("Unable to Upload")

    def get_signed_url(self, request, signed_url_expiry=SIGNED_URL_EXPIRY):
        rules = {"filepath": {"type": "list", "required": True}}
        input = validator.validate(rules, request)
        filepaths = input.get("filepath")
        data = []
        try:
            for filepath in filepaths:
                if ".amazonaws.com/" in filepath:
                    filepath = filepath.split("com/")[-1]
                content = filepath.split(".")[-1]
                if content in ImageType.Image.value:
                    content_type = f"image/{content}"
                elif content in FileType.File.value:
                    content_type = f"application/{content}"
                data.append(self.s3.generate_signed_url_for_read(filepath, content_type, expiration=signed_url_expiry))
            return data
        except Exception as e:
            ApiCallLogQuery().create(
                {"third_party": "AWS", "api_type": "PRV_SIGNED_URL", "response": e}, log_type="error"
            )
            raise BadRequestError("File not found")

    def __validate_filename(self, filename):
        for char in filename:
            if char in self.to_remov:
                filename = filename.replace(char, "_")
        return filename

    def delete_file_from_s3(self, filepath):
        self.s3.delete_file(filepath=filepath)
        return None
