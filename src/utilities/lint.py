"""
Linter configurations
"""
import argparse
from pylint.lint import Run
import src.utilities.logging as log

logger = log.get_logger(__name__)

parser = argparse.ArgumentParser(prog="LINT")

parser.add_argument('-p',
                    '--path',
                    help='path to directory you want to run pylint | '
                         'Default: %(default)s | '
                         'Type: %(type)s ',
                    default='./src',
                    type=str)

parser.add_argument('-t',
                    '--threshold',
                    help='score threshold to fail pylint runner | '
                         'Default: %(default)s | '
                         'Type: %(type)s ',
                    default=7,
                    type=float)

args = parser.parse_args()
PATH = str(args.path)
threshold = float(args.threshold)

logger.info('PyLint Starting | '
             'Path: %s | '
             'Threshold: %s ', PATH, threshold)

results = Run([PATH], do_exit=False)

final_score = results.linter.stats['global_note']

if final_score < threshold:
    message = (f"PyLint Failed | \
               Score: {final_score} | \
               Threshold: {threshold} ")

    logger.error(message)
    raise ValueError('Threshold does not match')

else:
    message = (f"PyLint Passed | \
               Score: {final_score} | \
               Threshold: {threshold} ")

    logger.info(message)

    exit(0)
