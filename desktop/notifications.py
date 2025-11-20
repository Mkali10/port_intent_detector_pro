# desktop/notifications.py
import platform

def notify_suspicious(message):
    """Show desktop notification for suspicious connection"""
    system = platform.system()
    try:
        if system == "Windows":
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast("Port Intent Detector PRO", message, duration=5)
        elif system == "Linux":
            import subprocess
            subprocess.run(['notify-send', "Port Intent Detector PRO", message])
        elif system == "Darwin":  # macOS
            import subprocess
            script = f'display notification "{message}" with title "Port Intent Detector PRO"'
            subprocess.run(["osascript", "-e", script])
    except Exception as e:
        print(f"Notification failed: {e}")
