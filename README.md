# Tax Return Timesheet

ATO requests work-from-home employees to provide timesheet that tracks the number of hours worked in a financial year. This programme accepts custom configuration, including sick/annual leaves override and period calibration, and generates a timesheet CSV file. It logs the following for each day
* date
* work start time
* work end time
* lunch star time
* lunch end time
* total hours worked
* note (holiday name, etc)

## System Requirements

* Python >= 3.9
* Poetry

## Usage

Prepare an input file. Run the following at project root

```
> cp input.yaml.sample <path-to-your-input-file-with-file-name>
```
e.g.
```
> cp input.yaml.sample input.yaml
```
Refer to the commented code block within the input file and set up your own configuration where applicable.

Run the command below to generate timesheet CSV.

```
> poetry run python ato_timesheet/timesheet.py -i <path-to-input-file> -o <path-to-output-file>
```
e.g.
```
> poetry run python ato_timesheet/timesheet.py -i input.yaml -o generated/FY23_timesheet.csv
```

To see what options are accepted by the programme

```
> poetry run python ato_timesheet/timesheet.py -h
```