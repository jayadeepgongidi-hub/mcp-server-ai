from mcp.server.fastmcp import FastMCP
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load .env file (if exists)
load_dotenv()

# ✅ Use a standard name MCP expects
mcp = FastMCP("Email Notification Agent")

# ✅ Get credentials from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

@mcp.tool()
def send_email(to: str, subject: str, message: str) -> str:
    """
    Send an email notification or reminder.
    Example:
        send_email("receiver@gmail.com", "Meeting Reminder", "Don't forget our 3 PM call!")
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return "Email credentials not found. Please set SENDER_EMAIL and SENDER_PASSWORD in .env"

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return f"✅ Email sent successfully to {to}!"

    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

