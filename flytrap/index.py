import traceback
import requests
from datetime import datetime
from typing import Dict
from flask import Flask

class Flytrap:
    def __init__(self, config: Dict[str, str]) -> None:
        """
        Initializes the Flytrap instance with configuration.

        :param config: Dictionary containing 'project_id', 'api_endpoint', and 'api_key'.
        """
        self.project_id: str = config.get("project_id")
        self.api_endpoint: str = config.get("api_endpoint")
        self.api_key: str = config.get("api_key")

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
            response = requests.post(self.api_endpoint, json={"data": data}, headers=headers)
            response.raise_for_status()
            print("[flytrap]", response.status_code, response.text)
        except requests.RequestException as e:
            print(f"[flytrap] An error occurred sending error data: %s", e)
            # Raise a new FlytrapError?