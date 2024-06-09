import random
from backend.utils.datetime import datetime
import logging
import os
from uuid import uuid4

logger = logging.getLogger(__name__)
log_mode = os.getenv("LOG_MODE")


def logTypeService(data, log_type):

    data = str(data)
    if log_type == "debug":
        logger.debug(data)
    elif log_type == "info":
        logger.info(data)
    elif log_type == "error":
        logger.error(data)
    elif log_type == "warning":
        logger.warning(data)
    return True


class ApiCallLogQuery:
    """
    This class is use for logging
    """

    def __init__(self, uid=None):
        if uid is None:
            self.uid = self.__get_unique_id()
        else:
            self.uid = uid

    def __get_unique_id(self):
        return str(uuid4())

    """Return AuthSession
    
    Create AuthSession.
    """

    def create(self, data, log_type=None):

        if not log_type:
            log_type = "info" if result_status_code in range(199, 210) else "error"

        api_type = (data.get("api_type", "Internal"),)
        response = (data.get("response"),)
        method = (data.get("method"),)
        request_body = (data.get("request_body"),)
        result_status_code = data.get("result_status_code")
        endpoint = data.get("endpoint")

        logging_key = (f"{api_type}-{result_status_code}",)
        log_dict = {
            f"{logging_key}": {
                "response": response,
                "endpoint": endpoint,
                "request_body": request_body,
                "result_status_code": result_status_code,
                "error_traceback": method,
                "api_type": data.get("api_type"),
                "date": datetime.get_date_time(),
            }
        }

        log = logTypeService(log_dict, log_type)
        return log
