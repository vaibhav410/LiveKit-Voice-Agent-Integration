# LiveKit Voice Agent Integration

A complete AI Voice Assistant implementation using LiveKit that collects user information through voice conversation and submits it to a webhook endpoint. This project is designed as an internship assignment for Earthonoid AI.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Agent](#running-the-agent)
- [Webhook Setup](#webhook-setup)
- [Example Output](#example-output)
- [Conversation Flow](#conversation-flow)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Technologies Used](#technologies-used)
- [Assignment Requirements](#assignment-requirements)
- [Future Enhancements](#future-enhancements)

## Project Overview

This project implements a basic AI Voice Assistant using LiveKit that:

1. **Greets the user** with a welcome message
2. **Collects user's name** through voice input (speech-to-text)
3. **Collects user's requirement/problem** through voice input
4. **Stores the information** in memory during the session
5. **Sends data to webhook** in JSON format
6. **Confirms submission** with a success message

The agent uses:
- **LiveKit**: For real-time voice communication
- **Google Cloud STT/TTS**: For speech-to-text and text-to-speech conversion
- **Silero**: For voice activity detection
- **Python**: For core implementation
- **Requests library**: For webhook communication

## Features

✅ Voice-based user interaction (no typing required)  
✅ Automated conversation flow  
✅ Real-time speech-to-text transcription  
✅ Natural text-to-speech responses  
✅ Webhook integration for data submission  
✅ Environment variable configuration  
✅ Comprehensive error handling  
✅ Detailed logging and debugging  
✅ JSON payload transmission  
✅ Session management  

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Voice Input                     │
│                   (Microphone Audio)                    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  LiveKit Voice Agent                    │
│         (Real-time Audio Communication)                │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Google STT   │ │ Voice Agent  │ │ Google TTS   │
│ (Speech-to-  │ │ Logic        │ │ (Text-to-    │
│  Text)       │ │              │ │  Speech)     │
└──────────────┘ └──────────────┘ └──────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│            Data Collection & Processing                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 1: Collect Name via Speech-to-Text        │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 2: Collect Requirement via Speech-to-Text │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Step 3: Store Information in Session Variables │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              JSON Payload Creation                      │
│  {                                                      │
│    "name": "Vaibhav",                                  │
│    "requirement": "AI Automation"                      │
│  }                                                      │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│          Webhook Submission (HTTP POST)                 │
│        requests.post(WEBHOOK_URL, json=payload)        │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│           Confirmation Message to User                  │
│  "Thank you. Your information has been submitted       │
│   successfully."                                        │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **git** (for version control)
- **A LiveKit Server** (Cloud or self-hosted)
- **Google Cloud Account** (for STT/TTS)
- **Webhook endpoint** (for receiving data)

### Account Setup

1. **LiveKit Account**: Sign up at [LiveKit.io](https://livekit.io)
2. **Google Cloud**: Set up a project and enable Speech-to-Text and Text-to-Speech APIs
3. **Webhook Service**: Use [webhook.site](https://webhook.site) for testing

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/vaibhav410/LiveKit-Voice-Agent-Integration.git
cd LiveKit-Voice-Agent-Integration
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your actual configuration:

```
# LiveKit Configuration
LIVEKIT_URL=https://your-livekit-url
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Webhook Configuration
WEBHOOK_URL=https://webhook.site/your-unique-url

# Agent Configuration
PARTICIPANT_NAME=AI Assistant
ROOM_NAME=voice-agent-room
```

## Configuration

### LiveKit Setup

1. Visit [LiveKit Cloud Console](https://cloud.livekit.io)
2. Create a new project
3. Generate API credentials
4. Add credentials to `.env` file

### Google Cloud Setup

1. Create a Google Cloud project
2. Enable Speech-to-Text API
3. Enable Text-to-Speech API
4. Create a service account
5. Download the service account key JSON
6. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
# On Windows
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json

# On macOS/Linux
export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### Webhook Setup

For testing, use [webhook.site](https://webhook.site):

1. Visit https://webhook.site
2. Copy your unique webhook URL
3. Add it to the `.env` file as `WEBHOOK_URL`
4. The agent will send JSON data to this URL

## Running the Agent

### Basic Execution

```bash
python voice_agent.py
```

### With Verbose Logging

```bash
python voice_agent.py --verbose
```

### Expected Console Output

```
============================================================
LiveKit Voice Agent Integration - Earthonoid AI
============================================================
Starting voice agent...

2024-01-15 10:30:45 - __main__ - INFO - All required environment variables are configured
2024-01-15 10:30:45 - __main__ - INFO - Prewarmed Text-to-Speech
2024-01-15 10:30:45 - __main__ - INFO - Prewarmed Voice Activity Detection
2024-01-15 10:30:46 - __main__ - INFO - Starting voice agent conversation
2024-01-15 10:30:46 - __main__ - INFO - Step 1: Greeting user
2024-01-15 10:30:46 - __main__ - INFO - Assistant: Hello, welcome to Earthonoid AI. I'm your AI Voice Assistant.
2024-01-15 10:30:47 - __main__ - INFO - Step 2: Asking for user's name
2024-01-15 10:30:47 - __main__ - INFO - Assistant: What is your name?
2024-01-15 10:30:50 - __main__ - INFO - User Input - Name: Vaibhav
2024-01-15 10:30:50 - __main__ - INFO - Step 3: Asking for user's requirement
2024-01-15 10:30:50 - __main__ - INFO - Assistant: What is your requirement or problem you'd like to solve?
2024-01-15 10:30:55 - __main__ - INFO - User Input - Requirement: AI Automation
2024-01-15 10:30:55 - __main__ - INFO - Step 4: Sending data to webhook
2024-01-15 10:30:55 - __main__ - INFO - Sending webhook payload: {"name": "Vaibhav", "requirement": "AI Automation"}
2024-01-15 10:30:56 - __main__ - INFO - Webhook submitted successfully. Status: 200
2024-01-15 10:30:56 - __main__ - INFO - Step 5: Confirm submission status
2024-01-15 10:30:56 - __main__ - INFO - Assistant: Thank you. Your information has been submitted successfully.
2024-01-15 10:30:56 - __main__ - INFO - ============================================================
2024-01-15 10:30:56 - __main__ - INFO - SESSION SUMMARY
2024-01-15 10:30:56 - __main__ - INFO - ============================================================
2024-01-15 10:30:56 - __main__ - INFO - User Name: Vaibhav
2024-01-15 10:30:56 - __main__ - INFO - User Requirement: AI Automation
2024-01-15 10:30:56 - __main__ - INFO - ============================================================

============================================================
CONVERSATION SUMMARY
============================================================
User Name: Vaibhav
User Requirement: AI Automation
Webhook URL: https://webhook.site/your-unique-url
Submission Status: Success
============================================================
```

## Webhook Setup

### Using webhook.site

1. Visit [webhook.site](https://webhook.site)
2. Copy the unique URL provided
3. Add it to your `.env` file

### Expected Webhook Payload

When the agent successfully collects information, it sends a JSON POST request:

**Endpoint**: `POST` to your webhook URL

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Vaibhav",
  "requirement": "AI Automation"
}
```

**Expected Response**: HTTP 200 OK

### Custom Webhook Server (Optional)

You can also set up a custom webhook server using FastAPI:

```python
from fastapi import FastAPI
import uvicorn
import json

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(payload: dict):
    """Receive webhook from voice agent"""
    print(f"Received: {json.dumps(payload, indent=2)}")
    return {"status": "success", "message": "Data received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with:
```bash
python webhook_server.py
```

Then set `WEBHOOK_URL=http://localhost:8000/webhook`

## Example Output

### Console Output

```
============================================================
CONVERSATION SUMMARY
============================================================
User Name: Vaibhav
User Requirement: AI Automation
Webhook URL: https://webhook.site/a1b2c3d4-e5f6-7890-abcd-ef1234567890
Submission Status: Success
============================================================
```

### Webhook Request

```bash
curl -X POST https://webhook.site/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "Content-Type: application/json" \
  -d '{"name": "Vaibhav", "requirement": "AI Automation"}'
```

### Webhook Response (webhook.site)

The webhook.site interface will display:
- **Request Method**: POST
- **Headers**: Content-Type: application/json
- **Body**: `{"name": "Vaibhav", "requirement": "AI Automation"}`
- **Timestamp**: 2024-01-15 10:30:56 UTC

## Conversation Flow

### Expected Conversation

```
VOICE AGENT:    Hello, welcome to Earthonoid AI. I'm your AI Voice Assistant.

VOICE AGENT:    What is your name?

USER:           Vaibhav

VOICE AGENT:    What is your requirement or problem you'd like to solve?

USER:           AI Automation

VOICE AGENT:    Thank you. Your information has been submitted successfully.
```

### Conversation Stages

| Stage | Agent Action | Timeout | Error Handling |
|-------|-------------|---------|-----------------|
| Greeting | TTS message | N/A | Continue |
| Name Request | TTS + STT | 30s | Retry |
| Requirement Request | TTS + STT | 30s | Retry |
| Webhook Submit | HTTP POST | 10s | Notify user |
| Confirmation | TTS message | N/A | Log error |

## Project Structure

```
LiveKit-Voice-Agent-Integration/
│
├── voice_agent.py                 # Main voice agent implementation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .env                           # Local environment variables (git-ignored)
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore rules
│
├── screenshots/                   # Screenshots directory
│   ├── webhook_output.png        # Sample webhook output
│   ├── console_output.png        # Console execution output
│   └── setup_guide.png           # Setup instructions
│
└── demo/                          # Demo files and samples
    ├── sample_conversation.txt   # Sample conversation transcript
    ├── webhook_payload.json      # Sample webhook payload
    └── installation_guide.md     # Detailed installation guide
```

## Troubleshooting

### Issue: Missing Environment Variables

**Error**: `ValueError: Missing environment variables: LIVEKIT_URL, ...`

**Solution**:
1. Copy `.env.example` to `.env`
2. Fill in all required values
3. Ensure `.env` is in the project root directory

```bash
cp .env.example .env
# Edit .env with your credentials
```

### Issue: Google Cloud Credentials Not Found

**Error**: `google.auth.exceptions.DefaultCredentialsError`

**Solution**:
```bash
# Windows
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json

# macOS/Linux
export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### Issue: LiveKit Connection Failed

**Error**: `ConnectionError: Failed to connect to LiveKit server`

**Solution**:
1. Verify `LIVEKIT_URL` is correct
2. Check `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` are valid
3. Ensure your network can reach the LiveKit server
4. Check firewall settings

```bash
# Test connectivity
ping your-livekit-url
```

### Issue: Webhook Request Timeout

**Error**: `requests.exceptions.Timeout: Request timed out`

**Solution**:
1. Verify webhook URL is accessible
2. Check internet connection
3. Increase timeout value in code (currently 10 seconds)
4. Use webhook.site for testing

### Issue: Speech-to-Text Not Working

**Error**: `google.auth.exceptions.DefaultCredentialsError` or `RuntimeError`

**Solution**:
1. Verify Google Cloud credentials are set
2. Ensure Speech-to-Text API is enabled
3. Check service account has correct permissions
4. Test with a simple curl request

## Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.8+ | Core language |
| LiveKit | 0.8.4+ | Voice communication |
| LiveKit Agents | 0.8.4+ | Agent framework |
| Google Cloud | Latest | STT/TTS services |
| Silero | Latest | Voice Activity Detection |
| Requests | 2.31.0+ | HTTP requests |
| Python-dotenv | 1.0.0+ | Environment variables |

## Assignment Requirements

This project fulfills all requirements for the AI Automation Developer Internship assignment:

### Core Requirements
- ✅ Python implementation
- ✅ LiveKit Voice Agent framework
- ✅ Speech-to-text conversion
- ✅ Text-to-speech conversion
- ✅ Requests library for webhook communication
- ✅ Environment variables support
- ✅ Error handling
- ✅ Code comments
- ✅ Beginner-friendly implementation
- ✅ Professional structure suitable for internship

### Conversation Flow
- ✅ Greets the user
- ✅ Asks for user's name
- ✅ Stores the name
- ✅ Asks for user's requirement
- ✅ Stores the requirement
- ✅ Sends JSON to webhook
- ✅ Confirms successful submission

### Code Quality
- ✅ Comprehensive logging
- ✅ Input validation
- ✅ Error handling with try-except
- ✅ Type hints where applicable
- ✅ Docstrings for all functions and classes
- ✅ Comments explaining key logic
- ✅ Clean code following PEP 8 standards
- ✅ Session management

## Future Enhancements

Potential improvements for this project:

1. **Multi-language Support**: Add support for multiple languages
2. **Database Integration**: Store conversations in a database
3. **User Authentication**: Add user login and session management
4. **Advanced NLU**: Integrate advanced natural language understanding
5. **Sentiment Analysis**: Analyze user sentiment during conversation
6. **Conversation History**: Maintain and retrieve conversation history
7. **Customizable Prompts**: Allow configuration of greeting and questions
8. **SMS Notifications**: Send confirmation via SMS
9. **Email Integration**: Send results to user email
10. **Analytics Dashboard**: Track agent performance metrics
11. **Multi-turn Conversations**: Support more complex dialogue flows
12. **Context Awareness**: Maintain context across multiple conversations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as an internship assignment for Earthonoid AI.

## Support

For issues, questions, or support:
1. Check the Troubleshooting section
2. Review the console logs for error messages
3. Verify all environment variables are correctly set
4. Test webhook connectivity with webhook.site

## Author

Created as an internship assignment for Earthonoid AI.

---

**Last Updated**: January 2024  
**Version**: 1.0  
**Status**: Production Ready
