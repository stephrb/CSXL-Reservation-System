"""Reservations are the data object to keep track of user reservations"""
from pydantic import BaseModel, validator
from datetime import datetime

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
        
        if datetime(year=start_time.year, month=start_time.month, day=start_time.day) != datetime(year=v.year, month=v.month, day=v.day):
            raise ValueError(f'Start time and end time must be on the same day (start_time: {start_time}, end_time: {v})')
        return v