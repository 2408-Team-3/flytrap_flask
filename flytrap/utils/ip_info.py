from flask import request


def get_client_ip() -> str:
    """Extracts the IP address of the client from request headers."""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip
