import traceback
import requests
import sys
from datetime import datetime
from typing import Dict
from flask import Flask
from flytrap import FlytrapError

class Flytrap:
    def __init__(self, config: Dict[str, str]) -> None:
        """
        Initializes the Flytrap instance with configuration.

        :param config: Dictionary containing 'project_id', 'api_endpoint', and 'api_key'.
        """
        sys.excepthook = self.system_exception_handler
        self.project_id: str = config.get("project_id")
        self.api_endpoint: str = config.get("api_endpoint")
        self.api_key: str = config.get("api_key")
    
    def system_exception_handler(self, exc_type, exc_value, exc_traceback):
        # Allow user to stop the program with keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.timestamp = datetime.now().astimezone()
        self.capture_exception(exc_value)

    def setup_flask_error_handler(self, app: Flask) -> None:
        """
        Sets up a global error handler for the Flask app.

        :param app: The Flask application instance.
        """
        @app.errorhandler(Exception)
        def handle_exception(error: Exception) -> None:
            self._log_error(error, False)
            raise error 

    def capture_exception(self, e: Exception) -> None:
        """
        Captures an exception and logs it as handled.

        :param e: The exception to capture.
        """
        self._log_error(e, True)

    def _log_error(self, e: Exception, handled: bool) -> None:
        """
        Logs an error and sends it to the backend.

        :param e: The exception to log.
        :param handled: Boolean indicating whether the exception was handled explicitly.
        """
        if not e:
            return
        
        data: Dict[str, str] = {
            'error': {
                'name': type(e).__name__,
                'message': str(e),
                'stack': traceback.format_exc(),
            },
            'timestamp': datetime.now().astimezone().isoformat(),
            'handled': handled,
            'project_id': self.project_id
        }

        headers: Dict[str, str] = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
        }

        try:
            print("[flytrap] Sending error to the backend...")
            response = requests.post(f"{self.api_endpoint}/api/errors", json={"data": data}, headers=headers)
            response.raise_for_status()
            print("[flytrap]", response.status_code, response.text)
        except requests.RequestException as e:
            print(f"[flytrap] An error occurred sending error data: %s", e)
            raise FlytrapError("Failed to send error data to Flytrap API.", e)