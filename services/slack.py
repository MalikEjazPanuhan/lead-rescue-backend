from slack_sdk.web.async_client import AsyncWebClient
from config.settings import settings

client = AsyncWebClient(token=settings.SLACK_TOKEN) if settings.SLACK_TOKEN else None

async def send_slack(channel: str, text: str):
    if not settings.SLACK_TOKEN or settings.SLACK_TOKEN == "your_slack_token_here":
        print(f"\n📢 SLACK MESSAGE TO #{channel.upper()}:\n{text}\n{'='*50}")
        return True
    
    channel_id = settings.SLACK_CHANNELS.get(channel)
    if channel_id and client:
        try:
            await client.chat_postMessage(channel=channel_id, text=text)
            return True
        except Exception as e:
            print(f"Slack error: {e}")
            return False
    return False

