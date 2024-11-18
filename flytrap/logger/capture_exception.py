from flask import request
from .log_error import log_error

def capture_exception(e: Exception) -> None:
    """Capture and log an exception, adding it to the logged errors tracker."""
    if not e:
        return
    
    req_info = {
        "method": request.method,
        "path": request.path,
    }
    
    # Log the error (using the log_error function)
    log_error(e, handled=True, req=req_info)
