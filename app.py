import time

from listener import model
from wake_word import wait_for_wake_word
from whisper_listener import listen_whisper
from speech import speak
from brain import ask_ai
from commands import execute
from memory import remember, recall, forget, get_all_memories


# ============================================================
# SETTINGS
# ============================================================

MIC_DEVICE = 1


# ============================================================
# SPEAK
# ============================================================

def speak_response(text):
    if not text:
        return

    speak(
        text,
        wake_model=model,
        mic_device=MIC_DEVICE
    )

# ============================================================
# SMART MEMORY
# ============================================================

def handle_memory(text):

    # --------------------------------------------------------
    # NORMALIZE COMMON WHISPER VARIATIONS
    # --------------------------------------------------------

    text = (
        text
        .lower()
        .strip()
        .rstrip(".,!?")
    )

    # Whisper may produce:
    # "remember, my name is nicky"
    # "remember my name is nicky"
    text = text.replace("remember,", "remember")
    text = text.replace("forget,", "forget")
    text = text.replace("forgot,", "forgot")


    # --------------------------------------------------------
    # FORGET MY NAME
    # --------------------------------------------------------

    if text in [
        "forget my name",
        "forgot my name",
        "forget my name memory",
        "delete my name",
        "remove my name",
        "forget about my name",
        "forgot about my name"
    ]:

        if forget("name"):

            speak_response(
                "Okay, I've forgotten your name."
            )

        else:

            speak_response(
                "I don't have your name saved."
            )

        return True


    # --------------------------------------------------------
    # FORGET MY NAME IS ...
    # --------------------------------------------------------

    if (
        text.startswith("forget my name is ")
        or text.startswith("forgot my name is ")
        or text.startswith("forget about my name is ")
        or text.startswith("forgot about my name is ")
    ):

        if forget("name"):

            speak_response(
                "Okay, I've forgotten your name."
            )

        else:

            speak_response(
                "I don't have your name saved."
            )

        return True


    # --------------------------------------------------------
    # WHAT DO YOU REMEMBER?
    # --------------------------------------------------------

    if text in [
        "what do you remember",
        "what do you remember about me",
        "what do you know about me"
    ]:

        memories = get_all_memories()

        if not memories:

            speak_response(
                "I don't have any saved memories yet."
            )

            return True


        memory_values = []

        for key, value in memories.items():

            if key == "name":

                memory_values.append(
                    f"your name is {value}"
                )

            else:

                memory_values.append(
                    str(value)
                )


        # Keep response short
        memory_values = memory_values[-5:]


        response = (
            "I remember that "
            + ", and ".join(memory_values)
            + "."
        )

        speak_response(response)

        return True


    # --------------------------------------------------------
    # REMEMBER MY NAME
    # --------------------------------------------------------

    if (
        text.startswith("remember my name is ")
        or text.startswith("remember about my name is ")
    ):

        if text.startswith("remember my name is "):

            name = text[
                len("remember my name is "):
            ].strip()

        else:

            name = text[
                len("remember about my name is "):
            ].strip()


        if not name:

            speak_response(
                "What is your name?"
            )

            return True


        if remember("name", name):

            speak_response(
                f"Okay, I'll remember your name is {name}."
            )

        else:

            speak_response(
                "Sorry, I couldn't save your name."
            )

        return True

    # --------------------------------------------------------
    # FAVORITE SUBJECT
    # --------------------------------------------------------

    if text.startswith("remember my favorite subject is "):

        subject = text[
            len("remember my favorite subject is "):
        ].strip()

        if not subject:
            speak_response(
                "What is your favorite subject?"
            )
            return True

        if remember("favorite_subject", subject):

            speak_response(
                f"Okay, I'll remember that your favorite subject is {subject}."
            )

        else:

            speak_response(
                "Sorry, I couldn't save your favorite subject."
            )

        return True


    # --------------------------------------------------------
    # RECALL FAVORITE SUBJECT
    # --------------------------------------------------------

    if text in [
        "what is my favorite subject",
        "what's my favorite subject",
        "what is my favourite subject",
        "what's my favourite subject"
    ]:

        subject = recall("favorite_subject")

        if subject:

            speak_response(
                f"Your favorite subject is {subject}."
            )

        else:

            speak_response(
                "You haven't told me your favorite subject yet."
            )

        return True

    # --------------------------------------------------------
    # REMEMBER THAT...
    # --------------------------------------------------------

    if text.startswith("remember that "):

        information = text[
            len("remember that "):
        ].strip()


        if not information:

            speak_response(
                "What would you like me to remember?"
            )

            return True


        key = f"memory_{int(time.time())}"


        if remember(
            key,
            information
        ):

            speak_response(
                "Okay, I'll remember that."
            )

        else:

            speak_response(
                "Sorry, I couldn't save that memory."
            )

        return True


    # --------------------------------------------------------
    # REMEMBER...
    # --------------------------------------------------------

    if text.startswith("remember "):

        information = text[
            len("remember "):
        ].strip()


        # Avoid treating "remember my name is..."
        # as a generic memory.
        if information.startswith("my name is "):

            name = information[
                len("my name is "):
            ].strip()


            if name:

                if remember("name", name):

                    speak_response(
                        f"Okay, I'll remember your name is {name}."
                    )

                else:

                    speak_response(
                        "Sorry, I couldn't save your name."
                    )

            else:

                speak_response(
                    "What is your name?"
                )

            return True


        if information:

            key = f"memory_{int(time.time())}"


            if remember(
                key,
                information
            ):

                speak_response(
                    "Okay, I'll remember that."
                )

            else:

                speak_response(
                    "Sorry, I couldn't save that memory."
                )

            return True


    # --------------------------------------------------------
    # FORGET A SAVED MEMORY
    # --------------------------------------------------------

    if text.startswith("forget "):

        information = text[
            len("forget "):
        ].strip()


        memories = get_all_memories()

        found_key = None


        for key, value in memories.items():

            if information in str(value).lower():

                found_key = key

                break


        if found_key:

            if forget(found_key):

                speak_response(
                    "Okay, I've forgotten that."
                )

            else:

                speak_response(
                    "Sorry, I couldn't remove that memory."
                )

        else:

            speak_response(
                "I couldn't find that memory."
            )

        return True


    return False

