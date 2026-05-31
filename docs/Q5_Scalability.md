# Q5 – Scalability & Problem Solving

**Earthonoid AI Automation Developer Internship**  
**Author:** Vaibhav | **Repository:** [LiveKit-Voice-Agent-Integration](https://github.com/vaibhav410/LiveKit-Voice-Agent-Integration)

---

## Problem Statement

> **Suppose 1,000 leads arrive in a single day.**  
> How would you design the system to handle this load reliably without data loss, duplicate CRM entries, or degraded user experience?

**Assumptions:**

- Average ~42 leads/hour (peak hours may reach 150–200/hour)
- Each lead requires webhook ingestion, AI enrichment, CRM write, and email notification
- Voice agent and website form share the same downstream pipeline

---

## Target Architecture

```
┌────────────┐     ┌──────────┐     ┌───────┐     ┌─────────┐     ┌─────┐     ┌───────────────┐
│ Lead Form  │ ──► │ Webhook  │ ──► │ Queue │ ──► │ Workers │ ──► │ CRM │ ──► │ Email Service │
└────────────┘     └──────────┘     └───────┘     └─────────┘     └─────┘     └───────────────┘
```

See: [`screenshots/q5_scalability.png`](../screenshots/q5_scalability.png)

---

## Scaling Strategy

| Phase | Volume | Approach |
|-------|--------|----------|
| **MVP** | &lt; 100 leads/day | Synchronous webhook → direct CRM API (current voice agent pattern) |
| **Growth** | 100–1,000 leads/day | Introduce message queue; async workers |
| **Scale** | 1,000+ leads/day | Auto-scaling workers, read replicas, CDN for forms |

### Horizontal vs vertical scaling

- **Vertical:** Increase EC2 instance size (`t3.small` → `t3.medium`) — quick fix, single point of failure  
- **Horizontal:** Multiple worker instances behind a queue — **recommended** for 1,000 leads/day  

### Capacity estimate (1,000 leads/day)

| Step | Avg time | Parallelism |
|------|----------|-------------|
| Webhook ingest | 50 ms | API Gateway + Lambda or ALB |
| Queue write | 10 ms | SQS (unlimited throughput at this scale) |
| AI processing | 2–5 s | 5–10 workers |
| CRM API call | 300 ms | Rate-limit aware pool |
| Email send | 200 ms | SES batch / async |

With **5 concurrent workers**, ~1,000 leads can be processed in **~35–50 minutes** at peak sustained rate; with **10 workers**, under **20 minutes**.

---

## Queue-Based Architecture

### Why a queue?

- **Decouples** ingestion from processing (webhook returns `200` immediately)
- **Buffers** traffic spikes (e.g., 200 leads in one hour)
- **Enables retries** without blocking the user
- **Prevents CRM rate-limit violations**

### Recommended AWS flow

```
API Gateway  →  Lambda (validate + enqueue)  →  SQS  →  ECS/EC2 Workers  →  CRM + SES
                     │
                     └──► DLQ (failed messages after N retries)
```

| Service | Purpose |
|---------|---------|
| **API Gateway** | Public HTTPS endpoint, throttling, API keys |
| **Lambda** | Validate JSON, assign `lead_id`, push to SQS |
| **Amazon SQS** | Standard queue for lead jobs |
| **SQS DLQ** | Dead-letter queue for poison messages |
| **ECS / EC2 Auto Scaling** | Worker fleet processes queue |
| **DynamoDB** | Idempotency store (`lead_id` → status) |
| **Amazon SES** | Transactional email |
| **CloudWatch** | Metrics, logs, alarms |

---

## Retry Logic

| Layer | Policy |
|-------|--------|
| **SQS visibility timeout** | 30–60s (must exceed max worker processing time) |
| **SQS redrive policy** | Max 3 receives → move to DLQ |
| **CRM API** | Exponential backoff on 429/5xx; respect `Retry-After` header |
| **Email (SES)** | 2 retries; suppress list for hard bounces |
| **Idempotency** | Check DynamoDB before CRM create; skip if `status=completed` |

### Message schema (queue body)

```json
{
  "lead_id": "uuid-v4",
  "name": "Vaibhav",
  "requirement": "AI Automation",
  "source": "voice_agent",
  "enqueued_at": "2026-05-31T12:00:00Z",
  "attempt": 1
}
```

---

## Monitoring

| Metric | Source | Purpose |
|--------|--------|---------|
| `ApproximateNumberOfMessagesVisible` | SQS | Backlog depth |
| `NumberOfMessagesDeleted` | SQS | Throughput |
| Worker processing time | CloudWatch custom | Performance |
| CRM API error rate | Application logs | Integration health |
| DLQ message count | SQS DLQ | Failed leads requiring intervention |

### Dashboards

1. **Ingestion** – requests/min, 4xx/5xx rate  
2. **Queue** – depth, age of oldest message  
3. **Workers** – CPU, active tasks, success/fail counts  
4. **Downstream** – CRM sync latency, email delivery rate  

---

## Logging

| Log type | Destination | Retention |
|----------|-------------|-----------|
| Access logs | API Gateway → CloudWatch Logs | 30 days |
| Application logs | CloudWatch Logs / OpenSearch | 90 days |
| Audit trail | S3 + Glacier | 1 year (compliance) |
| Session files (voice agent) | S3 sync from EC2 | 90 days |

### Correlation ID

Every lead receives a `lead_id` propagated through webhook → queue → worker → CRM → email logs for end-to-end tracing.

---

## Alerting

| Alarm | Condition | Action |
|-------|-----------|--------|
| High queue depth | &gt; 500 messages for 10 min | Scale out workers |
| DLQ non-empty | &gt; 0 messages | SNS → on-call engineer |
| Webhook 5xx rate | &gt; 5% over 5 min | Page ops |
| Worker CPU | &gt; 80% for 15 min | Auto Scaling policy |
| CRM failures | &gt; 20 failures/hour | Email ops team |

**SNS topics:** `ops-critical`, `ops-warning`, `business-leads`

---

## AWS Services Summary

| Service | Role in 1,000 leads/day design |
|---------|--------------------------------|
| **EC2 / ECS** | Voice agent host + worker containers |
| **Application Load Balancer** | Distribute webhook traffic |
| **API Gateway** | Managed ingress + throttling |
| **SQS** | Lead job queue |
| **Lambda** | Lightweight validation and enqueue |
| **DynamoDB** | Idempotency and lead state |
| **SES** | Email notifications |
| **CloudWatch** | Metrics, logs, alarms |
| **Auto Scaling** | Worker fleet based on queue depth |
| **S3** | Session backup, log archive |

---

## Auto Scaling

### EC2 Auto Scaling policy (worker tier)

```text
Target tracking: ApproximateNumberOfMessagesVisible per worker ≈ 50
Min instances: 2
Max instances: 10
Scale-out cooldown: 60 seconds
Scale-in cooldown: 300 seconds
```

### Scaling trigger example

| Queue depth | Worker instances |
|-------------|------------------|
| 0–100 | 2 |
| 100–300 | 4 |
| 300–600 | 6 |
| 600+ | 8–10 |

---

## Failure Scenarios & Mitigations

| Scenario | Mitigation |
|----------|------------|
| Webhook flood | API Gateway throttling (e.g., 100 req/s) + WAF |
| Worker crash mid-job | SQS visibility timeout → message reprocessed |
| CRM outage | Queue backs up; workers retry; no user-facing failure |
| Duplicate submission | Idempotency key in DynamoDB |
| Email provider down | Queue email step separately; retry from DLQ |

---

## Link to This Repository

The current `voice_agent.py` implements the **ingestion** pattern (collect → POST → log). At 1,000 leads/day, the webhook receiver should **acknowledge immediately** and enqueue—matching the architecture above—while this repository’s session JSON files serve as a **local audit trail** during development.

---

## Related Documentation

- [Q3 – AWS Deployment](./Q3_AWS_Deployment.md)
- [Q4 – Workflow Design](./Q4_Workflow_Design.md)
- [README – Scalability Section](../README.md#scalability-q5)
