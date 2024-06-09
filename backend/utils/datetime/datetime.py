import datetime
from datetime import date
import time
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from backend.utils.exceptions.http_exception import BadRequestError


"""Return current date time string"""


def get_date_time():
    return timezone.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_jobs_date(date_str):
    """_summary_
        convert this datetime str %Y-%m-%dT%H:%M:%S.%fZ
    Returns:
        str: dd/mm/yyyy
    """
    return datetime.datetime.strptime(str(date_str), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%d/%m/%Y")


def change_datetime_to_epoch(datetime_string: str, format: str = "%d/%m/%Y %H:%M:%S"):
    try:
        # Parse the date string using the provided format
        dt = timezone.datetime.strptime(datetime_string, format)
        # Convert to a UTC timestamp and return as an integer
        return int(dt.timestamp())
    except:
        # Use the default format if the provided format fails
        dt = timezone.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())


def get_date_time_in_slash():
    return timezone.now().strftime("%d/%m/%Y %H:%M:%S")


def get_date():
    return timezone.now().strftime("%Y-%m-%d")


def get_date_in_ymd(date):
    val = datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
    return datetime.datetime.strptime(val, "%Y-%m-%d").date()


def get_time():
    return timezone.now().strftime("%H:%M:%S")


"""Return current unix timestamp"""


def get_unix_timestamp():
    return int(timezone.now().timestamp())


def get_unix_timestamp_after(seconds):
    new_datetime = int(timezone.now().timestamp()) + seconds
    return new_datetime


def get_date_time_after(days=0):
    dt = timezone.now() + timezone.timedelta(days=days)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def change_date_format(date_string):
    if date_string is None:
        return date_string
    return datetime.datetime.strptime(date_string, "%d/%m/%Y").date().strftime("%Y-%m-%d")


def get_diff_in_years(start_date, end_date=None):
    if end_date is None:
        end_date = datetime.datetime.today()

    val = None
    try:
        val = relativedelta(end_date, start_date).years
    except Exception as e:
        val = None

    return val


def today():
    return datetime.datetime.today()


def change_datetime_format(datetime_string: str, format: str):
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S").strftime(format)


def update_date_format(datetime_string: str, format: str):
    try:
        return datetime.datetime.strptime(datetime_string, "%d-%m-%Y").strftime(format)
    except:
        raise BadRequestError("Invalid date or date format.")


def get_formatted_date_time_after(format="%Y-%m-%d %H:%M:%S", days=0, hours=0, minutes=0, seconds=0):
    dt = datetime.datetime.today() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return dt.strftime(format)


def get_unix_timestamp_for_string(datetime_str, format):
    return int(time.mktime(datetime.datetime.strptime(datetime_str, format).timetuple()))


def is_valid_future_date(date_string):

    try:
        date_string = str(date_string)
        user_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        cur_date = date.today()
        user_date_timestamp = int(time.mktime(user_date.timetuple()))
        cur_date_timestamp = int(time.mktime(cur_date.timetuple()))
        if user_date_timestamp < cur_date_timestamp:
            raise BadRequestError("Previous date is not allowed!")
        return True
    except Exception as e:
        raise BadRequestError(e)


def is_valid_past_date(date_string):

    try:
        user_date = datetime.datetime.strptime(date_string, "%d-%m-%Y")
        cur_date = date.today()
        thirty_days_ago = cur_date - datetime.timedelta(days=30)
        user_date_timestamp = int(time.mktime(user_date.timetuple()))
        thirty_days_ago_timestamp = int(time.mktime(thirty_days_ago.timetuple()))
        if user_date_timestamp > thirty_days_ago_timestamp:
            raise BadRequestError("Only past date older than 30 days is allowed!")
        return True
    except Exception as e:
        raise BadRequestError(e)


def get_age_from_dob(dob):
    if not dob:
        raise BadRequestError("DOB is required.")
    dob_date = datetime.datetime.strptime(dob, "%d-%m-%Y")
    cur_date = datetime.datetime.now()
    age = cur_date.year - dob_date.year - ((cur_date.month, cur_date.day) < (dob_date.month, dob_date.day))
    return age


def convert_unix_to_minutes_and_seconds(unix_time: int):
    if isinstance(unix_time, int):
        seconds = unix_time % 60
        minutes = (unix_time // 60) % 60
        return f"{minutes}:{seconds}"
    raise BadRequestError("unix time is not an integer")


def convert_vintage_string(vintage_string):
    """
    vintage_string excepted in format : 10 Years 10 Months
    if value of months is equals to 12, it convert that to 0 and increase 1 in year.
    """
    if isinstance(vintage_string, str):
        date_matched = re.match(r"(?P<years>\w+) Years (?P<months>\w+) Months", vintage_string)
        if date_matched:
            years = int(date_matched.group("years"))
            months = int(date_matched.group("months"))
            if months >= 12:
                years += months // 12
                months = months % 12
            updated_vintage_date = f"{years} Years {months} Months"
            return updated_vintage_date

    else:
        return False
