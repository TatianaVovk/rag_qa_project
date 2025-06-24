# # query_service/llm_loader.py

# from configs.config import USE_MOCK_LLM, GGUF_MODEL_PATH

# if USE_MOCK_LLM:
#     def ask_model(prompt: str) -> str:
#         """
#         Мок-функция генерации ответа (используется при отладке или слабом железе).
#         """
#         return f"[МОК] Ответ на запрос: {prompt[:100]}..."
# else:
#     from ctransformers import AutoModelForCausalLM

#     print("Загружаем локальную LLM...")
#     llm = AutoModelForCausalLM.from_pretrained(
#         GGUF_MODEL_PATH,
#         model_type="mistral",
#         model_file=GGUF_MODEL_PATH,
#         gpu_layers=0,   # на слабом железе – обязательно 0
#         threads=4       # можно снизить до 2, если тормозит
#     )

#     def ask_model(prompt: str) -> str:
#         """
#         Генерация ответа с использованием локальной LLM.
#         """
#         return llm(prompt, max_new_tokens=512, temperature=0.7)
# query_service/llm_loader.py

import requests
from configs.config import USE_MOCK_LLM,COLAB_LLM_URL, GGUF_MODEL_PATH



#COLAB_LLM_URL = "https://4bda-34-87-189-151.ngrok-free.app/generate"  


if USE_MOCK_LLM:
    def ask_model(prompt):
        return f"[МОК] Ответ: {prompt}"
        
else:
    def ask_model(prompt):
        try:
                response = requests.post(
                    COLAB_LLM_URL,
                    json={"prompt": prompt},
                    timeout=300
                )
                response.raise_for_status()
                return response.json()["answer"]
        except Exception as e:
                return f"⚠️ Ошибка при вызове модели: {e}"
      
