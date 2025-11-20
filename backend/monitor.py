# backend/monitor.py
import psutil
import time
import threading
from backend.intent_map import get_intent
from backend.utils import is_suspicious
from backend.database import log_connection

class ConnectionInfo:
    def __init__(self, pid, laddr, raddr, status, proto):
        self.pid = pid
        self.laddr = laddr  # (ip, port)
        self.raddr = raddr  # (ip, port)
        self.status = status
        self.proto = proto  # 'tcp' or 'udp'
        try:
            self.process = psutil.Process(pid)
            self.name = self.process.name()
            self.exe = self.process.exe()
        except Exception:
            self.process = None
            self.name = None
            self.exe = None

    def intent(self):
        if self.raddr:
            _, remote_port = self.raddr
            return get_intent(remote_port, self.proto)
        return "Unknown"

    def is_suspicious(self):
        if self.raddr:
            _, remote_port = self.raddr
            return is_suspicious(remote_port, self.proto)
        return False

def scan_connections():
    """Return list of outbound connections."""
    conns = psutil.net_connections(kind='inet')
    results = []
    for c in conns:
        if not c.raddr:
            continue
        proto = 'tcp' if c.type == psutil.SOCK_STREAM else 'udp'
        ci = ConnectionInfo(c.pid, c.laddr, c.raddr, c.status, proto)
        results.append(ci)
    return results

def monitor(poll_interval=2.0, callback=None):
    """Continuously monitor connections. Optionally call callback on new connection."""
    seen = set()
    try:
        while True:
            conns = scan_connections()
            for c in conns:
                key = (c.pid, c.laddr, c.raddr, c.proto)
                if key not in seen:
                    seen.add(key)
                    intent = c.intent()
                    suspicious = c.is_suspicious()
                    log_connection(c.pid, c.name, c.exe, c.laddr, c.raddr, c.proto, intent, suspicious)
                    output = f"[{c.proto.upper()}] {c.laddr} -> {c.raddr} | PID={c.pid} Name={c.name} | Intent={intent}"
                    if suspicious:
                        output += "SUSPICIOUS"
                    print(output)
                    if callback:
                        callback(c)
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Stopping Port Intent Detector PRO monitor.")

def start_monitor_thread(poll_interval=2.0, callback=None):
    """Run monitor in a separate thread."""
    t = threading.Thread(target=monitor, args=(poll_interval, callback), daemon=True)
    t.start()
    return t
