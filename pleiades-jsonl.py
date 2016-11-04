"""Convert Pleiades JSON dump to JSON Lines (new-line-delimited JSON)
"""

import argparse
from functools import wraps
import gzip
import json
import jsonlines
import inspect
import logging
import os
import progressbar
import re
import shutil
import sys
import traceback
import wget

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_PLEIADES_URI = ('http://atlantides.org/downloads/pleiades/json/'
                        'pleiades-places-latest.json.gz')
POSITIONAL_ARGUMENTS = [
    ['-l', '--loglevel', logging.getLevelName(DEFAULT_LOG_LEVEL),
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR'],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)'],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)'],
    ['-p', '--pleiades', DEFAULT_PLEIADES_URI, 'Pleiades JSON dataset to'
        ' use (default: {})'.format(DEFAULT_PLEIADES_URI)]
]


def arglogger(func):
    """
    decorator to log argument calls to functions
    """
    @wraps(func)
    def inner(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.debug("called with arguments: %s, %s" % (args, kwargs))
        return func(*args, **kwargs)
    return inner


@arglogger
def main(args):
    """
    main function
    """
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    fn_pdata = get_pleiades(args.pleiades)
    print('\nreading json from local file {}'.format(fn_pdata))
    with open(fn_pdata, 'r') as f_in:
        places = json.load(f_in)

    fn_out = '{}.jsonl'.format(os.path.splitext(os.path.basename(fn_pdata))[0])
    bar = progressbar.ProgressBar(redirect_stdout=True)
    with jsonlines.open(fn_out, mode='w', sort_keys=True,
                        compact=True) as f_out:
        print('writing json to local  file {}'.format(fn_out))
        i = 0
        for place in bar(places['@graph']):
            logger.debug(place['title'])
            f_out.write(place)
            i += 1

    print('wrote {} json objects to {}'.format(i, fn_out))


@arglogger
def get_pleiades(where):
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    print('fetching {}'.format(where))
    if where.startswith('http'):
        fn = wget.download(where)
    else:
        fn = where
    logger.debug('pleiades filename: {}'.format(fn))
    if fn.endswith('.gz'):
        with gzip.open(fn, 'rb') as f_in:
            with open(fn[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        fn = fn[:-3]
        logger.debug('uncompressed to: {}'.format(fn))
    return fn


if __name__ == "__main__":
    log_level = DEFAULT_LOG_LEVEL
    log_level_name = logging.getLevelName(log_level)
    logging.basicConfig(level=log_level)
    try:
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        for p in POSITIONAL_ARGUMENTS:
            d = {
                'help': p[3]
            }
            if type(p[2]) == bool:
                if p[2] is False:
                    d['action'] = 'store_true'
                    d['default'] = False
                else:
                    d['action'] = 'store_false'
                    d['default'] = True
            else:
                d['default'] = p[2]
            parser.add_argument(
                p[0],
                p[1],
                **d)
        # example positional argument
        # parser.add_argument(
        #     'foo',
        #     metavar='N',
        #     type=str,
        #     nargs='1',
        #     help="foo is better than bar except when it isn't")
        args = parser.parse_args()
        if args.loglevel is not None:
            args_log_level = re.sub('\s+', '', args.loglevel.strip().upper())
            try:
                log_level = getattr(logging, args_log_level)
            except AttributeError:
                logging.error(
                    "command line option to set log_level failed "
                    "because '%s' is not a valid level name; using %s"
                    % (args_log_level, log_level_name))
        if args.veryverbose:
            log_level = logging.DEBUG
        elif args.verbose:
            log_level = logging.INFO
        log_level_name = logging.getLevelName(log_level)
        logging.getLogger().setLevel(log_level)
        fn_this = inspect.stack()[0][1].strip()
        title_this = __doc__.strip()
        logging.info(': '.join((fn_this, title_this)))
        if log_level != DEFAULT_LOG_LEVEL:
            logging.warning(
                "logging level changed to %s via command line option"
                % log_level_name)
        else:
            logging.info("using default logging level: %s" % log_level_name)
        logging.debug("command line: '%s'" % ' '.join(sys.argv))
        main(args)
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print("ERROR, UNEXPECTED EXCEPTION")
        print(str(e))
        traceback.print_exc()
        os._exit(1)
