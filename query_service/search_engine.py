import json
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import sys

class SearchEngine:
    """
    Класс для поиска релевантных текстов по эмбеддингу запроса.
    Загружает эмбеддинги чанков и их ID, векторизует запрос и находит наиболее близкие чанки.
    """
    def __init__(self,
                 model_name: str = "intfloat/multilingual-e5-base",
                 embeddings_path: str = "vector_db/chunk_embeddings.npy",
                 ids_path: str = "vector_db/chunk_ids.json",
                 texts_path: str = "data/cleaned_text_chunks.json",
                 normalize_embeddings: bool = True):

        print("Загружаем модель...")
        self.model = SentenceTransformer(model_name)

        print("Загружаем эмбеддинги...")
        self.embeddings = np.load(embeddings_path)
        if isinstance(self.embeddings, np.ndarray):
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.embeddings = torch.tensor(self.embeddings, device=device)
        else:
            self.embeddings = self.embeddings.to(device)

        print("Загружаем ID...")
        with open(ids_path, encoding="utf-8") as f:
            self.ids = json.load(f)

        print("Загружаем тексты...")
        with open(texts_path, encoding="utf-8") as f:
            chunks = json.load(f)
            self.id2text = {chunk["id"]: chunk["text"] for chunk in chunks}

        if len(self.ids) != len(self.embeddings):
            raise ValueError("Число эмбеддингов не совпадает с числом ID")

        self.normalize_embeddings = normalize_embeddings
        print(f"✅ Загружено {len(self.embeddings)} эмбеддингов.")

    def search(self, query: str, top_k: int = 5):
        """
        Выполняет поиск ближайших чанков по запросу.
        Возвращает top_k наиболее похожих ID, тексты и оценки близости.
        """
        query_input = f"query: {query}"
        query_embedding = self.model.encode(
            query_input,
            convert_to_tensor=True,
            normalize_embeddings=self.normalize_embeddings,
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )

        # 🔥 Переносим эмбеддинги на тот же девайс
        device = query_embedding.device
        embeddings = self.embeddings.to(device)

        scores = util.cos_sim(query_embedding, embeddings)[0]
        top_results = torch.topk(scores, k=top_k)

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            chunk_id = self.ids[idx]
            chunk_text = self.id2text.get(chunk_id, "<текст не найден>")
            results.append({
                "id": chunk_id,
                "score": float(score),
                "text": chunk_text
            })

        return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Укажите запрос при запуске. Пример:\npython search_engine.py \"что такое машинное обучение\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    engine = SearchEngine()
    results = engine.search(query)

    print("\n▶️ Результаты поиска:")
    for res in results:
        print(f"\n🔹 ID: {res['id']} | Score: {res['score']:.3f}")
        print(f"Текст: {res['text'][:500]}{'...' if len(res['text']) > 500 else ''}")

