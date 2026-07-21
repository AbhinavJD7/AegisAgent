# AegisAgent

**Zero-Trust Conversational Servicing Agent**
Hackathon Project — AmEx Codestreet 2026

## Overview

A conversational agent that resolves routine card-servicing requests (like fee reversals and credit limit checks) end-to-end in a single interaction. Crucially, every AI decision is logged to an immutable, cryptographically verifiable Solana on-chain audit trail.

This prevents any human admin from retroactively altering or hiding what the agent did.

## Architecture

The system consists of a 5-step request lifecycle:

1. **INGEST**: Next.js frontend chat UI.
2. **EVALUATE**: FastAPI backend using LangGraph state machine. Uses RAG over mock policy docs to evaluate eligibility with Gemini Pro API.
3. **EXECUTE**: Calls a mock banking API to enact the decision (e.g., reverse a fee).
4. **AUDIT (async)**: Computes a SHA-256 hash of the decision context and pushes it to a Redis/Celery queue so the UI isn't blocked.
5. **COMMIT**: A Solana Anchor program receives the hash and emits an immutable on-chain event.

See [docs/architecture.md](docs/architecture.md) for more details.

## Setup Instructions

*(To be expanded as development continues)*

### Prerequisites
- Node.js & npm (for frontend)
- Python 3.10+ (for backend)
- Rust, Solana CLI, & Anchor CLI (for Solana program)
- Redis (for Celery broker)

### Current Status
- Scaffolded basic directory structure.
- Built initial Solana Anchor program skeleton for logging decisions on-chain.
