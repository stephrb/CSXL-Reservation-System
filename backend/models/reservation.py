"""Reservations are the data object to keep track of user reservations"""
from pydantic import BaseModel, validator
from datetime import datetime
from zoneinfo import ZoneInfo

class Reservation(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime

class ReservationForm(BaseModel):
    start_time: datetime
    end_time: datetime
    reservable_id: int
    
    @validator('start_time', 'end_time')
    def validate_time_slots(cls, v: datetime):
        if v.minute not in [0, 30] or v.microsecond != 0 or v.second != 0:
            raise ValueError(f'Reservation time: {v} is only available at XX:00 or XX:30')
        return v
    
    @validator('end_time')
    def validate_end_time(cls, v: datetime, values: dict):
        start_time: datetime = values.get('start_time')
        if v <= start_time:
            raise ValueError('End time must be after start time')
        
        start_time_est, v_est = start_time.astimezone(ZoneInfo('America/New_York')), v.astimezone(ZoneInfo('America/New_York'))

        if datetime(year=start_time_est.year, month=start_time_est.month, day=start_time_est.day) != datetime(year=v_est.year, month=v_est.month, day=v_est.day):
            raise ValueError(f'Start time and end time must be on the same day (start_time: {start_time}, end_time: {v})')
        return v