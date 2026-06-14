import uuid
from datetime import datetime
from database.connection import execute_query
from core.ai_scorer import score_lead
from core.router import route_lead

async def process_lead(raw_data: dict, source: str):
    """Main lead processing pipeline"""
    
    lead_id = f"LEAD_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    
    lead = {
        "lead_id": lead_id,
        "source": source,
        "name": raw_data.get("name", "Unknown"),
        "email": raw_data.get("email", ""),
        "phone": raw_data.get("phone", ""),
        "message": raw_data.get("message", ""),
        "created_at": datetime.now().isoformat()
    }
    
    print(f"\n📝 New Lead Received: {lead['name']} ({lead['email']})")
    
    # Save to database
    await execute_query("""
        INSERT INTO leads (lead_id, source, name, email, phone, message, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'new', ?)
    """, lead["lead_id"], lead["source"], lead["name"], lead["email"], 
        lead["phone"], lead["message"], lead["created_at"])
    
    # Get AI scoring
    ai_result = await score_lead(lead)
    
    # Update lead with scores
    await execute_query("""
        UPDATE leads 
        SET lead_score = ?, category = ?, budget = ?, urgency = ?, 
            intent = ?, estimated_value = ?, status = 'analyzed'
        WHERE lead_id = ?
    """, ai_result["score"], ai_result["category"], ai_result["budget"],
        ai_result["urgency"], ai_result["intent"], ai_result["estimated_value"], lead_id)
    
    # Route to workflow (Slack, Email)
    lead.update(ai_result)
    await route_lead(lead)
    
    next_steps_map = {
        "hot": "Sales team will contact you within 15 minutes",
        "warm": "You will receive a nurture sequence via email",
        "cold": "You have been added to our newsletter"
    }
    
    return {
        "status": "success",
        "lead_id": lead_id,
        "category": ai_result["category"],
        "lead_score": ai_result["score"],
        "next_steps": next_steps_map.get(ai_result["category"], "Lead processed successfully")
    }

