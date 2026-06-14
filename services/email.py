
import smtplib
from email.mime.text import MIMEText

async def send_email(to: str, subject: str, body: str):
    """Send email - prints to console for now"""
    
    print(f"\n📧 ===== EMAIL SENT =====")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print(f"========================\n")
    
    # For real email, uncomment and configure:
    # msg = MIMEText(body)
    # msg['Subject'] = subject
    # msg['From'] = 'your-email@gmail.com'
    # msg['To'] = to
    # with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #     server.starttls()
    #     server.login('your-email@gmail.com', 'password')
    #     server.send_message(msg)
    
    return True


