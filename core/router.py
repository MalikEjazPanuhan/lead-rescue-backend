
from services.slack import send_slack
from services.email import send_email
from datetime import datetime, timedelta

async def route_lead(lead: dict):
    if lead["category"] == "hot":
        await handle_hot(lead)
    elif lead["category"] == "warm":
        await handle_warm(lead)
    else:
        await handle_cold(lead)

async def handle_hot(lead: dict):
    await send_slack("hot", f"🔥 *HOT LEAD ALERT!*\n• Lead: {lead['lead_id']}\n• Name: {lead['name']}\n• Score: {lead['score']}/100\n• Message: {lead['message']}")
    
    if lead.get("email"):
        await send_email(lead["email"], "URGENT: We're ready to help!", f"Hi {lead['name']},\n\nOur sales team will contact you within 15 minutes.\n\nBest regards,\nLead Rescue Team")
    
    print(f"✅ Hot lead {lead['lead_id']} - Sales team notified")

async def handle_warm(lead: dict):
    await send_slack("warm", f"🟡 *Warm Lead Added*\n• Lead: {lead['lead_id']}\n• Name: {lead['name']}\n• Will receive nurture sequence")
    
    if lead.get("email"):
        await send_email(lead["email"], "Thanks for your interest!", f"Hi {lead['name']},\n\nThanks for reaching out! We'll send you some helpful resources.\n\nBest regards,\nLead Rescue Team")
    
    print(f"✅ Warm lead {lead['lead_id']} - Nurture email sent")

async def handle_cold(lead: dict):
    await send_slack("cold", f"❄️ Cold Lead: {lead['lead_id']} - {lead['name']}")
    print(f"✅ Cold lead {lead['lead_id']} - Added to newsletter list")


