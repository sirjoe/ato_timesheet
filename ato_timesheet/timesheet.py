import csv
from datetime import timedelta

import holidays 
import yaml

import ato_timesheet.config as c
from ato_timesheet.calculator import HoursCalculator
from ato_timesheet.models import CalculationResult, Input, PeriodCalibration
from ato_timesheet.parser import parser


args = parser.parse_args()


input: Input
period_calibrations: list[PeriodCalibration] = []

with open(args.input_filepath, 'r') as f:
    input: Input =  Input(**yaml.safe_load(f))

for pc in input.period_calibrations:
    period_calibrations.append(PeriodCalibration(**pc))

current_date = input.financial_year_start
hours_calculator = HoursCalculator(period_calibrations=period_calibrations)
au_holidays = holidays.country_holidays('AU')


with open(args.output_filepath, mode='w') as f:
    writer = csv.DictWriter(f, fieldnames=c.CSV_HEADERS)
    writer.writeheader()

    for d in range(c.DAYS_IN_YEAR):
        if current_date in au_holidays:
            writer.writerow({
                c.FIELD_DATE: current_date,
                c.FIELD_DAY_START_TIME: '-',
                c.FIELD_DAY_END_TIME: '-',
                c.FIELD_LUNCH_BREAK_START_TIME: '-',
                c.FIELD_LUNCH_BREAK_END_TIME: '-',
                c.FIELD_DAY_HOURS_WORKED: 0,  
                c.FIELD_NOTE: f"Public Holiday: {au_holidays.get(current_date)}",    
            })
        elif current_date in input.sick_leaves:
            writer.writerow({
                c.FIELD_DATE: current_date,
                c.FIELD_DAY_START_TIME: '-',
                c.FIELD_DAY_END_TIME: '-',
                c.FIELD_LUNCH_BREAK_START_TIME: '-',
                c.FIELD_LUNCH_BREAK_END_TIME: '-',
                c.FIELD_DAY_HOURS_WORKED: 0,  
                c.FIELD_NOTE: 'Sick Leave',    
            })
        elif current_date in input.annual_leaves:
            writer.writerow({
                c.FIELD_DATE: current_date,
                c.FIELD_DAY_START_TIME: '-',
                c.FIELD_DAY_END_TIME: '-',
                c.FIELD_LUNCH_BREAK_START_TIME: '-',
                c.FIELD_LUNCH_BREAK_END_TIME: '-',
                c.FIELD_DAY_HOURS_WORKED: 0,  
                c.FIELD_NOTE: 'Annual Leave',    
            })
        else:
            # Day actually worked
            result: CalculationResult = hours_calculator.calculate(current_date)
            entry = {
                c.FIELD_DATE: current_date,
                c.FIELD_DAY_START_TIME: result.day_start_time.time(),
                c.FIELD_DAY_END_TIME: result.day_end_time.time(),
                c.FIELD_LUNCH_BREAK_START_TIME: result.lunch_break_start_time.time(),
                c.FIELD_LUNCH_BREAK_END_TIME: result.lunch_break_end_time.time(),
                c.FIELD_DAY_HOURS_WORKED: round(result.hours_worked(), 2),  
                c.FIELD_NOTE: '',    
            }
            writer.writerow(entry)

        current_date = current_date + timedelta(days=1)