import json
import os
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import numpy as np

# Пути
INPUT_PATH = "data/cleaned_text_chunks.json"
EMBEDDINGS_PATH = "vector_db/chunk_embeddings.npy"
IDS_PATH = "vector_db/chunk_ids.json"

# Загрузка модели
print("Загружаем модель...")
model = SentenceTransformer("intfloat/multilingual-e5-base")

# Загрузка очищенных данных
print("Загружаем текстовые чанки...")
with open(INPUT_PATH, encoding="utf-8") as f:
    chunks = json.load(f)

# Добавление префикса "passage: " и извлечение id
texts = [f"passage: {chunk['text']}" for chunk in chunks]
ids = [chunk['id'] for chunk in chunks]

# Генерация эмбеддингов
print("Генерация эмбеддингов...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=64, convert_to_numpy=True, normalize_embeddings=True)

# Сохранение
print("Сохраняем эмбеддинги и id...")
np.save(EMBEDDINGS_PATH, embeddings)
with open(IDS_PATH, "w", encoding="utf-8") as f:
    json.dump(ids, f, ensure_ascii=False, indent=2)

print("✅ Эмбеддинги успешно сохранены.")
