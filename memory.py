import json
import os


# ============================================================
# SETTINGS
# ============================================================

FILE = "memory.json"


# ============================================================
# LOAD MEMORY
# ============================================================

def load_memory():

    if not os.path.exists(FILE):
        return {}

    try:

        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if isinstance(data, dict):
            return data

        print("⚠️ Memory file format is invalid.")
        return {}

    except json.JSONDecodeError:

        print("⚠️ Memory file is corrupted.")
        return {}

    except Exception as e:

        print(
            "❌ Could not load memory:",
            type(e).__name__,
            "-",
            e
        )

        return {}


# ============================================================
# SAVE MEMORY
# ============================================================

def save_memory(data):

    try:

        with open(
            FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        print(
            "❌ Could not save memory:",
            type(e).__name__,
            "-",
            e
        )

        return False


# ============================================================
# MEMORY
# ============================================================

memory = load_memory()


# ============================================================
# REMEMBER
# ============================================================

def remember(key, value):

    key = str(key).strip()
    value = str(value).strip()

    if not key or not value:

        print("⚠️ Cannot save empty memory.")
        return False

    memory[key] = value

    return save_memory(memory)


# ============================================================
# RECALL
# ============================================================

def recall(key):

    return memory.get(key)


# ============================================================
# FORGET
# ============================================================

def forget(key):

    if key not in memory:

        return False

    del memory[key]

    return save_memory(memory)


# ============================================================
# GET ALL MEMORIES
# ============================================================

def get_all_memories():

    return memory.copy()