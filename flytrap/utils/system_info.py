import sys
import platform

def get_system_details() -> str:
    """Retrieves system details, including the operating system and runtime information."""
    os_name = platform.system()
    os_version = platform.release()
    return {
        "runtime": f"Python/{sys.version.split()[0]}",
        "os": f"{os_name} {os_version}"
    }