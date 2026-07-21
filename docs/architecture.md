# AegisAgent Architecture

This document outlines the architecture for the AegisAgent zero-trust conversational servicing agent.

## 5-Step Request Lifecycle

1. **INGEST**: 
   - **Component**: Next.js frontend, React, Tailwind CSS.
   - **Role**: Provides a simple chat UI for users to submit requests like "reverse my late fee."

2. **EVALUATE**:
   - **Component**: FastAPI backend + LangGraph.
   - **Role**: Routes the user intent to the appropriate node (e.g., `FeeReversalNode`). RAG is used over mock policy documents to fetch rules. Gemini Pro evaluates the request (Approve, Deny, Escalate) in a deterministic way bounded by context.

3. **EXECUTE**:
   - **Component**: FastAPI Mock Endpoint + PostgreSQL.
   - **Role**: If approved, a mock banking API is called to perform the action. The decision is recorded in the relational database.

4. **AUDIT (async)**:
   - **Component**: Redis + Celery.
   - **Role**: A SHA-256 hash of the decision context (user request, policy reference, model decision, timestamp) is computed and pushed to a background queue. This ensures the frontend doesn't block on blockchain confirmation.

5. **COMMIT**:
   - **Component**: Solana Anchor Program (Rust).
   - **Role**: Receives the hashed context and emits an on-chain event. No persistent account state is used to keep costs near zero. This provides an immutable, verifiable audit trail.
