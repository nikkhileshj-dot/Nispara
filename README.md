# 🤖 Nispara

Nispara is a personal AI voice assistant built with Python.

It uses voice recognition, speech synthesis, AI responses, memory, and Windows automation to provide a hands-free assistant experience.

## ✨ Features

- 🎙️ Voice-controlled interaction
- 🟢 Wake word detection using Vosk
- 🧠 Speech-to-text using Faster-Whisper
- 💬 AI conversations using Groq
- 🔊 Natural text-to-speech using Edge TTS
- 🧠 Simple persistent memory
- 🌐 Web search
- 🔎 Google and Chrome search
- ▶️ YouTube search
- 📸 Camera control
- 📷 Screenshot capture
- 📝 Open Notepad
- 🧮 Open Calculator
- 🎨 Open Paint
- 📁 Open File Explorer
- 💻 Open Command Prompt
- 🌐 Browser navigation
- 🔄 Refresh browser
- ❌ Close browser
- ⏰ Reminders
- 🔋 Battery information
- 🖥️ System information
- 🛑 Voice interruption / barge-in

## 🛠️ Technologies

- Python
- Faster-Whisper
- Vosk
- Groq API
- Edge TTS
- SoundDevice
- Pygame
- OpenCV
- PyAutoGUI

## 📁 Project Structure

```text
NISPARA/
│
├── app.py
├── brain.py
├── commands.py
├── memory.py
├── speech.py
├── whisper_listener.py
├── wake_word.py
├── listener.py
│
├── camera.py
├── battery.py
├── screenshot.py
├── system_info.py
├── reminder.py
├── web_search.py
│
├── requirements.txt
├── README.md
└── .gitignore