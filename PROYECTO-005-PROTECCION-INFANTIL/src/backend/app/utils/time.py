from datetime import datetime, timezone


def truncate_to_hours(dt: datetime, hours: int = 6) -> datetime:
    """
    Trunca una fecha UTC a un bucket de N horas.
    Se usa para reducir la precisión temporal de los reportes y evitar
    correlaciones de tiempo exactas.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    bucket_hour = (dt.hour // hours) * hours
    return dt.replace(hour=bucket_hour, minute=0, second=0, microsecond=0)
