import datetime


def datetime_to_rfc3339_string(date: datetime.datetime) -> str:
    rfc3339_date = date
    rfc3339_date = rfc3339_date.replace(microsecond=0)
    rfc3339_date = rfc3339_date.astimezone()

    return rfc3339_date.isoformat()
