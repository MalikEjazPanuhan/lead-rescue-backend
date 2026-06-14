from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from core.processor import process_lead
from database.connection import execute_query, init_db
import json
import qrcode
import base64
from io import BytesIO

router = APIRouter()

# Initialize database
init_db()

class LeadRequest(BaseModel):
    name: str
    email: Optional[str] = ""
    phone: Optional[str] = ""
    message: Optional[str] = ""

@router.post("/webhook/website")
@router.post("/webhook/form")
@router.post("/webhook/email")
async def handle_lead_capture(lead_data: LeadRequest):
    data = lead_data.dict()
    result = await process_lead(data, "website")
    return result

@router.post("/webhook/generate-qr")
async def generate_qr(campaign: str = Body("default")):
    qr_id = f"QR_{int(datetime.now().timestamp())}"
    qr_data = json.dumps({"qr_id": qr_id, "campaign": campaign})
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "status": "success",
        "qr_id": qr_id,
        "qr_image": f"data:image/png;base64,{qr_base64}"
    }

@router.post("/webhook/validate-qr")
async def validate_qr(qr_id: str = Body(...), name: str = Body(...), email: str = Body(""), phone: str = Body("")):
    lead_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "message": f"Scanned QR: {qr_id}"
    }
    result = await process_lead(lead_data, "qr_code")
    return {"status": "success", "lead_id": result["lead_id"], "category": result["category"]}

@router.get("/leads/recent")
async def get_recent_leads(limit: int = 10):
    results = await execute_query("""
        SELECT lead_id, source, name, email, lead_score, category, estimated_value, created_at
        FROM leads 
        ORDER BY created_at DESC 
        LIMIT ?
    """, limit)
    return results

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "Lead Rescue 360"}

@router.get("/metrics")
async def metrics():
    total = await execute_query("SELECT COUNT(*) as total FROM leads")
    return {"total_leads": total[0]["total"] if total else 0}

