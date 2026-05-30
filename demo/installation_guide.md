# LiveKit Voice Agent - Detailed Installation Guide

This guide provides step-by-step instructions for setting up the LiveKit Voice Agent Integration project.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.8 or higher** installed
2. **pip** (Python package manager)
3. **git** for version control
4. A **LiveKit account** (cloud or self-hosted)
5. A **webhook endpoint** for testing

## Step 1: Clone the Repository

```bash
git clone https://github.com/vaibhav410/LiveKit-Voice-Agent-Integration.git
cd LiveKit-Voice-Agent-Integration
```

## Step 2: Create a Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Edit the `.env` file with your configuration:

```env
# LiveKit Configuration
LIVEKIT_URL=https://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Webhook Configuration
WEBHOOK_URL=https://webhook.site/your-unique-url

# Agent Configuration
PARTICIPANT_NAME=AI Assistant
ROOM_NAME=voice-agent-room
```

### Getting LiveKit Credentials

1. Visit [LiveKit Cloud Console](https://cloud.livekit.io)
2. Create a new project or select an existing one
3. Go to Settings → API Keys
4. Create a new API key
5. Copy the URL, API Key, and API Secret to your `.env` file

### Setting Up a Test Webhook

1. Visit [webhook.site](https://webhook.site)
2. Copy the unique URL provided
3. Paste it as `WEBHOOK_URL` in your `.env` file

## Step 5: Run the Agent

```bash
python voice_agent.py
```

## Expected Output

```
============================================================
🤖 LiveKit Voice Agent Integration
   Earthonoid AI - Internship Assignment
============================================================

🎤 Assistant: Hello, welcome to Earthonoid AI. I'm your AI Voice Assistant.
🎤 Assistant: What is your name?
👤 You: [Enter your name]
🎤 Assistant: What is your requirement or problem you'd like to solve?
👤 You: [Enter your requirement]

🎤 Assistant: Thank you. Your information has been submitted successfully.

============================================================
✓ SESSION SUMMARY
============================================================
Name: [Your Name]
Requirement: [Your Requirement]
Status: ✓ Success
============================================================
```

## Troubleshooting

### Issue: Module not found

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Environment variables not loading

```bash
# Ensure python-dotenv is installed
pip install python-dotenv

# Verify .env file exists in project root
ls -la .env
```

### Issue: Webhook connection failed

1. Verify your webhook URL is correct
2. Check internet connectivity
3. Try using webhook.site for testing

## Next Steps

- Review the main [README.md](../README.md) for detailed documentation
- Check out the sample conversation in `demo/sample_conversation.txt`
- Explore the session data saved in the `sessions/` directory