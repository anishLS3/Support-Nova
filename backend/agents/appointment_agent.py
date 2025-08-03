from langchain_core.runnables import RunnableLambda
from database.complaint_db import insert_complaint
from agents.notification_agent import get_notification_agent
from utils.llm import get_llm

def generate_summary_prompt(email, description):
    return f"""
You are a professional assistant. Summarize the following customer complaint for the internal support team.

Email: {email}
Issue Description: {description}

The summary should be clear, concise, and professional.
"""

def get_appointment_agent():
    def invoke(payload):
        description = payload.get("query", "").strip()
        email = payload.get("email", "").strip()

        if not description or not email:
            return {
                "result": "⚠️ Please provide both your issue and email so we can help you.",
                "summary": None
            }

        print(f"[Appointment Agent] Logging issue from {email}: {description}")

        llm = get_llm()
        try:
            summary_prompt = generate_summary_prompt(email, description)
            summary = llm.invoke(summary_prompt).content.strip()
        except Exception as e:
            print(f"❌ Summary generation failed: {e}")
            summary = f"Complaint from {email}: {description}"

        print(f"[Appointment Agent] Summary:\n{summary}")
        # Store in DB
        insert_complaint(email=email, query=description, summary=summary)
        print(f"✅ Complaint inserted for: {email}")

        # Generate summary
        

        # Notify support team
        notify_result = get_notification_agent().invoke({
            "summary": summary,
            "email": email,
            "name": email.split("@")[0]  # fallback name from email
        })

        return {
            "result": "✅ Your complaint has been logged. Our support team will contact you shortly.",
            "summary": summary
        }

    return RunnableLambda(invoke)
