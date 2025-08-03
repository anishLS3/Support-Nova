from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.router_agent import classify_intent
from agents.service_recommender import get_service_recommender_agent
from agents.faq_agent import get_faq_agent
from agents.appointment_agent import get_appointment_agent
from agents.notification_agent import get_notification_agent
from concurrent.futures import ThreadPoolExecutor

# Thread pool for parallel processing
executor = ThreadPoolExecutor(max_workers=3)

# ------------------ Graph State ------------------
class GraphState(TypedDict):
    query: str
    email: str
    intent: Optional[str]
    response: Optional[str]
    summary: Optional[str]
    name: Optional[str]
    escalate: Optional[bool]
    awaiting_details: Optional[bool]

# ------------------ Router Node ------------------
def router_node(state: GraphState) -> GraphState:
    print(f"[Router Node] Incoming state: {state}")
    query = state.get("query")
    if not query:
        raise ValueError("❌ Missing 'query' in state at router_node")

    intent = classify_intent(query)
    print(f"[Router Node] Detected intent: {intent}")

    if state.get("awaiting_details"):
        print("[Router Node] Awaiting details previously set. Moving to escalation_details.")
        state["intent"] = "escalation_details"
        state["awaiting_details"] = False
    else:
        state["intent"] = intent

    return state

# ------------------ Service Node ------------------
service_agent = get_service_recommender_agent()

def service_node(state: GraphState) -> GraphState:
    print(f"[Service Node] Query: {state.get('query')} | Email: {state.get('email')}")
    
    future = executor.submit(service_agent.invoke, {
        "query": state["query"],
        "email": state["email"]
    }, config={"configurable": {"session_id": state["email"]}})
    
    result = future.result()
    print(f"[Service Node] Response: {result}")
    state["response"] = result["result"]
    return state

# ------------------ FAQ Node ------------------
def faq_node(state: GraphState) -> GraphState:
    print(f"[FAQ Node] Query: {state.get('query')} | Email: {state.get('email')}")
    
    faq_agent = get_faq_agent()
    result = faq_agent.invoke({
        "query": state["query"],
        "email": state["email"]
    })

    state["response"] = result.get("result", "⚠️ Something went wrong while answering your query.")
    state["escalate"] = result.get("escalate", False)

    if state["escalate"]:
        if "query" in result:
            state["query"] = result["query"]
        state["awaiting_details"] = True

    return state

# ------------------ Appointment Node ------------------
appointment_agent = get_appointment_agent()

def appointment_node(state: GraphState) -> GraphState:
    print(f"[Appointment Node] Escalated Query: {state.get('query')} | Email: {state.get('email')}")

    future = executor.submit(appointment_agent.invoke, {
        "query": state["query"],
        "email": state["email"]
    })
    
    result = future.result()
    print(f"[Appointment Node] Complaint Log Result: {result['result']}")
    state["response"] = result["result"]
    state["summary"] = result.get("summary")
    return state

# ------------------ Notification Node ------------------
notify_agent = get_notification_agent()

def notification_node(state: GraphState) -> GraphState:
    future = executor.submit(notify_agent.invoke, {
        "summary": state.get("summary"),
        "email": state.get("email"),
        "name": state.get("name", "User")
    })
    
    result = future.result()
    print(f"[Notification Node] Notification Response: {result['result']}")

    summary_text = state.get("summary", "No summary available.")
    state["response"] = (
        f"📬 We've notified our support team. Here’s a summary of what was escalated:\n\n"
        f"{summary_text}\n\n"
        "Our support team will reach out to you shortly. Thanks for your patience!"
    )

    return state

# ------------------ Collect Details Node ------------------
def collect_details_node(state: GraphState) -> GraphState:
    print("📝 Collecting complaint details from user...")
    state["response"] = (
        "✅ Thanks! Please describe the issue you're facing in a few words so we can escalate it to our support team."
    )
    state["awaiting_details"] = True
    return state

# ------------------ LangGraph Creation ------------------
def create_langgraph_flow():
    builder = StateGraph(GraphState)

    builder.add_node("router", router_node)
    builder.add_node("service", service_node)
    builder.add_node("faq", faq_node)
    builder.add_node("collect", collect_details_node)
    builder.add_node("appointment", appointment_node)
    builder.add_node("notify", notification_node)

    builder.set_entry_point("router")

    builder.add_conditional_edges("router", lambda s: s["intent"], {
        "service": "service",
        "complaint": "faq",
        "collect": "collect",
        "escalation_details": "appointment",
    })

    builder.add_conditional_edges("faq", lambda s: s.get("escalate", False), {
        True: "collect",
        False: END
    })

    builder.add_edge("collect", "router")
    builder.add_edge("appointment", "notify")
    builder.add_edge("notify", END)
    builder.add_edge("service", END)

    return builder.compile()

# ✅ Compile the flow
langgraph_flow = create_langgraph_flow()
