import psutil

def get_battery():
    battery = psutil.sensors_battery()

    if battery is None:
        return "I couldn't detect a battery."

    percent = battery.percent
    charging = battery.power_plugged

    if charging:
        return f"Battery is {percent} percent and is charging."
    else:
        return f"Battery is {percent} percent and is not charging."