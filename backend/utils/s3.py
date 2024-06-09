import boto3, os
from botocore.exceptions import ClientError
from botocore.client import Config
from django.conf import settings


ENABLE_IAM_ROLE = settings.ENABLE_IAM_ROLE
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
S3_REGION_NAME = settings.S3_REGION_NAME
S3_ACCESS_ID = settings.S3_ACCESS_ID
S3_ACCESS_KEY = settings.S3_ACCESS_KEY
REGION_NAME = S3_REGION_NAME
AWS_BASE_URL = "https://" + AWS_STORAGE_BUCKET_NAME + ".s3." + S3_REGION_NAME + ".amazonaws.com/"
ENDPOINT_URL = "https://" + AWS_STORAGE_BUCKET_NAME + ".s3." + S3_REGION_NAME + ".amazonaws.com"


class MediaStorage:
    bucket_name = AWS_STORAGE_BUCKET_NAME

    def upload(self, file_path, content):
        if ENABLE_IAM_ROLE:
            s3 = boto3.resource(service_name="s3", region_name=REGION_NAME, endpoint_url=ENDPOINT_URL)
        else:
            s3 = boto3.resource(
                service_name="s3",
                region_name=REGION_NAME,
                aws_access_key_id=S3_ACCESS_ID,
                aws_secret_access_key=S3_ACCESS_KEY,
                endpoint_url=ENDPOINT_URL,
            )
        s3.Bucket(self.bucket_name).put_object(Key=file_path, Body=content)
        return os.path.join(AWS_BASE_URL, AWS_STORAGE_BUCKET_NAME, file_path)

    def generate_signed_url_for_read(self, filepath, content_type, expiration):

        filepath = filepath.replace(AWS_STORAGE_BUCKET_NAME + "/", "")

        if ENABLE_IAM_ROLE:
            s3_client = boto3.client(
                "s3", config=Config(signature_version="s3v4"), region_name=S3_REGION_NAME, endpoint_url=ENDPOINT_URL
            )
        else:
            s3_client = boto3.client(
                "s3",
                config=Config(signature_version="s3v4"),
                region_name=S3_REGION_NAME,
                aws_access_key_id=S3_ACCESS_ID,
                aws_secret_access_key=S3_ACCESS_KEY,
                endpoint_url=ENDPOINT_URL,
            )
        try:
            try:
                s3_client.head_object(Bucket=self.bucket_name, Key=filepath)
            except:
                if ENABLE_IAM_ROLE:
                    s3_client = boto3.client("s3", config=Config(signature_version="s3v4"), region_name=S3_REGION_NAME)
                else:
                    s3_client = boto3.client(
                        "s3",
                        config=Config(signature_version="s3v4"),
                        region_name=S3_REGION_NAME,
                        aws_access_key_id=S3_ACCESS_ID,
                        aws_secret_access_key=S3_ACCESS_KEY,
                    )

            response = s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket_name, "Key": filepath, "ResponseContentType": content_type},
                ExpiresIn=expiration,
            )
            return response
        except ClientError as e:
            return None

    def get_file_size(self, s3_url):
        s3_parts = s3_url.split("/")
        s3_bucket_name = AWS_STORAGE_BUCKET_NAME
        s3_object_key = "/".join(s3_parts[3:])
        if ENABLE_IAM_ROLE:
            s3_client = boto3.client(
                "s3", config=Config(signature_version="s3v4"), region_name=S3_REGION_NAME, endpoint_url=ENDPOINT_URL
            )
        else:
            s3_client = boto3.client(
                "s3",
                config=Config(signature_version="s3v4"),
                region_name=S3_REGION_NAME,
                aws_access_key_id=S3_ACCESS_ID,
                aws_secret_access_key=S3_ACCESS_KEY,
                endpoint_url=ENDPOINT_URL,
            )
        response = s3_client.head_object(Bucket=s3_bucket_name, Key=s3_object_key)
        file_size = response["ContentLength"]
        if file_size >= 1024:
            return True
        return False

    def delete_file(self, filepath):

        if AWS_BASE_URL in filepath:
            filepath = filepath.split("com/")[-1]

        if ENABLE_IAM_ROLE:
            s3_client = boto3.client(
                "s3", config=Config(signature_version="s3v4"), region_name=S3_REGION_NAME, endpoint_url=ENDPOINT_URL
            )
        else:
            s3_client = boto3.client(
                "s3",
                config=Config(signature_version="s3v4"),
                region_name=S3_REGION_NAME,
                aws_access_key_id=S3_ACCESS_ID,
                aws_secret_access_key=S3_ACCESS_KEY,
                endpoint_url=ENDPOINT_URL,
            )
        try:
            response = s3_client.delete_object(Bucket=self.bucket_name, Key=filepath)
            return response
        except ClientError as e:
            return None
