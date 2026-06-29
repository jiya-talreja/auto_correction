from groq import Groq
from core.config import settings
client=Groq(api_key=settings.groq_api)
