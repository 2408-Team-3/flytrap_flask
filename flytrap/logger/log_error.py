import traceback
import requests
from flask import Request
from datetime import datetime
from typing import Optional, List, Dict
from ..utils.stack_trace import parse_stack_trace
from ..utils.file_reader import read_source_file
from ..utils.code_context import get_code_context
from ..utils.exceptions import FlytrapError


def log_error(
    error: Exception,
    handled: bool,
    req: Optional[Dict] = None
) -> None:
    """Logs the error and sends it to the backend."""
    from ..config import get_config

    if not error:
        return

    config = get_config()
    stack_frames = parse_stack_trace(error)
    print('stack frames:')
    print(stack_frames)

    code_contexts: List[dict] = []
    if config.get("include_context", True) and stack_frames:
        for frame in stack_frames:
            source = read_source_file(frame["file"])

            if source:
                context = get_code_context(source, frame["line"])
                code_contexts.append({
                    "file": frame["file"],
                    "line": frame["line"],
                    "column": frame["column"],
                    "context": context,
                })

    data = {
        "error": {
            "name": type(error).__name__,
            "message": str(error),
            "stack": traceback.format_exc(),
        },
        "codeContexts": code_contexts,
        "handled": handled,
        "timestamp": datetime.now().astimezone().isoformat(),
        "project_id": config["project_id"],
        "method": req["method"] if req else None,
        "path": req["path"] if req else None,
    }

    try:
        print("[flytrap] Sending error to backend...")
        response = requests.post(
            f"{config['api_endpoint']}/api/errors",
            json={"data": data},
            headers={"x-api-key": config["api_key"]},
        )
        response.raise_for_status()
        print("[flytrap]", response.status_code, response.text)
    except requests.RequestException as e:
        print(f"[flytrap] Failed to send error data: {e}")
        raise FlytrapError("Failed to send error data to Flytrap API.", e)
