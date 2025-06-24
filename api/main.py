from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from query_service.search_engine import SearchEngine
from configs.config import USE_MOCK_LLM

from query_service.build_prompt import build_prompt

app = FastAPI()
engine = SearchEngine()  # загружаем векторную БД

# === Pydantic-модель запроса ===
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3  # по умолчанию искать 3 релевантных чанка


# === Pydantic-модель ответа ===
class QueryResponse(BaseModel):
    answer: str
    context: List[str]


# === Эндпоинт /query ===
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    results = engine.search(request.question, top_k=request.top_k)

    if not results:
        raise HTTPException(status_code=404, detail="Ничего не найдено по запросу")

    prompt = build_prompt(results, request.question)

    if USE_MOCK_LLM:
        answer = f"[МОК] Ответ на вопрос: '{request.question}'"
    else:
        # Здесь должен быть вызов реальной LLM (например, через ctransformers)
        from query_service.llm_loader import ask_model  
        answer = ask_model(prompt)

    return QueryResponse(
        answer=answer,
        context=[doc["text"] for doc in results]
    )
