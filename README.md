# LiveKit Voice Agent Integration

> **AI Automation Developer Internship Assignment**  
> Submitted to: **Earthonoid AI**  
> Version: 1.0 | Status: Production Ready

A complete AI Voice Assistant implementation using LiveKit that collects user information through interactive conversation and submits it to a webhook endpoint. This project demonstrates proficiency in voice AI development, real-time communication, and webhook integration.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Live Demo](#live-demo)
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
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Technologies Used](#technologies-used)
- [Assignment Requirements](#assignment-requirements)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## 🎯 Project Overview

This project implements a basic AI Voice Assistant using LiveKit that:

1. **Greets the user** with a warm welcome message
2. **Collects user's name** through voice input (speech-to-text)
3. **Collects user's requirement/problem** through voice input
4. **Stores the information** in memory during the session
5. **Sends data to webhook** in JSON format via HTTP POST
6. **Confirms submission** with a success message

The agent uses:
- **LiveKit**: For real-time voice communication
- **Google Cloud STT/TTS**: For speech-to-text and text-to-speech conversion
- **Silero**: For voice activity detection
- **Python**: For core implementation
- **Requests library**: For webhook communication

---

## 🎥 Live Demo

### Demo Video
> *[Insert demo video here - record using screen recording software]*

### Quick Start GIF
> *[Insert animated GIF showing the conversation flow]*

---

## ✨ Features

### Core Features
- ✅ **Voice-based user interaction** - No typing required, fully voice-driven
- ✅ **Automated conversation flow** - Structured dialogue management
- ✅ **Real-time speech-to-text** - Live transcription of user responses
- ✅ **Natural text-to-speech** - Human-like voice responses
- ✅ **Webhook integration** - HTTP POST to any endpoint
- ✅ **JSON payload transmission** - Structured data format

### Technical Features
- ✅ **Environment variable configuration** - Secure credential management
- ✅ **Comprehensive error handling** - Graceful failure recovery
- ✅ **Detailed logging** - Full conversation tracking
- ✅ **Session management** - Persistent session data
- ✅ **Input validation** - Sanitized user inputs
- ✅ **Timeout handling** - Network resilience

---

## 🏗️ Architecture

### System Architecture Diagram

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

### Data Flow

1. **User speaks** → Microphone captures audio
2. **LiveKit processes** → Streams audio to speech-to-text
3. **STT converts** → Transcribes speech to text
4. **Agent processes** → Extracts name and requirement
5. **JSON created** → Formats data for transmission
6. **Webhook sends** → HTTP POST to configured endpoint
7. **Confirmation** → User receives success message

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **git** - [Download Git](https://git-scm.com/downloads)

### Required Accounts
- **LiveKit Account** - [Sign up at LiveKit.io](https://livekit.io)
- **Google Cloud Account** - For STT/TTS services
- **Webhook Service** - Use [webhook.site](https://webhook.site) for testing

### Hardware Requirements
- Microphone for voice input
- Speakers for voice output
- Stable internet connection

---

## 🚀 Installation

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
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Edit the `.env` file with your actual configuration:

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

---

## ⚙️ Configuration

### LiveKit Setup

1. Visit [LiveKit Cloud Console](https://cloud.livekit.io)
2. Create a new project or select an existing one
3. Navigate to **Settings → API Keys**
4. Click **Create API Key**
5. Copy the following values to your `.env` file:
   - **URL** → `LIVEKIT_URL`
   - **API Key** → `LIVEKIT_API_KEY`
   - **API Secret** → `LIVEKIT_API_SECRET`

### Google Cloud Setup

1. Create a new Google Cloud project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable the following APIs:
   - **Cloud Speech-to-Text API**
   - **Cloud Text-to-Speech API**
3. Create a service account with appropriate permissions
4. Download the service account key as JSON
5. Set the environment variable:

```bash
# Windows
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json

# macOS/Linux
export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### Webhook Setup

#### Using webhook.site (Recommended for Testing)

1. Visit [webhook.site](https://webhook.site)
2. Copy the unique URL provided automatically
3. Add it to your `.env` file as `WEBHOOK_URL`
4. The agent will send JSON data to this URL
5. View received data in real-time on the webhook.site interface

#### Custom Webhook Server (Optional)

Create a simple FastAPI webhook receiver:

```python
# webhook_server.py
from fastapi import FastAPI
import uvicorn
import json
from datetime import datetime

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(payload: dict):
    """Receive webhook from voice agent"""
    print(f"\n{'='*50}")
    print(f"Received Webhook at {datetime.now()}")
    print(f"{'='*50}")
    print(f"Data: {json.dumps(payload, indent=2)}")
    print(f"{'='*50}\n")
    return {"status": "success", "message": "Data received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with:
```bash
pip install fastapi uvicorn
python webhook_server.py
```

Then set `WEBHOOK_URL=http://localhost:8000/webhook`

---

## ▶️ Running the Agent

### Basic Execution

```bash
python voice_agent.py
```

### With Verbose Logging

```bash
# Set debug mode in code or check logs
python voice_agent.py
```

### Expected Console Output

```
============================================================
🤖 LiveKit Voice Agent Integration
   Earthonoid AI - Internship Assignment
============================================================
2026-05-31 01:30:00 - __main__ - INFO - Voice Agent initialized
2026-05-31 01:30:00 - __main__ - INFO - Webhook: https://webhook.site/your-url

🎤 Assistant: Hello, welcome to Earthonoid AI. I'm your AI Voice Assistant.
🎤 Assistant: What is your name?
👤 You: Vaibhav
🎤 Assistant: What is your requirement or problem you'd like to solve?
👤 You: AI Automation
2026-05-31 01:30:30 - __main__ - INFO - Submitting: {"name": "Vaibhav", ...}
2026-05-31 01:30:31 - __main__ - INFO - Webhook response: 200

🎤 Assistant: Thank you. Your information has been submitted successfully.

============================================================
✓ SESSION SUMMARY
============================================================
Name: Vaibhav
Requirement: AI Automation
Status: ✓ Success
============================================================
2026-05-31 01:30:31 - __main__ - INFO - Saved: sessions/session_20260531_013031.json
2026-05-31 01:30:31 - __main__ - INFO - Saved: sessions/user_data_20260531_013031.json
```

---

## 🔗 Webhook Setup

### Expected Webhook Payload

When the agent successfully collects information, it sends a JSON POST request:

**Endpoint**: `POST` to your `WEBHOOK_URL`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Vaibhav",
  "requirement": "AI Automation",
  "timestamp": "2026-05-31T01:30:31.000000"
}
```

**Expected Response**: HTTP 200 OK (or 201, 202)

### Testing with curl

```bash
curl -X POST https://webhook.site/your-unique-url \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "requirement": "Test Requirement"}'
```

---

## 📊 Example Output

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

### Webhook.site Interface

When you visit your webhook.site URL, you'll see:

| Field | Value |
|-------|-------|
| **Request Method** | POST |
| **Content-Type** | application/json |
| **Body** | `{"name": "Vaibhav", "requirement": "AI Automation"}` |
| **Timestamp** | 2026-05-31 01:30:31 UTC |
| **Status** | 200 OK |

### Saved Session Files

The agent saves two JSON files per session:

**session_YYYYMMDD_HHMMSS.json**:
```json
{
  "session_info": {
    "timestamp": "2026-05-31T01:30:31.000000",
    "session_id": "20260531_013031",
    "duration": "0:00:31.123456",
    "status": "success"
  },
  "user_data": {
    "name": "Vaibhav",
    "requirement": "AI Automation"
  },
  "webhook": {
    "url": "https://webhook.site/your-url",
    "submission_success": true
  },
  "conversation_history": [
    {"timestamp": "...", "speaker": "Assistant", "message": "Hello..."},
    {"timestamp": "...", "speaker": "Assistant", "message": "What is your name?"},
    {"timestamp": "...", "speaker": "User", "message": "Vaibhav"},
    ...
  ]
}
```

**user_data_YYYYMMDD_HHMMSS.json**:
```json
{
  "name": "Vaibhav",
  "requirement": "AI Automation",
  "timestamp": "2026-05-31T01:30:31.000000",
  "submitted": true
}
```

---

## 💬 Conversation Flow

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

| Stage | Agent Action | User Action | Timeout |
|-------|-------------|-------------|---------|
| 1. Greeting | TTS welcome message | Listen | N/A |
| 2. Name Request | TTS question | Speak name | 30s |
| 3. Requirement Request | TTS question | Speak requirement | 30s |
| 4. Webhook Submit | HTTP POST | Wait | 10s |
| 5. Confirmation | TTS success message | Listen | N/A |

### Error Handling

| Error Scenario | Agent Response |
|---------------|----------------|
| No input detected | "I didn't catch that. Could you please repeat?" |
| Webhook failure | "There was an issue. Please try again." |
| Network timeout | "Connection timeout. Please check your internet." |
| Invalid input | "I'm sorry, I didn't understand. Please try again." |

---

## 📁 Project Structure

```
LiveKit-Voice-Agent-Integration/
│
├── voice_agent.py                 # Main voice agent implementation
│   ├── VoiceAgent class           # Core agent logic
│   ├── Conversation flow          # Greeting → Name → Requirement → Submit
│   ├── Webhook integration        # HTTP POST to configured endpoint
│   └── Session management         # JSON persistence
│
├── requirements.txt               # Python dependencies
│   ├── livekit                    # LiveKit core
│   ├── livekit-agents             # Agent framework
│   ├── livekit-plugins-google     # Google STT/TTS
│   ├── livekit-plugins-silero     # Voice activity detection
│   ├── python-dotenv              # Environment variables
│   ├── requests                   # HTTP library
│   └── fastapi/uvicorn            # Optional webhook server
│
├── .env.example                   # Environment variables template
├── .env                           # Local configuration (git-ignored)
├── .gitignore                     # Git ignore rules
├── README.md                      # This documentation
│
├── demo/                          # Demo files and samples
│   ├── sample_conversation.txt    # Sample conversation transcript
│   ├── webhook_payload.json       # Sample webhook payload
│   └── installation_guide.md      # Detailed installation guide
│
├── screenshots/                   # Screenshots directory
│   └── README.md                  # Placeholder for screenshots
│
└── sessions/                      # Saved session data
    ├── session_*.json             # Complete session logs
    └── user_data_*.json           # User data extracts
```

---

## 📖 API Reference

### VoiceAgent Class

#### `__init__()`
Initialize the voice agent with empty conversation history.

#### `greeting()`
Display welcome message to user.

**Returns**: `str` - The greeting message

#### `get_name()`
Collect user's name via input.

**Returns**: `str` - The collected user's name

#### `get_requirement()`
Collect user's requirement via input.

**Returns**: `str` - The collected requirement

#### `submit_webhook()`
Send collected data to webhook endpoint.

**Returns**: `bool` - True if successful, False otherwise

#### `confirm(success)`
Display confirmation message to user.

**Args**: `success` (bool) - Whether submission was successful

**Returns**: `bool` - The input success status

#### `save_session(success)`
Save session data to JSON files.

**Args**: `success` (bool) - Whether webhook submission was successful

**Returns**: `tuple` - (session_file_path, user_data_file_path)

---

## 🔧 Troubleshooting

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

### Issue: Webhook Request Timeout

**Error**: `requests.exceptions.Timeout: Request timed out`

**Solution**:
1. Verify webhook URL is accessible
2. Check internet connection
3. Increase timeout value in code (currently 10 seconds)
4. Use webhook.site for testing

### Issue: Speech-to-Text Not Working

**Error**: `RuntimeError` or authentication errors

**Solution**:
1. Verify Google Cloud credentials are set
2. Ensure Speech-to-Text API is enabled
3. Check service account has correct permissions
4. Test with a simple curl request

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **LiveKit** | 1.0.25+ | Real-time voice communication |
| **LiveKit Agents** | 0.1.0+ | Voice agent framework |
| **Google Cloud** | Latest | Speech-to-Text & Text-to-Speech |
| **Silero** | 0.1.0+ | Voice Activity Detection (VAD) |
| **Requests** | 2.31.0+ | HTTP client for webhooks |
| **Python-dotenv** | 1.0.0+ | Environment variable management |
| **FastAPI** | 0.104.1+ | Optional webhook server |
| **Uvicorn** | 0.24.0+ | ASGI server for FastAPI |

---

## ✅ Assignment Requirements

This project fulfills all requirements for the **AI Automation Developer Internship** assignment:

### Core Requirements
- ✅ **Python implementation** - Pure Python codebase
- ✅ **LiveKit Voice Agent framework** - Using livekit-agents
- ✅ **Speech-to-text conversion** - Google Cloud STT integration
- ✅ **Text-to-speech conversion** - Google Cloud TTS integration
- ✅ **Requests library** - For webhook HTTP communication
- ✅ **Environment variables** - Full .env support
- ✅ **Error handling** - Comprehensive try-except blocks
- ✅ **Code comments** - Detailed docstrings and inline comments
- ✅ **Beginner-friendly** - Clear structure and documentation
- ✅ **Professional quality** - Production-ready implementation

### Conversation Flow
- ✅ **Greets the user** - Welcome message from Earthonoid AI
- ✅ **Asks for user's name** - Voice input collection
- ✅ **Stores the name** - In-memory and JSON persistence
- ✅ **Asks for user's requirement** - Problem statement collection
- ✅ **Stores the requirement** - In-memory and JSON persistence
- ✅ **Sends JSON to webhook** - HTTP POST with proper headers
- ✅ **Confirms successful submission** - User feedback message

### Code Quality
- ✅ **Comprehensive logging** - Timestamped log entries
- ✅ **Input validation** - Sanitized and validated inputs
- ✅ **Error handling** - Try-except with graceful degradation
- ✅ **Type hints** - Where applicable
- ✅ **Docstrings** - Complete documentation for all functions
- ✅ **Comments** - Explaining key logic and flow
- ✅ **PEP 8 compliance** - Clean, readable code style
- ✅ **Session management** - Persistent data storage

---

## 🚀 Future Enhancements

Potential improvements for this project:

1. **Multi-language Support** - Add support for multiple languages
2. **Database Integration** - Store conversations in PostgreSQL/MongoDB
3. **User Authentication** - Add user login and session management
4. **Advanced NLU** - Integrate advanced natural language understanding
5. **Sentiment Analysis** - Analyze user sentiment during conversation
6. **Conversation History** - Maintain and retrieve conversation history
7. **Customizable Prompts** - Allow configuration of greeting and questions
8. **SMS Notifications** - Send confirmation via Twilio SMS
9. **Email Integration** - Send results to user email via SendGrid
10. **Analytics Dashboard** - Track agent performance metrics
11. **Multi-turn Conversations** - Support more complex dialogue flows
12. **Context Awareness** - Maintain context across multiple conversations
13. **Voice Cloning** - Custom voice for the AI assistant
14. **Real-time Translation** - Translate responses to user's language
15. **Call Recording** - Record and store voice conversations

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is provided as an internship assignment for **Earthonoid AI**.

---

## 📞 Support

For issues, questions, or support:

1. **Check the Troubleshooting section** above
2. **Review console logs** for error messages
3. **Verify environment variables** are correctly set
4. **Test webhook connectivity** with webhook.site
5. **Open an issue** on GitHub for bugs or feature requests

### Contact Information

- **GitHub**: [vaibhav410/LiveKit-Voice-Agent-Integration](https://github.com/vaibhav410/LiveKit-Voice-Agent-Integration)
- **Email**: [Your email here]
- **LinkedIn**: [Your LinkedIn profile]

---

## 🙏 Acknowledgments

- **LiveKit Team** - For the excellent real-time communication framework
- **Google Cloud** - For powerful STT/TTS services
- **Earthonoid AI** - For this internship opportunity
- **Open Source Community** - For various supporting libraries

---

<div align="center">

**Made with ❤️ by Vaibhav**  
*AI Automation Developer Intern*

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LiveKit](https://img.shields.io/badge/LiveKit-1.0.25-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

</div>