# Design: API Streaming for Apps

**Project:** `api-streaming-for-apps`  
**Parent system design:** [02 — Streaming Token Delivery](https://github.com/Debashis2007/api-streaming-for-apps/blob/main/02-streaming-token-delivery.md) · [09 — Multi-Model Routing / API Platform](https://github.com/Debashis2007/api-streaming-for-apps/blob/main/09-multi-model-routing-api-platform.md)

## 1. What this POC demonstrates

Developer streaming API with concurrent stream quota, sequenced events, and resume.

## 2. Architecture (POC)

```text
POST /v1/chat/stream (SSE) → buffered events
GET /v1/chat/stream/{id}?after_seq=
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Stream concurrency quota | Open SSE connections are scarce. | `TokenBucket` on accept. |
| Versioned event schema | SDKs need stable `token`/`done` events. | `format_sse` event names. |
| Resume after_seq | Mobile networks drop; clients reattach. | In-memory `buffers`. |

## 4. Key endpoints

`GET /health`, `POST /v1/chat/stream`, `GET /v1/chat/stream/{generation_id}`

## 5. Tradeoffs / POC limits

Quota approximates concurrent streams; production tracks active FDs per key.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

> **Watch on YouTube:** [Api Streaming For Apps — System Design #Shorts](https://youtu.be/4Ush4VcE7oc)
>
> Direct link: **https://youtu.be/4Ush4VcE7oc**

Also available in-repo:
- GIF preview: [`video/design-overview.gif`](./video/design-overview.gif)
- MP4 download: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Narration script: [`video/narration.txt`](./video/narration.txt)

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

