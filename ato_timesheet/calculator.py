from datetime import datetime, timedelta
import random

from ato_timesheet.models import CalculationResult, PeriodCalibration

class HoursCalculator:
    MIN_HOURS = 8.5 # minimum number of hours worked in a day, inclusive of lunch hour
    DAY_START_HOUR = 8 # e.g. 8 oclock
    DAY_START_HOUR_VARIANCE_MINUTES = list(range(0, 30, 15)) # List of minutes to add to day start hour
    HOURS_VARIANCE_MINUTES = list(range(0, 90, 10)) # List of minutes to add to hours worked

    def __init__(self, period_calibrations: list[PeriodCalibration] = []):
        self.period_calibrations: list[PeriodCalibration] = period_calibrations

    def calculate(self, date: datetime.date) -> CalculationResult:
        _min_hours = self.MIN_HOURS
        _day_start_hour = self.DAY_START_HOUR

        for pc in self.period_calibrations:
            if pc.start_date <= date <= pc.end_date:
                _min_hours = pc.min_hours
                _day_start_hour = pc.day_start_hour

            day_start_time_hour_offset = _day_start_hour + random.choice(self.DAY_START_HOUR_VARIANCE_MINUTES)/60
            day_end_time_hour_offset = day_start_time_hour_offset + _min_hours + random.choice(self.HOURS_VARIANCE_MINUTES)/60

            return CalculationResult(
                day_start_time=self._datetime(date, hour_offset=day_start_time_hour_offset),
                day_end_time=self._datetime(date, hour_offset=day_end_time_hour_offset),
                lunch_break_start_time=self._datetime(date, hour_offset=12),
                lunch_break_end_time=self._datetime(date, hour_offset=13),
            )

    def _datetime(self, date: datetime.date, hour_offset: int = 0, minute_offset: int = 0) -> datetime:
        return (datetime.combine(date, datetime.min.time()) + timedelta(hours=hour_offset, minutes=minute_offset))

