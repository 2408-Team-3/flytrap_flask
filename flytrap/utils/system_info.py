import sys
import platform

def get_system_details() -> str:
    """Returns the os and runtime in a user-friendly format."""
    os_name = platform.system()
    os_version = platform.release()
    return {
        "runtime": f"Python/{sys.version.split()[0]}",
        "os": f"{os_name} {os_version}"
    }