import os
import time
import wave
import tempfile

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

print("Loading Whisper Base model...")

model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8",
    cpu_threads=8,
    num_workers=1
)

print("✅ Whisper Base loaded!")

# ==================================================

# MICROPHONE SETTINGS

# ==================================================

SAMPLE_RATE = 16000
MIC_DEVICE = 1

BLOCK_DURATION = 0.1
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

# ==================================================

# SPEECH DETECTION SETTINGS

# ==================================================

SILENCE_DURATION = 0.55
MAX_DURATION = 6

CALIBRATION_TIME = 0.3

PRE_ROLL_DURATION = 0.25
THRESHOLD_MULTIPLIER = 1.8
MIN_THRESHOLD = 180
MAX_THRESHOLD = 500

# ==================================================

# DEBUG RECORDING

# ==================================================

# Temporary debugging only.

# Set to False when debugging is finished.

DEBUG_RECORDING = False

DEBUG_FOLDER = "debug_audio"

# ==================================================

# LISTEN

# ==================================================

def listen_whisper():

    print("🎤 Listening...")

    total_start = time.time()

    audio_data = []

    # ==================================================
    # 1. CALIBRATE BACKGROUND NOISE
    # ==================================================

    calibration_data = []

    def calibration_callback(
        indata,
        frames,
        time_info,
        status
    ):

        if status:
            print(
                "⚠️ Audio status:",
                status
            )

        calibration_data.append(
            indata.copy()
        )

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            device=MIC_DEVICE,
            blocksize=BLOCK_SIZE,
            callback=calibration_callback
        ):

            time.sleep(CALIBRATION_TIME)

    except Exception as e:

        print(
            "❌ Microphone calibration error:",
            type(e).__name__,
            "-",
            e
        )

    if calibration_data:

        calibration_audio = np.concatenate(
            calibration_data,
            axis=0
        )

        noise_level = np.sqrt(
            np.mean(
                calibration_audio.astype(
                    np.float32
                ) ** 2
            )
        )

    else:

        noise_level = 300

    # ==================================================
    # 2. ADAPTIVE SILENCE THRESHOLD
    # ==================================================

    silence_threshold = min(
        650,
        max(
            500,
            noise_level * 2.5
        )
    )

    print(
        f"🎚️ Noise: {noise_level:.0f} | "
        f"Threshold: {silence_threshold:.0f}"
    )

    # ==================================================
    # 3. RECORD SPEECH
    # ==================================================

    speech_started = False
    silence_start = None

    start_time = time.time()

    # Ensure the recording buffer exists in this scope before the
    # callback and the main recording loop use it.
    audio_data = []

    def callback(
        indata,
        frames,
        time_info,
        status
    ):

        if status:

            print(
                "⚠️ Audio status:",
                status
            )

        audio_data.append(
            indata.copy()
        )

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            device=MIC_DEVICE,
            blocksize=BLOCK_SIZE,
            callback=callback
        ):

            while True:

                time.sleep(0.03)

                if not audio_data:
                    continue

                chunk = audio_data[-1]

                volume = np.sqrt(
                    np.mean(
                        chunk.astype(
                            np.float32
                        ) ** 2
                    )
                )

                # ------------------------------------------
                # SPEECH DETECTED
                # ------------------------------------------

                if volume > silence_threshold:

                    speech_started = True
                    silence_start = None

                # ------------------------------------------
                # SILENCE AFTER SPEECH
                # ------------------------------------------

                elif speech_started:

                    if silence_start is None:

                        silence_start = time.time()

                    elif (
                        time.time() - silence_start
                        >= SILENCE_DURATION
                    ):

                        break

                # ------------------------------------------
                # MAXIMUM RECORDING TIME
                # ------------------------------------------

                if (
                    time.time() - start_time
                    >= MAX_DURATION
                ):

                    break

    except Exception as e:

        print(
            "❌ Microphone recording error:",
            type(e).__name__,
            "-",
            e
        )

        return ""

    recording_time = time.time() - start_time

    print(
        f"🎤 Recording: {recording_time:.2f}s"
    )

    # ==================================================
    # 4. CHECK AUDIO
    # ==================================================

    if not audio_data:

        print(
            "⚠️ No audio was captured."
        )

        return ""

    # ==================================================
    # 5. COMBINE AUDIO
    # ==================================================

    try:

        audio = np.concatenate(
            audio_data,
            axis=0
        )

    except Exception as e:

        print(
            "❌ Audio processing error:",
            type(e).__name__,
            "-",
            e
        )

        return ""

    # ==================================================
    # 6. TEMP WAV
    # ==================================================

    filename = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            filename = temp.name

        with wave.open(
            filename,
            "wb"
        ) as wf:

            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)

            wf.writeframes(
                audio.tobytes()
            )

        # ==================================================
        # 6.5 DEBUG AUDIO SAVE
        # ==================================================

        if DEBUG_RECORDING:

            try:

                os.makedirs(
                    DEBUG_FOLDER,
                    exist_ok=True
                )

                timestamp = time.strftime(
                    "%Y%m%d_%H%M%S"
                )

                debug_filename = os.path.join(
                    DEBUG_FOLDER,
                    f"whisper_debug_{timestamp}.wav"
                )

                with wave.open(
                    debug_filename,
                    "wb"
                ) as debug_wav:

                    debug_wav.setnchannels(1)
                    debug_wav.setsampwidth(2)
                    debug_wav.setframerate(SAMPLE_RATE)

                    debug_wav.writeframes(
                        audio.tobytes()
                    )

                print(
                    f"💾 Debug audio saved: "
                    f"{debug_filename}"
                )

            except Exception as e:

                print(
                    "⚠️ Could not save debug audio:",
                    type(e).__name__,
                    "-",
                    e
                )

        # ==================================================
        # 7. WHISPER
        # ==================================================

        whisper_start = time.time()

        try:

            segments, info = model.transcribe(
                filename,
                language="en",

                beam_size=1,
                best_of=1,
                temperature=0,

                vad_filter=False,

                condition_on_previous_text=False
            )

            # Whisper transcription is lazy.
            # Processing happens while
            # iterating through segments.

            text = " ".join(
                segment.text
                for segment in segments
            ).strip()

        except Exception as e:

            print(
                "❌ Whisper error:",
                type(e).__name__,
                "-",
                e
            )

            return ""

        whisper_time = (
            time.time() - whisper_start
        )

        print(
            f"🧠 Whisper: "
            f"{whisper_time:.2f}s"
        )

        # ==================================================
        # 8. RESULT
        # ==================================================

        if text:

            print(
                "You:",
                text
            )

        else:

            print(
                "⚠️ Whisper detected no speech."
            )

        print(
            f"⚡ Total listening: "
            f"{time.time() - total_start:.2f}s"
        )

        result = text.lower()

    except Exception as e:

        print(
            "❌ Temp WAV / Whisper setup error:",
            type(e).__name__,
            "-",
            e
        )

        return ""

    # ==================================================
    # 9. DELETE TEMP WHISPER WAV
    # ==================================================

    if (
        filename
        and os.path.exists(filename)
    ):

        try:

            os.remove(filename)

        except Exception:

            pass

    return result