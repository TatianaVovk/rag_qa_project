def build_prompt(chunks, question):
    """
    Формирует промпт для LLM на основе текста чанков и вопроса.
    """
    context = "\n".join(f"- {chunk['text']}" for chunk in chunks)
    prompt = f"""Ты — ассистент, отвечающий на вопросы на основе контекста.
Если ответа нет в контексте, скажи, что не знаешь.

Контекст:
{context}

Вопрос: {question}
Ответ:"""
    return prompt
