import argparse
import src.utilities.logging as log
from pylint.lint import Run

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
path = str(args.path)
threshold = float(args.threshold)

logger.info('PyLint Starting | '
             'Path: {} | '
             'Threshold: {} '.format(path, threshold))

results = Run([path], do_exit=False)

final_score = results.linter.stats['global_note']

if final_score < threshold:

    message = ('PyLint Failed | '
               'Score: {} | '
               'Threshold: {} '.format(final_score, threshold))

    logger.error(message)
    raise Exception(message)

else:
    message = ('PyLint Passed | '
               'Score: {} | '
               'Threshold: {} '.format(final_score, threshold))

    logger.info(message)

    exit(0)