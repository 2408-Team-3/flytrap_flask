def get_code_context(source: str, line_number: int, context_lines: int = 5) -> str:
    """Gets the surrounding context lines from the source code."""
    lines = source.split("\n")
    start = max(line_number - context_lines - 1, 0)
    end = min(line_number + context_lines, len(lines))

    return "\n".join(lines[start:end])
