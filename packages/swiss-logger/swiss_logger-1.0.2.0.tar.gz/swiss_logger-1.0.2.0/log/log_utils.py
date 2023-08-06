import logging
import time

import coloredlogs
import pyfiglet

logger = None

LOG_FORMAT = '%(asctime)s %(hostname)s %(name)s[%(process)d][%(threadName)s:%(thread)d] %(levelname)s %(message)s'


def get_logger(name=None, level='DEBUG'):
    logger = logging.getLogger(name)
    coloredlogs.install(level=level, logger=logger, fmt=LOG_FORMAT)
    return logger


def log_enter_and_exit(orig_func):
    logger = get_logger('log_enter_and_exit')

    def wrapper(*args, **kwargs):
        func_full_name = '.'.join([orig_func.__module__, orig_func.__qualname__])
        logger.debug('[ENTER] {}'.format(func_full_name))
        start = int(time.time()) * 1000
        result = orig_func(*args, **kwargs)
        run_time = (int(time.time()) * 1000) - start
        logger.debug('[EXIT] {} (Execution time: {}ms)'.format(func_full_name, run_time))

        global exec_time_record
        exec_time_record.append((orig_func.__qualname__, run_time))
        return result

    return wrapper


def log_function_args_and_kwargs(orig_func):
    logger = get_logger('log_function_args_and_kwargs')

    def wrapper(*args, **kwargs):
        logger.info('Function: {} run with args: {}, and kwargs: {}'.format(orig_func.__name__, args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


exec_time_record = []


def log_function_runtime(orig_func):
    logger = get_logger('log_function_runtime')
    import time

    def wrapper(*args, **kwargs):
        start = int(time.time()) * 1000
        result = orig_func(*args, **kwargs)
        run_time = (int(time.time()) * 1000) - start
        logger.info('Function: {} execution time: {}ms'.format(orig_func.__qualname__, run_time))
        global exec_time_record
        exec_time_record.append((orig_func.__qualname__, run_time))
        return result

    return wrapper


def print_ascii_art(text, font=pyfiglet.DEFAULT_FONT):
    print()
    print(pyfiglet.figlet_format(text=text, font=font))
    print()
