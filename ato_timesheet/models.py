from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CalculationResult:
    day_start_time: datetime
    day_end_time: datetime
    lunch_break_start_time: datetime
    lunch_break_end_time: datetime

    def hours_worked(self) -> float:
        return ((self.day_end_time - self.day_start_time) - (self.lunch_break_end_time - self.lunch_break_start_time)).total_seconds() / 3600


@dataclass
class PeriodCalibration:
    start_date: datetime.date # YYYY-MM-DD
    end_date: datetime.date # YYYY-MM-DD
    min_hours: int # minimum number of hours worked in a day
    day_start_hour: int # e.g. 8 oclock


@dataclass
class Input:
    financial_year_start: datetime
    sick_leaves: list[datetime] = field(default_factory=[])
    annual_leaves: list[datetime] = field(default_factory=[])
    period_calibrations: list[PeriodCalibration] = field(default_factory=[])
