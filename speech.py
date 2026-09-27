import asyncio
import edge_tts
import pygame
import os
import tempfile
import json
import queue
import threading
import sounddevice as sd
from vosk import KaldiRecognizer


VOICE = "en-US-GuyNeural"

# Keeps track of whether NISPARA is currently speaking
speaking = False


# ============================================================
# STOP SPEAKING
# ============================================================

def stop_speaking():

    global speaking

    try:

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    except Exception as e:

        print(
            "⚠️ Could not stop speech:",
            type(e).__name__,
            "-",
            e
        )

    finally:

        speaking = False


# ============================================================
# INTERRUPTION MONITOR
# ============================================================

def monitor_interrupt(model, mic_device, stop_event):

    SAMPLE_RATE = 16000
    q = queue.Queue()

    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )

    def callback(indata, frames, time_info, status):

        if status:
            print(
                "⚠️ Interrupt audio status:",
                status
            )

        q.put(bytes(indata))

    try:

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=4000,
            dtype="int16",
            channels=1,
            device=mic_device,
            callback=callback
        ):

            print("🎧 Interruption monitor active.")

            while not stop_event.is_set():

                try:
                    data = q.get(timeout=0.1)

                except queue.Empty:
                    continue

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get(
                        "text",
                        ""
                    ).strip().lower()

                    if not text:
                        continue

                    print(
                        "🔊 While speaking:",
                        text
                    )

                    # Only accept an actual wake word
                    words = text.split()

                    if (
                        text == "max"
                        or (
                            words
                            and words[-1] == "max"
                        )
                    ):

                        print(
                            "🛑 Interruption detected!"
                        )

                        stop_speaking()

                        stop_event.set()

                        return

    except Exception as e:

        print(
            "⚠️ Interrupt monitor error:",
            type(e).__name__,
            "-",
            e
        )


# ============================================================
# SPEAK
# ============================================================

def speak(text, wake_model=None, mic_device=None):

    global speaking

    if not text or not text.strip():

        print("⚠️ Nothing to speak.")

        return

    print("NISPARA:", text)

    speaking = True

    stop_event = threading.Event()

    interrupt_thread = None

    try:

        # ----------------------------------------------------
        # START INTERRUPTION MONITOR
        # ----------------------------------------------------

        if wake_model is not None and mic_device is not None:

            interrupt_thread = threading.Thread(
                target=monitor_interrupt,
                args=(
                    wake_model,
                    mic_device,
                    stop_event
                ),
                daemon=True
            )

            interrupt_thread.start()

        # ----------------------------------------------------
        # SPEAK
        # ----------------------------------------------------

        asyncio.run(
            _speak(
                text,
                stop_event
            )
        )

    except Exception as e:

        print(
            "❌ Speech error:",
            type(e).__name__,
            "-",
            e
        )

    finally:

        speaking = False

        stop_event.set()

        if interrupt_thread:

            interrupt_thread.join(
                timeout=0.5
            )


# ============================================================
# EDGE TTS
# ============================================================

async def _speak(text, stop_event):

    filename = None

    try:

        # ----------------------------------------------------
        # CREATE TEMP MP3
        # ----------------------------------------------------

        try:

            with tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            ) as temp:

                filename = temp.name

        except Exception as e:

            print(
                "❌ Could not create speech file:",
                type(e).__name__,
                "-",
                e
            )

            return

        # ----------------------------------------------------
        # GENERATE SPEECH
        # ----------------------------------------------------

        try:

            communicate = edge_tts.Communicate(
                text,
                VOICE
            )

            await communicate.save(
                filename
            )

        except Exception as e:

            print(
                "❌ Edge TTS error:",
                type(e).__name__,
                "-",
                e
            )

            return

        # ----------------------------------------------------
        # INITIALIZE AUDIO
        # ----------------------------------------------------

        try:

            if not pygame.mixer.get_init():
                pygame.mixer.init()

        except Exception as e:

            print(
                "❌ Audio initialization error:",
                type(e).__name__,
                "-",
                e
            )

            return

        # ----------------------------------------------------
        # LOAD AUDIO
        # ----------------------------------------------------

        try:

            pygame.mixer.music.load(
                filename
            )

        except Exception as e:

            print(
                "❌ Audio loading error:",
                type(e).__name__,
                "-",
                e
            )

            return

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        try:

            pygame.mixer.music.play()

        except Exception as e:

            print(
                "❌ Audio playback error:",
                type(e).__name__,
                "-",
                e
            )

            return

        # ----------------------------------------------------
        # WAIT WHILE PLAYING
        # ----------------------------------------------------

        while pygame.mixer.music.get_busy():

            # Stop waiting immediately after interruption
            if stop_event.is_set():

                pygame.mixer.music.stop()

                break

            await asyncio.sleep(
                0.05
            )

    except Exception as e:

        print(
            "❌ Unexpected speech error:",
            type(e).__name__,
            "-",
            e
        )

    finally:

        # ----------------------------------------------------
        # STOP AUDIO
        # ----------------------------------------------------

        try:

            if pygame.mixer.get_init():

                pygame.mixer.music.stop()

                pygame.mixer.quit()

        except Exception as e:

            print(
                "⚠️ Audio cleanup error:",
                type(e).__name__,
                "-",
                e
            )

        # ----------------------------------------------------
        # DELETE TEMP FILE
        # ----------------------------------------------------

        if (
            filename
            and os.path.exists(filename)
        ):

            try:

                os.remove(filename)

            except Exception as e:

                print(
                    "⚠️ Could not delete "
                    "temporary speech file:",
                    e
                )