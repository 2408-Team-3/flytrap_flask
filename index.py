from flask import Flask

class Flytrap:
    def __init__(self, app: Flask, config):
        self.project_id = config.get("project_id")
        self.api_endpoint = config.get("api_endpoint")
        self.api_key = config.get("api_key")
        self.app = app
    