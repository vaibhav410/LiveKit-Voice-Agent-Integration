# Q3 – AWS Deployment

**Earthonoid AI Automation Developer Internship**  
**Author:** Vaibhav | **Repository:** [LiveKit-Voice-Agent-Integration](https://github.com/vaibhav410/LiveKit-Voice-Agent-Integration)

---

## Deployment Overview

This document describes how to deploy the LiveKit Voice Agent on **Amazon Web Services (AWS)** using an **EC2** instance. The voice agent collects user information (name and requirement) through conversation, submits a JSON payload to a webhook, logs the session locally, and can be monitored in production.

| Component | Role |
|-----------|------|
| **AWS EC2** | Hosts the Python voice agent and optional local webhook server |
| **Security Group** | Controls inbound/outbound network access |
| **LiveKit Cloud** | Real-time voice communication (STT/TTS when fully integrated) |
| **Webhook endpoint** | Receives lead data (`name`, `requirement`) via HTTP POST |

---

## AWS Architecture Diagram

```
┌──────────┐
│   User   │  (Voice / Browser / CLI client)
└────┬─────┘
     │
     ▼
┌──────────────────────────────────────────┐
│              AWS EC2 Instance             │
│  ┌────────────────────────────────────┐  │
│  │         Voice Agent (Python)        │  │
│  │  • Greeting & data collection         │  │
│  │  • JSON payload generation          │  │
│  │  • Session logging → /sessions      │  │
│  └────────────────┬───────────────────┘  │
└───────────────────┼──────────────────────┘
                    │ HTTP POST (JSON)
                    ▼
            ┌───────────────┐
            │    Webhook    │  (webhook.site / API Gateway / custom server)
            └───────────────┘
```

**Flow:** User → AWS EC2 → Voice Agent → Webhook

See also: [`screenshots/q3_architecture.png`](../screenshots/q3_architecture.png)

---

## EC2 Deployment Steps

### 1. Launch an EC2 Instance

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Navigate to **EC2 → Instances → Launch Instance**.
3. Recommended settings:

| Setting | Value |
|---------|--------|
| **Name** | `earthonoid-voice-agent` |
| **AMI** | Ubuntu Server 22.04 LTS |
| **Instance type** | `t3.small` (or `t3.micro` for testing) |
| **Key pair** | Create or select an existing `.pem` key |
| **Storage** | 20 GB gp3 (default is sufficient) |

4. Under **Network settings**, create or assign a security group (see next section).
5. Launch the instance and note the **public IPv4 address**.

### 2. Connect via SSH

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

---

## Security Group Configuration

Create a security group with the following rules:

| Type | Protocol | Port | Source | Purpose |
|------|----------|------|--------|---------|
| SSH | TCP | 22 | Your IP only | Secure server administration |
| HTTP | TCP | 80 | 0.0.0.0/0 | Optional: reverse proxy / health checks |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Optional: TLS termination |
| Custom TCP | TCP | 8000 | Your IP or VPC | Local webhook test server (`webhook_server.py`) |

> **Security best practice:** Restrict SSH (port 22) to your office/home IP. Do not expose port 8000 publicly in production; use API Gateway or an internal load balancer instead.

---

## Python Installation

On the EC2 instance (Ubuntu):

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git
python3 --version   # Verify 3.8+
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Git Clone Instructions

```bash
cd ~
git clone https://github.com/vaibhav410/LiveKit-Voice-Agent-Integration.git
cd LiveKit-Voice-Agent-Integration
```

---

## Environment Setup

```bash
cp .env.example .env
nano .env   # or vim .env
```

Configure the following variables:

```env
LIVEKIT_URL=https://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
WEBHOOK_URL=https://webhook.site/your-unique-id
PARTICIPANT_NAME=AI Assistant
ROOM_NAME=voice-agent-room
```

For Google Cloud STT/TTS (full LiveKit voice pipeline):

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/ubuntu/credentials.json
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Option A: Voice agent (main application)

```bash
source venv/bin/activate
python voice_agent.py
```

### Option B: Local webhook receiver (testing)

Terminal 1:

```bash
python webhook_server.py
```

Terminal 2:

```bash
export WEBHOOK_URL=http://127.0.0.1:8000/webhook
python voice_agent.py
```

### Option C: Run as a background service (systemd)

Create `/etc/systemd/system/voice-agent.service`:

```ini
[Unit]
Description=Earthonoid LiveKit Voice Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/LiveKit-Voice-Agent-Integration
Environment=PATH=/home/ubuntu/LiveKit-Voice-Agent-Integration/venv/bin
ExecStart=/home/ubuntu/LiveKit-Voice-Agent-Integration/venv/bin/python voice_agent.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable voice-agent
sudo systemctl start voice-agent
sudo systemctl status voice-agent
```

---

## Monitoring Strategy

| Layer | Tool / Method | What to monitor |
|-------|----------------|-----------------|
| **Application** | Python `logging` module | Conversation steps, webhook status codes |
| **Sessions** | `sessions/*.json` files | Per-session success/failure, payloads |
| **EC2** | CloudWatch Agent | CPU, memory, disk, network |
| **Webhook** | webhook.site / API logs | POST success rate, latency |
| **Alerts** | CloudWatch Alarms | CPU > 80%, instance status check failed |

### Recommended CloudWatch metrics

- `CPUUtilization` – scale or upgrade instance if sustained high usage
- `StatusCheckFailed` – instance health
- Custom log metric filter on `"Webhook error"` in application logs

### Log locations

```text
Application stdout  → journalctl -u voice-agent -f
Session files       → ./sessions/session_*.json
Webhook server      → uvicorn INFO logs
```

---

## Production Checklist

- [ ] `.env` configured and never committed to Git
- [ ] Security group restricts SSH to trusted IPs
- [ ] Webhook URL uses HTTPS in production
- [ ] `sessions/` directory backed up or synced to S3 (optional)
- [ ] systemd service enabled for auto-restart
- [ ] CloudWatch alarms configured

---

## Related Documentation

- [README – AWS Section](../README.md#aws-deployment-q3)
- [Q4 – Workflow Design](./Q4_Workflow_Design.md)
- [Q5 – Scalability](./Q5_Scalability.md)