# ============================================================
# TIME & DATE
# ============================================================

def handle_time_date(text):

    if text in [
        "what time is it",
        "what is the time",
        "tell me the time",
        "current time",
        "time"
    ]:
        current_time = time.strftime("%I:%M %p")
        speak_response(f"The time is {current_time}.")
        return True

    if text in [
        "what is today's date",
        "what is the date",
        "tell me the date",
        "today's date",
        "current date",
        "date"
    ]:
        current_date = time.strftime("%A, %d %B %Y")
        speak_response(f"Today is {current_date}.")
        return True

    return False

# ============================================================
# CONVERSATION
# ============================================================

def handle_conversation():

    while True:

        # ====================================================
        # LISTEN WITH AUTO-RETRY
        # ====================================================

        text = ""

        for attempt in range(2):

            text = listen_whisper()

            if text:
                break

            if attempt == 0:
                print("🔄 No speech detected — listening again...")

        if not text:
            continue

        text = (
            text
            .lower()
            .strip()
            .rstrip(".,!?")
        )

        # ==================================================
        # EXIT COMMANDS
        # ==================================================

        if text in [
            "exit",
            "quit",
            "goodbye",
            "good bye"
        ]:
            speak_response("Goodbye!")
            return True

        # ==================================================
        # SLEEP COMMANDS
        # ==================================================

        if text in [
            "sleep",
            "go to sleep",
            "stop listening",
            "be quiet"
        ]:
            speak_response("Going to sleep.")
            return False

        # ====================================================
        # TIME & DATE
        # ====================================================

        if handle_time_date(text):
            continue

        # ====================================================
        # NAME MEMORY
        # ====================================================

        if text.startswith(
            "remember my name is "
        ):

            name = text.replace(
                "remember my name is ",
                "",
                1
            ).strip()

            if remember(
                "name",
                name
            ):

                speak_response(
                    f"Okay, I'll remember your name is {name}."
                )

            else:

                speak_response(
                    "Sorry, I couldn't save your name."
                )

            continue

        if text == "what is my name":

            name = recall("name")

            if name:

                speak_response(
                    f"Your name is {name}."
                )

            else:

                speak_response(
                    "I don't know your name yet."
                )

            continue

        # ====================================================
        # SMART MEMORY
        # ====================================================

        if handle_memory(text):
            continue

        # ====================================================
        # COMPUTER COMMANDS
        # ====================================================

        reply = execute(text)

        if reply:

            speak_response(
                reply
            )

            continue

        # ====================================================
        # AI
        # ====================================================

        start_time = time.time()

        reply = ask_ai(text)

        print(
            f"AI response time: "
            f"{time.time() - start_time:.2f} seconds"
        )

        if reply:

            speak_response(
                reply
            )

        else:

            speak_response(
                "Sorry, I couldn't generate a response."
            )

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("Nispara is ready!")

    while True:
        wait_for_wake_word(model, mic_device=MIC_DEVICE)

        speak_response("Yes?")

        time.sleep(0.3)

        should_exit = handle_conversation()

        if should_exit:
            break