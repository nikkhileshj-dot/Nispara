import threading
import time

def set_reminder(seconds, message):
    def remind():
        time.sleep(seconds)
        print(f"🔔 Reminder: {message}")

    threading.Thread(target=remind, daemon=True).start()
    return f"I'll remind you in {seconds} seconds."