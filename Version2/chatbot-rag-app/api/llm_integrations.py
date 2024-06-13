from langchain_community.chat_models import (
    ChatOpenAI,
    ChatVertexAI,
    AzureChatOpenAI,
    BedrockChat,
    ChatCohere,
)
from langchain_mistralai.chat_models import ChatMistralAI
import os
import vertexai
import boto3
import requests
import json

LLM_TYPE = os.getenv("LLM_TYPE", "ollama")

# Existing initialization functions...

def init_ollama_chat(temperature):
    OLLAMA_API_ENDPOINT = os.getenv("OLLAMA_API_ENDPOINT", "http://192.168.8.108:11434")
    GEMMA_MODEL = os.getenv("GEMMA_MODEL", "tinyllama")
    return OllamaChat(endpoint=OLLAMA_API_ENDPOINT, model=GEMMA_MODEL, temperature=temperature)

MAP_LLM_TYPE_TO_CHAT_MODEL = {
    "ollama": init_ollama_chat,
}

def get_llm(temperature=0.1):
    if not LLM_TYPE in MAP_LLM_TYPE_TO_CHAT_MODEL:
        raise Exception(
            "LLM type not found. Please set LLM_TYPE to one of: "
            + ", ".join(MAP_LLM_TYPE_TO_CHAT_MODEL.keys())
            + "."
        )

    return MAP_LLM_TYPE_TO_CHAT_MODEL[LLM_TYPE](temperature=temperature)

class OllamaChat:
    def __init__(self, endpoint, model, temperature=0):
        self.endpoint = endpoint
        self.model = model
        self.temperature = temperature

    def invoke(self, prompt):
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json={"model": self.model, "prompt": prompt, "temperature": self.temperature},
        )
        response.raise_for_status()
        return response.json()

    def stream(self, prompt):
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",  # Changed to /api/generate if /api/stream is not supported
                json={"model": self.model, "prompt": prompt, "temperature": self.temperature},
                stream=True,
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError as e:
                        logging.error(f"Failed to decode JSON line: {line}, error: {e}")
        except requests.ConnectionError as e:
            logging.error(f"Connection error: {e}")
            raise
        except requests.HTTPError as e:
            logging.error(f"HTTP error: {e}")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise
