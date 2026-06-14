async def score_lead(lead: dict) -> dict:
    """Score lead using keyword matching"""
    
    message = lead.get("message", "").lower()
    
    # Hot keywords - ready to buy
    hot_words = ["buy", "purchase", "urgent", "now", "asap", "immediately", "demo", "call", "price"]
    warm_words = ["maybe", "later", "research", "info", "learn", "how", "what", "interested"]
    
    score = 50
    category = "warm"
    
    if any(word in message for word in hot_words):
        score = 85
        category = "hot"
    elif any(word in message for word in warm_words):
        score = 65
        category = "warm"
    else:
        score = 30
        category = "cold"
    
    # Adjust for message length
    if len(message) > 50:
        score = min(score + 10, 100)
    
    return {
        "score": score,
        "category": category,
        "budget": "high" if category == "hot" else "medium" if category == "warm" else "low",
        "urgency": "high" if category == "hot" else "medium" if category == "warm" else "low",
        "intent": "ready_to_buy" if category == "hot" else "researching",
        "estimated_value": 10000 if category == "hot" else 2500 if category == "warm" else 500
    }

