import os
import json
import logging
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import anthropic
import firebase_admin
from firebase_admin import credentials, firestore

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Slack ─────────────────────────────────────────────────────────────────────
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# ── Firebase ──────────────────────────────────────────────────────────────────
firebase_creds = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

# ── Anthropic ─────────────────────────────────────────────────────────────────
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful internal company assistant.
Your job is to answer employee questions using the company knowledge base provided.

RULES:
- Only answer based on the company knowledge provided below
- If the answer is not in the knowledge base, say exactly: "I don't have that information in my knowledge base. Please contact HR or your manager for this."
- Be professional, clear, and concise
- If a question is about sensitive topics (financials, legal, HR), always add: "Please also verify this with the relevant team."
- Never make up information that is not in the knowledge base"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_company_knowledge() -> str:
    """Fetch all company knowledge documents from Firebase."""
    try:
        docs = db.collection("knowledge_base").stream()
        parts = []
        for doc in docs:
            data = doc.to_dict()
            topic = data.get("topic", doc.id)
            content = data.get("content", "")
            parts.append(f"### {topic}\n{content}")
        return "\n\n".join(parts)
    except Exception as e:
        logger.error(f"Firebase error: {e}")
        return ""


def ask_claude(question: str, knowledge: str) -> str:
    """Send question + company knowledge to Claude and return the answer."""
    try:
        response = claude.messages.create(
            model="claude-haiku-4-5-20251001",   # Cheapest + fastest model
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"COMPANY KNOWLEDGE BASE:\n\n{knowledge}\n\n"
                        f"---\n\nEMPLOYEE QUESTION:\n{question}"
                    )
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return "Sorry, I encountered an error. Please try again in a moment."


# ── Slack Event Handler ───────────────────────────────────────────────────────

@app.event("app_mention")
def handle_mention(event, say, client):
    """Triggered whenever someone @mentions the bot in any channel."""
    try:
        thread_ts = event.get("thread_ts", event["ts"])

        # Strip the @mention from the question
        bot_user_id = client.auth_test()["user_id"]
        question = event["text"].replace(f"<@{bot_user_id}>", "").strip()

        if not question:
            say(text="Hi! Ask me anything about the company 👋", thread_ts=thread_ts)
            return

        # Fetch company knowledge from Firebase
        knowledge = get_company_knowledge()
        if not knowledge:
            say(
                text="⚠️ The knowledge base is empty. Please ask the admin to upload company documents.",
                thread_ts=thread_ts
            )
            return

        # Get Claude's answer
        answer = ask_claude(question, knowledge)

        # Reply inside the same thread
        say(text=answer, thread_ts=thread_ts)

    except Exception as e:
        logger.error(f"Error handling mention: {e}")
        say(text="Something went wrong. Please try again.", thread_ts=event["ts"])


# ── Flask Routes ──────────────────────────────────────────────────────────────

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}, 200


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    flask_app.run(port=int(os.environ.get("PORT", 3000)))
