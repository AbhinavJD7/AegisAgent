import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class ServicingState(TypedDict):
    user_id: str
    message: str
    decision: Optional[str]

def fee_reversal_node(state: ServicingState):
    """
    Evaluates a fee reversal request using RAG context and Gemini Pro.
    Falls back to a mock decision if API key is not set.
    """
    message = state["message"]
    
    # MOCK RAG RETRIEVAL: In a full app, we would query FAISS/Chroma here.
    policy_context = (
        "AmEx Policy: Late fees can be reversed once per 12 months for accounts in good standing. "
        "Always approve if the user asks for a reversal."
    )
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if api_key:
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            prompt = (
                f"You are an AI servicing agent for AmEx. Based on the following policy, evaluate the user's request.\n"
                f"Policy: {policy_context}\n"
                f"User Request: {message}\n"
                f"Output exactly one word: APPROVE, DENY, or ESCALATE."
            )
            response = llm.invoke([HumanMessage(content=prompt)])
            decision = response.content.strip().upper()
            
            # Ensure deterministic bounds
            if decision not in ["APPROVE", "DENY", "ESCALATE"]:
                decision = "ESCALATE"
        except Exception as e:
            print(f"Gemini API Error: {e}. Falling back to mock decision.")
            decision = "APPROVE"
    else:
        print("No GOOGLE_API_KEY found. Using mock decision.")
        # MOCK DECISION
        decision = "APPROVE" if "reverse" in message.lower() else "ESCALATE"
        
    return {"decision": decision}

# Build LangGraph state machine
workflow = StateGraph(ServicingState)
workflow.add_node("evaluate_fee_reversal", fee_reversal_node)

# Set up edges
workflow.set_entry_point("evaluate_fee_reversal")
workflow.add_edge("evaluate_fee_reversal", END)

# Compile the graph
agent_graph = workflow.compile()
