# backend
import datetime
import platform

def timestamp():
    """Return current timestamp string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_suspicious(port: int, proto: str):
    """Return True if port/protocol combination is considered suspicious."""
    # Example: uncommon ports
    common_ports = {22, 25, 53, 80, 443, 587, 993, 3306, 5432, 5000, 1194}
    if port not in common_ports:
        return True
    return False

def system_info():
    """Return system info string."""
    return f"{platform.system()} {platform.release()} ({platform.machine()})"
