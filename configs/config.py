from pathlib import Path
import os


# Пути к данным
DATA_DIR = Path("data")
RAW_DATA_PATH = DATA_DIR / "RuBQ_2.0_paragraphs.json"
CLEAN_DATA_PATH = DATA_DIR / "cleaned_text_chunks.json"

# Параметры очистки текста
MIN_TEXT_LENGTH = 20

# Настройки LLM
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"
COLAB_LLM_URL = os.getenv("COLAB_LLM_URL", "http://localhost:7860/generate")
GGUF_MODEL_PATH = "llm_models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# Hugging Face Inference API
HF_API_TOKEN = "HF_API_TOKEN" # Добавьте токен Hugging Face (подробности в README.md)
HF_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"

