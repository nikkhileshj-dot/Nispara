import psutil

def get_system_status():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    return (
        f"CPU usage is {cpu} percent. "
        f"RAM usage is {ram} percent."
    )