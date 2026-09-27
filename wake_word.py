def wait_for_wake_word(model, mic_device=None):
    import json
    import queue
    import sounddevice as sd
    from vosk import KaldiRecognizer
    SAMPLE_RATE = 16000
    MIC_DEVICE = mic_device
    q = queue.Queue()
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    def callback(indata, frames, time_info, status):
        if status:
            print("Audio status:", status)

        q.put(bytes(indata))

    print("😴 Sleeping... Say 'Max'.")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        dtype="int16",
        channels=1,
        device=MIC_DEVICE,
        callback=callback,
    ):
        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip().lower()

                if text:
                    print("Heard:", text)

                    # Wake only when Max is the final word
                    if text == "max" or text.endswith(" max"):
                        print("🟢 Wake word detected!")
                        return