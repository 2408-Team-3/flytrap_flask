from flask import Flask, request
from ..logger.log_error import log_error


def setup_flask_error_handler(app: Flask) -> None:
    """Sets up a global error handler for the Flask app."""

    @app.errorhandler(Exception)
    def handle_exception(error: Exception) -> None:
        req_info = {
            "method": request.method,
            "path": request.path,
        }

        log_error(error, handled=False, req=req_info)
        raise error
