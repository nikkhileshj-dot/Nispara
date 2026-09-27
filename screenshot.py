import pyautogui
from datetime import datetime

def take_screenshot():
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pyautogui.screenshot(filename)
    return f"Screenshot saved as {filename}"