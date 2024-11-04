import traceback
import requests
import logging
from datetime import datetime
from flask import Flask

class Flytrap:
    def __init__(self, config):
        self.project_id = config.get("project_id")
        self.api_endpoint = config.get("api_endpoint")
        self.api_key = config.get("api_key")

    def setup_flask_error_handler(self, app):
        @app.errorhandler(Exception)
        def handle_exception(error):
            self._log_error(error, False)
            # raise error # Pass the error on to any other error handlers the user might have?

    def capture_exception(self, e):
        self._log_error(e, True)

    def _log_error(self, e, handled):
        if not e:
            return
        
        data = {
            'error': {
                'name': type(e).__name__,
                'message': str(e),
                'stack': traceback.format_exc(),
            },
            'timestamp': datetime.now().astimezone(),
            'handled': handled,
            'project_id': self.project_id
        }

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
        }

        try:
            self.logger.info("[flytrap] Sending error to the backend...")
            response = requests.post(self.api_endpoint, json={"data": data}, headers=headers)
            response.raise_for_status()
            self.logger.info("[flytrap]", response.status_code, response.text)
        except requests.RequestException as e:
            self.logger.error("[flytrap] An error occurred sending error data: %s", e)
            # Raise a new FlytrapError?