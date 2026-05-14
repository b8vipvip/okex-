from datetime import datetime, timedelta, timezone


CN_TZ = timezone(timedelta(hours=8))


def now_cn() -> datetime:
    """Return current Beijing time as a timezone-naive datetime for MySQL DATETIME fields."""
    return datetime.now(CN_TZ).replace(tzinfo=None)
