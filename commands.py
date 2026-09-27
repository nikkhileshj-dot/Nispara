import webbrowser
import subprocess
import os
import urllib.parse
import pyautogui

from datetime import datetime
from urllib.parse import quote

from screenshot import take_screenshot
from battery import get_battery
from camera import open_camera
from system_info import get_system_status
from reminder import set_reminder
from web_search import search_web
from memory import remember, recall, forget


# ============================================================
# WHISPER COMMAND CORRECTIONS
# ============================================================

def correct_command(command):

    command = command.lower().strip()

    # Remove punctuation
    command = command.rstrip(".,!?")

    # Common Whisper mistakes
    corrections = {
        "lant chrome": "launch chrome",
        "laun chrome": "launch chrome",
        "lanch chrome": "launch chrome",
        "lunch chrome": "launch chrome",

        "lant browser": "launch browser",
        "laun browser": "launch browser",
        "lanch browser": "launch browser",

        "open chome": "open chrome",
        "open crome": "open chrome",
        "launch chome": "launch chrome",
        "launch crome": "launch chrome",

        "opn chrome": "open chrome",
        "opn calculator": "open calculator",
        "opn notepad": "open notepad",

        "calclator": "calculator",
        "calculater": "calculator",

        "not pad": "notepad",
        "file explore": "file explorer",
        "file exploer": "file explorer",

        "comand prompt": "command prompt",
        "command promt": "command prompt",
    }

    return corrections.get(command, command)


# ============================================================
# MAIN COMMAND EXECUTOR
# ============================================================

