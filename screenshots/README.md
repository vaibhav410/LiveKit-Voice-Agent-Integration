# Screenshots

Visual evidence for the Earthonoid AI internship assessment.

| File | Assignment | Description |
|------|------------|-------------|
| `q2_voice_agent.png` | Q2 | Voice agent flow: conversation, webhook, session logging |
| `q3_architecture.png` | Q3 | Architecture: User → EC2 → Voice Agent → Webhook |
| `q3_ec2_running.png` | Q3 | EC2 instance state = Running |
| `q3_application_running.png` | Q3 | Voice agent executing on EC2 with webhook success |
| `q3_cloudwatch.png` | Q3 | CloudWatch metrics and monitoring |
| `q4_workflow.png` | Q4 | Lead pipeline: Form → Webhook → AI → CRM → Email |
| `q5_scalability.png` | Q5 | Queue-based architecture for 1,000 leads/day |

### Replacing Q3 screenshots with live captures

After deploying on your AWS account, replace these files with real console captures:

1. **q3_ec2_running.png** — EC2 → Instances → `earthonoid-voice-agent` → Running
2. **q3_application_running.png** — SSH terminal showing `python voice_agent.py` success output
3. **q3_cloudwatch.png** — CloudWatch → Monitoring / Alarms for your instance
