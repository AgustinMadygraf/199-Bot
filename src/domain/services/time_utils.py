"""
Path: src/domain/entities/f1_models.py
"""

from datetime import datetime, timezone, timedelta

def convert_utc_to_local(date_str: str, time_str: str, local_offset_hours: int = -3) -> str:
    try:
        time_clean = time_str.replace("Z", "")
        utc_dt = datetime.strptime(f"{date_str} {time_clean}", "%Y-%m-%d %H:%M:%S")
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
        local_tz = timezone(timedelta(hours=local_offset_hours))
        local_dt = utc_dt.astimezone(local_tz)
        
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_semana = dias[local_dt.weekday()]
        
        return f"{dia_semana} {local_dt.strftime('%d/%m')} a las {local_dt.strftime('%H:%M')} hs"
    except Exception:
        return f"{date_str} {time_str}"
