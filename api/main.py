from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lead-rescue")

app = FastAPI(title="Lead Rescue 360", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Lead Rescue 360 API", "status": "running", "version": "1.0.0"}

@app.on_event("startup")
async def startup():
    logger.info("🚀 Lead Rescue 360 API Started")

    