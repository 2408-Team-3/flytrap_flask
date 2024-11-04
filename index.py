from flask import Flask

class Flytrap:
    def __init__(self, config):
        self.project_id = config.get("project_id")
        self.api_endpoint = config.get("api_endpoint")
        self.api_key = config.get("api_key")
    

    def setup_flask_error_handler(self, app):
        @app.errorhandler(Exception)
        def handle_exception(error):
            self._log_error(error)
            # raise error # Pass the error on to any other error handlers the user might have?
            
