import os


def read_source_file(file_path: str) -> str | None:
    """Reads the content of a source file."""
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        with open(file_path, "r") as file:
            return file.read()

    except Exception:
        return None
