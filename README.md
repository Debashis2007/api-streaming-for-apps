# Use Case: API Streaming for Apps

**Author fingerprint:** `DBHATT-Debashis2007-SystemDesignPOC-2026` — Debashis Bhattacharjee ([@Debashis2007](https://github.com/Debashis2007))

**YouTube walkthrough:** [Api Streaming For Apps — System Design #Shorts](https://youtu.be/4Ush4VcE7oc)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [02 — Streaming Token Delivery](../02-streaming-token-delivery.md)  
**Also references:** [09 — Multi-model routing / API platform](../09-multi-model-routing-api-platform.md)

## Users & problem

Developers build products on your streaming API. They need stable event schemas, resume semantics, and rate limits that don’t strand open connections.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Event schema | Versioned; documented `token` / `tool` / `done` |
| Resume | `after_seq` supported for a short TTL |
| Limits | Concurrent streams per key + TPM |
| Errors | Typed mid-stream error events |

## Design (from parent)

```
SDK/HTTP SSE → Gateway (auth, concurrent stream quota)
  → Router → Inference → sequenced events
  → Usage metering on completion / abort
```

Reuse ring buffer resume, backpressure, and idempotent finalize from **02**. Enforce quotas from **09**.

## Specializations

| Concern | API choice |
|---------|------------|
| Contract | Strict OpenAPI/Async schema; SDKs generated |
| Hedging | Generally off for streams (double cost risk) |
| ZDR | Optional no-persist mode for enterprise |
| Fairness | Cap concurrent streams; 503 + Retry-After |

## Failure modes

- Idle open connections → read deadlines; reclaim slots.
- Resume after TTL → `410` + point to final message if completed.
- Partial tool JSON streamed unsafely → buffer tool args until valid/safe.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Api Streaming For Apps — System Design #Shorts](https://youtu.be/4Ush4VcE7oc)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd api-streaming-for-apps
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -N -X POST http://127.0.0.1:8000/v1/chat/stream -H 'x-api-key: demo' -H 'Content-Type: application/json' -d '{"prompt":"hi"}'

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

