import sys
from datetime import datetime
from ..logger.log_error import log_error

global_handlers_set = False


def system_exception_handler(exc_type, exc_value, exc_traceback):
    """System-wide exception handler for uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    timestamp = datetime.now().astimezone()
    log_error(exc_value, timestamp)


def setup_system_handler():
    global global_handlers_set

    if global_handlers_set:
        return

    global_handlers_set = True
    sys.excepthook = system_exception_handler
