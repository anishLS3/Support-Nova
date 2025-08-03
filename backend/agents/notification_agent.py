import smtplib
from email.message import EmailMessage
from langchain_core.runnables import RunnableLambda
from config import Config  # Ensure MAIL config values are properly set

def get_notification_agent():
    def invoke(payload):
        summary = payload.get("summary")
        email = payload.get("email")
        name = payload.get("name")

        if not email or not name:
            print("❌ Missing email or name in Notification Agent payload.")
            return {
                "result": "⚠️ Notification failed due to incomplete data."
            }

        # Fallback summary for vague or missing details
        if not summary or len(summary.strip().split()) < 4:
            summary = (
                "The user has requested general technical assistance, but did not provide "
                "specific details regarding the issue. We recommend following up to gather more context."
            )

        # Compose the professional email content
        msg = EmailMessage()
        msg["Subject"] = f"🚨 New Customer Support Request - {name}"
        msg["From"] = Config.MAIL_USERNAME
        msg["To"] = "anishls03102004@gmail.com"  # Or support email

        msg.set_content(f"""\
Dear Support Team,

A new customer support complaint has been submitted. Please find the details below:

👤 Customer Name: {name}  
📧 Email Address: {email}  

📝 Complaint Summary:
{summary}

Kindly review the request and initiate follow-up with the user if necessary.

Best regards,  
SupportNova AI Notification System
""")

        try:
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                if Config.MAIL_USE_TLS:
                    server.starttls()
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.send_message(msg)
                print(f"✅ Email sent to support team for user {name}")
                return {
                    "result": f"📬 Notification for {name} sent successfully to support team."
                }
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return {
                "result": f"⚠️ Notification failed due to an email error: {e}"
            }

    return RunnableLambda(invoke)
