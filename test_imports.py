print("Testing imports...")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Request
from slack_sdk.web.async_client import AsyncWebClient
import asyncpg
import openai
print("✅ All imports successful!")