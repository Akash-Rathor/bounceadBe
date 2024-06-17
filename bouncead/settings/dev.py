import enum, os


class Endpoints(enum.Enum):
    GENERATE_OTP = "otp"
    VERIFY_OTP = "otp/verify"
    REGISTER = "register"
    TOKEN = "token"
    TOKEN_REFRESH = "token/refresh"
    LOGIN = "login"


BLOCKED_TIMER = 12 * 60 * 60  # 12 hours
# TOKEN_EXPIRY = 300 # 1 year
TOKEN_EXPIRY = 31536000  # 1 year
OTP_VALIDITY = 90  # 90 seconds

# session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # to expire the session upon closing the browser
SESSION_COOKIE_AGE = 60 * 30  # 30 minutes of inactivity will expire the session
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_EXPIRY_MIDDLEWARE_ENABLED = True  # enable sessions for web app


# s3 configs
ENABLE_IAM_ROLE = True if os.getenv("ENABLE_IAM_ROLE") == "1" else False
AWS_STORAGE_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")
S3_ACCESS_ID = os.getenv("S3_ACCESS_ID")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SIGNED_URL_EXPIRY = int(os.getenv("SIGNED_URL_EXPIRY", 300))
DATA_UPLOAD_MAX_MEMORY_SIZE = 11 * 1024 * 1024  # 11 mb
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 mb
S3_RESTRICT_FILE = 2 * 1024 * 1024