def execute(command):

    if not command:
        return None

    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    command = command.lower().strip()
    command = command.rstrip(".,!?")

    # Whisper correction
    command = correct_command(command)


    # ========================================================
    # MEMORY
    # ========================================================

    if command.startswith("my name is "):

        name = command[len("my name is "):].strip().title()

        if name:

            if remember("name", name):
                return f"Nice to meet you, {name}. I'll remember your name."

            return "Sorry, I couldn't save your name."


    if command.startswith("remember my name is "):

        name = command[len("remember my name is "):].strip().title()

        if name:

            if remember("name", name):
                return f"Got it. I'll remember your name is {name}."

            return "Sorry, I couldn't save your name."


    if command in [
        "what is my name",
        "whats my name",
        "what's my name",
        "do you know my name",
        "who am i"
    ]:

        name = recall("name")

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."


    if command in [
        "forget my name",
        "forget my name please",
        "forget my name now"
    ]:

        if forget("name"):
            return "Okay, I've forgotten your name."

        return "I don't have your name saved."


    # --------------------------------------------------------
    # REMOVE COMMON FILLER WORDS
    # --------------------------------------------------------

    fillers = [
        "please ",
        "can you ",
        "could you ",
        "would you ",
        "will you ",
        "the ",
        "a ",
        "an "
    ]

    changed = True

    while changed:

        changed = False

        for filler in fillers:

            if command.startswith(filler):

                command = command[len(filler):].strip()
                changed = True
                break


    # ========================================================
    # NOTEPAD
    # ========================================================

    if command in [
        "open notepad",
        "launch notepad",
        "start notepad",
        "notepad"
    ]:

        subprocess.Popen("notepad.exe")

        return "Opening Notepad."


    # ========================================================
    # CALCULATOR
    # ========================================================

    if command in [
        "open calculator",
        "launch calculator",
        "start calculator",
        "calculator",
        "open the calculator",
        "launch the calculator"
    ]:

        try:

            calculator_path = r"C:\Windows\System32\calc.exe"

            if os.path.exists(calculator_path):

                subprocess.Popen([calculator_path])

                return "Opening Calculator."

            return "Sorry, Calculator was not found on this computer."

        except Exception as e:

            print(
                "Calculator error:",
                type(e).__name__,
                "-",
                e
            )

            return "Sorry, I couldn't open Calculator."


    # ========================================================
    # PAINT
    # ========================================================

    if command in [
        "open paint",
        "launch paint",
        "start paint",
        "paint",
        "open the paint",
        "launch the paint"
    ]:

        try:

            paint_path = r"C:\Windows\System32\mspaint.exe"

            if not os.path.exists(paint_path):

                return "Sorry, Paint was not found on this computer."

            subprocess.Popen([paint_path])

            return "Opening Paint."

        except Exception as e:

            print(
                "Paint error:",
                type(e).__name__,
                "-",
                e
            )

            return "Sorry, I couldn't open Paint."


    # ========================================================
    # CAMERA
    # ========================================================

    if command in [
        "open camera",
        "launch camera",
        "start camera",
        "camera",
        "open the camera",
        "launch the camera",
        "start the camera"
    ]:

        try:

            return open_camera()

        except Exception as e:

            print(
                "Camera error:",
                e
            )

            return "Sorry, I couldn't open the camera."


    # ========================================================
    # COMMAND PROMPT
    # ========================================================

    if command in [
        "open cmd",
        "launch cmd",
        "start cmd",
        "open command prompt",
        "launch command prompt",
        "start command prompt",
        "command prompt",
        "cmd"
    ]:

        subprocess.Popen("cmd.exe")

        return "Opening Command Prompt."


    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if command in [
        "open file explorer",
        "launch file explorer",
        "start file explorer",
        "file explorer",
        "open explorer",
        "launch explorer",
        "start explorer",
        "explorer"
    ]:

        subprocess.Popen("explorer.exe")

        return "Opening File Explorer."


    # ========================================================
    # BROWSER CONTROLS
    # ========================================================

    if command in [
        "go back",
        "go backwards",
        "back",
        "browser back"
    ]:

        pyautogui.hotkey("alt", "left")

        return "Going back."


    if command in [
        "go forward",
        "go forwards",
        "forward",
        "browser forward"
    ]:

        pyautogui.hotkey("alt", "right")

        return "Going forward."


    if command in [
        "refresh",
        "refresh page",
        "reload",
        "reload page"
    ]:

        pyautogui.hotkey("ctrl", "r")

        return "Refreshing."


    if command in [
        "close browser",
        "close chrome",
        "close the browser",
        "close the chrome"
    ]:

        pyautogui.hotkey("alt", "f4")

        return "Closing browser."


    # ========================================================
    # GOOGLE
    # ========================================================

    if command in [
        "open google",
        "launch google",
        "start google",
        "google"
    ]:

        webbrowser.open(
            "https://www.google.com"
        )

        return "Opening Google."


    # ========================================================
    # CHROME
    # ========================================================

    if command in [
        "open chrome",
        "launch chrome",
        "start chrome",
        "open browser",
        "launch browser",
        "start browser",
        "chrome",
        "browser"
    ]:

        try:

            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    "",
                    "chrome"
                ],
                shell=False
            )

        except Exception:

            webbrowser.open(
                "https://www.google.com"
            )

        return "Opening Chrome."


    # ========================================================
    # WEB SEARCH
    # ========================================================

    web_search_prefixes = [
        "search web for ",
        "search the web for ",
        "search web ",
        "search the web ",
        "web search for ",
        "web search ",
        "look up online ",
        "search online for ",
        "search online "
    ]

    for prefix in web_search_prefixes:

        if command.startswith(prefix):

            query = command[
                len(prefix):
            ].strip()

            if not query:

                return "What would you like me to search for?"

            print(
                f"🌐 Web search: {query}"
            )

            results = search_web(
                query,
                max_results=5
            )

            if not results:

                return (
                    "Sorry, I couldn't find "
                    "any web results."
                )


            # ------------------------------------------------
            # Build a concise response
            # ------------------------------------------------

            response_parts = []

            for result in results[:3]:

                title = result.get(
                    "title",
                    ""
                ).strip()

                body = result.get(
                    "body",
                    ""
                ).strip()

                if title and body:

                    # Keep spoken results short
                    if len(body) > 250:

                        body = body[:250] + "..."

                    response_parts.append(
                        f"{title}. {body}"
                    )


            if not response_parts:

                return (
                    "I found web results, "
                    "but couldn't extract useful information."
                )


            response = (
                f"According to my web search for "
                f"{query}: "
                + " ... ".join(response_parts)
            )


            # Prevent an extremely long TTS response
            if len(response) > 1200:

                response = response[:1200] + "..."


            return response


    # ========================================================
    # SEARCH IN CHROME
    # ========================================================

    chrome_search_prefixes = [
        "search in chrome for ",
        "search in chrome ",
        "search chrome for ",
        "search chrome "
    ]

    for prefix in chrome_search_prefixes:

        if command.startswith(prefix):

            query = command[
                len(prefix):
            ].strip()

            if query:

                url = (
                    "https://www.google.com/search?q="
                    + quote(query)
                )

                webbrowser.open(url)

                return f"Searching Chrome for {query}."


    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    search_google_prefixes = [
        "search google for ",
        "search google ",
        "google search for ",
        "google search "
    ]

    for prefix in search_google_prefixes:

        if command.startswith(prefix):

            query = command[
                len(prefix):
            ].strip()

            if query:

                url = (
                    "https://www.google.com/search?q="
                    + quote(query)
                )

                webbrowser.open(url)

                return (
                    f"Searching Google for {query}."
                )


    # ========================================================
    # GENERIC SEARCH
    # ========================================================

    search_prefixes = [
        "search for ",
        "look up ",
        "find ",
        "search "
    ]

    for prefix in search_prefixes:

        if command.startswith(prefix):

            query = command[
                len(prefix):
            ].strip()

            if query:

                url = (
                    "https://www.google.com/search?q="
                    + quote(query)
                )

                webbrowser.open(url)

                return (
                    f"Searching for {query}."
                )


    # ========================================================
    # SCREENSHOT
    # ========================================================

    if command in [
        "take a screenshot",
        "take screenshot",
        "screenshot",
        "capture screen",
        "capture screenshot"
    ]:

        try:

            result = take_screenshot()

            return "Screenshot taken."

        except Exception as e:

            print(
                "Screenshot error:",
                e
            )

            return "Sorry, I couldn't take a screenshot."


    # ========================================================
    # YOUTUBE
    # ========================================================

    if command.startswith("play "):

        query = command[5:].strip()

        if query:

            url = (
                "https://www.youtube.com/results?search_query="
                + quote(query)
            )

            webbrowser.open(url)

            return (
                f"Playing {query} on YouTube."
            )


    if command.startswith("youtube "):

        query = command[8:].strip()

        if query:

            url = (
                "https://www.youtube.com/results?search_query="
                + quote(query)
            )

            webbrowser.open(url)

            return (
                f"Opening YouTube results for {query}."
            )


    # ========================================================
    # NO COMMAND MATCH
    # ========================================================

    return None