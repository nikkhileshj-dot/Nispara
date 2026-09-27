from vosk import Model

MODEL_PATH = "vosk-model-small-en-us-0.15"

print("Loading Vosk model...")
model = Model(MODEL_PATH)
print("✅ Vosk model loaded!")