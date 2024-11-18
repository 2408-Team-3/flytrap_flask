import re
import traceback

def parse_stack_trace(error: Exception) -> list[dict] | None:
    """Parses the stack trace and returns a list of file, line, and column info."""
    if not error:
        return []

    stack_trace = ''.join(traceback.format_exception(None, error, error.__traceback__))
    stack_lines = stack_trace.split("\n")[1:]
    stack_frames = []

    pattern = r"^\s*File\s+\"([^\"]+)\",\s+line\s+(\d+)(?:,\s+in\s+(.+))?"

    for line in stack_lines:
        match = re.match(pattern, line)
        if match:
            file, line_number, _ = match.groups()
            stack_frames.append({
                'file': file,
                'line': int(line_number),
            })

    stack_frames.reverse()
    return stack_frames[:10]
