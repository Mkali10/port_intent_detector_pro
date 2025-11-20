# webapp/app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from backend.monitor import start_monitor_thread
from backend.monitor import scan_connections

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store last seen connections to avoid duplicate emits
seen_connections = set()

@app.route("/")
def index():
    return render_template("index.html")

def emit_new_connection(conn):
    """Emit new connection to all connected clients"""
    key = (conn.pid, conn.laddr, conn.raddr, conn.proto)
    if key not in seen_connections:
        seen_connections.add(key)
        socketio.emit("new_connection", {
            "pid": conn.pid,
            "name": conn.name,
            "exe": conn.exe,
            "local": f"{conn.laddr[0]}:{conn.laddr[1]}",
            "remote": f"{conn.raddr[0]}:{conn.raddr[1]}",
            "proto": conn.proto,
            "intent": conn.intent(),
            "suspicious": conn.is_suspicious()
        })

def run_web():
    """Run Flask + SocketIO web server with background monitor"""
    start_monitor_thread(poll_interval=2.0, callback=emit_new_connection)
    print("Starting Port Intent Detector PRO Web Dashboard on http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=5000)
