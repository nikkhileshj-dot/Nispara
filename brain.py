from groq import Groq
from config import GROQ_API_KEY


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation = [
    {
        "role": "system",
        "content": (
            "You are Nispara, a friendly personal AI assistant. "
            "Speak naturally and conversationally. "
            "Keep responses concise unless the user asks for details. "
            "Always finish your answer completely. "
            "Do not stop in the middle of a sentence. "
            "Remember the current conversation and understand follow-up questions. "
            "If the user refers to something with words like 'it', 'that', "
            "'there', 'the first one', or 'the previous one', use the conversation "
            "context to understand what they mean. "
            "Do not repeatedly introduce yourself. "
            "Do not invent real-time information. "
            "Be helpful, natural and concise."
        )
    }
]


# ============================================================
# AI RESPONSE
# ============================================================

def ask_ai(user_input):

    # Add user's message
    conversation.append({
        "role": "user",
        "content": user_input
    })

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=conversation,
            temperature=0.5,
            max_tokens=300
        )

        # Safely get response
        if not response.choices:

            print("❌ Groq returned no response.")

            conversation.pop()

            return (
                "Sorry, I didn't get a response from the AI."
            )

        reply = response.choices[0].message.content

        if not reply:

            print("❌ Groq returned an empty response.")

            conversation.pop()

            return (
                "Sorry, I received an empty response."
            )

        # Add AI response to conversation
        conversation.append({
            "role": "assistant",
            "content": reply
        })

        # Keep system message + last 8 conversation pairs
        if len(conversation) > 17:

            conversation[:] = (
                [conversation[0]]
                + conversation[-16:]
            )

        return reply.strip()


    # ========================================================
    # API / NETWORK ERROR
    # ========================================================

    except Exception as e:

        print(
            "❌ Groq error:",
            type(e).__name__,
            "-",
            e
        )

        # Remove failed user message
        if (
            conversation
            and conversation[-1]["role"] == "user"
        ):
            conversation.pop()

        return (
            "Sorry, I'm having trouble connecting "
            "to my AI service right now."
        )