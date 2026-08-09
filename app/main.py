# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""API Streaming for Apps — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "API Streaming for Apps"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(USE_CASE)


import uuid
from sse_starlette.sse import EventSourceResponse
from poc_core.sse import format_sse

stream_quota = TokenBucket(5, 1)
buffers: dict[str, list[dict]] = {}

class SIn(BaseModel):
    prompt: str

@app.post("/v1/chat/stream")
async def chat_stream(body: SIn, request: Request):
    if not stream_quota.allow():
        raise HTTPException(429, detail="concurrent/stream quota")
    key = request.headers.get("x-api-key", "anon")
    gid = f"g_{uuid.uuid4().hex[:8]}"
    buffers[gid] = []

    async def gen():
        yield format_sse("meta", {"generation_id": gid, "api_key": key})
        seq = 0
        async for tok in llm.stream(body.prompt, max_tokens=16):
            seq += 1
            evt = {"seq": seq, "text": tok}
            buffers[gid].append(evt)
            yield format_sse("token", evt, str(seq))
        yield format_sse("done", {"generation_id": gid})

    return EventSourceResponse(gen())

@app.get("/v1/chat/stream/{generation_id}")
def resume(generation_id: str, after_seq: int = 0):
    buf = buffers.get(generation_id)
    if buf is None:
        raise HTTPException(410, detail="expired")
    return {"events": [e for e in buf if e["seq"] > after_seq]}
