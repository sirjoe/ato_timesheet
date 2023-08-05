import argparse

import ato_timesheet.config as c

parser = argparse.ArgumentParser()

parser.add_argument(
    '-i',
    '--input-filepath',
    help='path to input file r.',
    default=c.DEFAULT_INPUT_FILEPATH,
    action='store',
)
parser.add_argument(
    '-o',
    '--output-filepath',
    help='patht to generated csv file.',
    default=c.DEFAULT_OUTPUT_FILEPATH,
    action='store',
)