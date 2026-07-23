from fastapi import FastAPI
from pydantic import BaseModel
from graph import agent_graph

app = FastAPI(title="AegisAgent Servicing API")

class ServiceRequest(BaseModel):
    user_id: str
    message: str

@app.post("/api/service_request")
async def handle_service_request(request: ServiceRequest):
    # Prepare the initial state for LangGraph
    initial_state = {
        "user_id": request.user_id,
        "message": request.message,
        "decision": None
    }
    
    # Invoke the LangGraph state machine
    # This simulates evaluating the request against RAG policy and making a decision
    final_state = agent_graph.invoke(initial_state)
    decision = final_state.get("decision", "ESCALATE")
    
    # Return the response to the frontend
    # In Step 4, we will add SHA-256 hashing and queue this for Solana on-chain logging.
    return {
        "user_id": request.user_id,
        "message": request.message,
        "decision": decision,
        "status": "success",
        "blockchain_audit_status": "Pending implementation (Step 4)"
    }
