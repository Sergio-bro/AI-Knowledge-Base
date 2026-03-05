# 🤖 Company Knowledge Slack Bot

A Slack bot that answers employee questions using your company knowledge base.
Powered by **Claude AI** (Anthropic) + **Firebase** + **Render**.

---

## How It Works

1. Employee types `@YourBot what are our restricted countries?` in Slack
2. Bot fetches company knowledge from Firebase
3. Claude reads the knowledge and generates an accurate answer
4. Bot replies in the same thread ✅

---

## Setup — Step by Step

### STEP 1 — Create the Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name it (e.g. `Company Assistant`) and pick your workspace
4. Go to **"OAuth & Permissions"** → scroll to **"Bot Token Scopes"** → add:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
5. Click **"Install to Workspace"** → copy the **Bot User OAuth Token** (`xoxb-...`)
6. Go to **"Basic Information"** → copy the **Signing Secret**

---

### STEP 2 — Create Firebase Project

1. Go to [https://console.firebase.google.com](https://console.firebase.google.com)
2. Click **"Add project"** → follow the steps (no need to enable Analytics)
3. In your project, go to **"Build"** → **"Firestore Database"** → **"Create database"**
   - Choose **"Start in production mode"** → pick a region → Done
4. Go to **"Project Settings"** (gear icon) → **"Service accounts"**
5. Click **"Generate new private key"** → download the JSON file
6. Save this file as `firebase-credentials.json` in this folder (for running `upload_docs.py` locally)

---

### STEP 3 — Upload Your Company Knowledge

1. Open `upload_docs.py`
2. Fill in your company information in the `COMPANY_KNOWLEDGE` list
3. Run the script:
   ```bash
   pip install firebase-admin
   python upload_docs.py
   ```
4. You should see ✅ for each topic uploaded

> You can run this anytime to update the knowledge base — no need to redeploy the bot.

---

### STEP 4 — Deploy to Render

1. Push this folder to a **GitHub repository**
2. Go to [https://render.com](https://render.com) → **"New Web Service"**
3. Connect your GitHub repo
4. Configure the service:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:flask_app`
   - **Plan**: Starter ($7/month) — needed so it doesn't sleep
5. Add these **Environment Variables**:

   | Variable | Value |
   |---|---|
   | `SLACK_BOT_TOKEN` | Your bot token (`xoxb-...`) |
   | `SLACK_SIGNING_SECRET` | Your signing secret |
   | `ANTHROPIC_API_KEY` | Your Claude API key from console.anthropic.com |
   | `FIREBASE_CREDENTIALS` | Paste the **entire contents** of your `firebase-credentials.json` file |

6. Click **"Create Web Service"** → wait for it to deploy
7. Copy your Render URL (e.g. `https://your-bot.onrender.com`)

---

### STEP 5 — Connect Slack to Render

1. Back in your Slack app settings → **"Event Subscriptions"**
2. Toggle **"Enable Events"** → ON
3. Paste your Render URL + `/slack/events`:
   ```
   https://your-bot.onrender.com/slack/events
   ```
4. Slack will verify the URL (your bot must be deployed and running)
5. Under **"Subscribe to bot events"** → add: `app_mention`
6. Click **"Save Changes"**

---

### STEP 6 — Test It!

1. Go to your Slack workspace
2. Create a channel called **"Ask Anything"** (or any name)
3. Invite the bot: `/invite @YourBot`
4. Type: `@YourBot what are our restricted countries?`
5. The bot should reply in the thread 🎉

---

## Updating the Knowledge Base

To add or change company info, just edit `upload_docs.py` and run it again:
```bash
python upload_docs.py
```
No need to redeploy the bot. Changes take effect immediately.

---

## Cost Estimate

| Service | Cost |
|---|---|
| Claude API (Haiku model) | ~$0.002 per question |
| Render Starter | $7/month |
| Firebase Spark | Free |
| Slack | Free |

**For testing with $5 on Claude console → ~2,000 questions** ✅

---

## Troubleshooting

**Bot doesn't respond:**
- Check Render logs for errors
- Make sure the bot is invited to the channel
- Verify event subscriptions are saved in Slack

**Knowledge base empty error:**
- Run `upload_docs.py` again
- Check Firebase Console → Firestore → `knowledge_base` collection

**Firebase credentials error:**
- Make sure the full JSON is pasted as the `FIREBASE_CREDENTIALS` env variable (including the `{}` curly braces)
