from google import genai
from google.genai import types

from app.config import settings

class GeminiClient:
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("Gemini_API_KEY is not set. Copy .env.example to .env and add your key in .env")
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def chat(self, prompt: str, system: str | None = None) -> str:
        config  = ( types.GenerateContentConfig(system_instructions=system) if system else None )
        response = self._client.models.generate_content(
            model=settings.gemini_chat_model, contents = prompt, config=config
        )
        return response.text

    def embed(self, text: str) -> list[float]:
        result = self._client.models.embed_content(
            model=settings.gemini_embed_model, contents=text
        )
        return result.embeddings[0].values

    def ping(self) -> str:
        return self.chat("reply with the single word: ping").strip()

_client: GeminiClient | None = None

def get_llm() -> GeminiClient:
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client