import json
import re
from pathlib import Path
from indexing_service.data_loader import load_raw_data, save_cleaned_data
from indexing_service.cleaner import clean_text, is_suspicious



from configs.config import RAW_DATA_PATH, CLEAN_DATA_PATH, MIN_TEXT_LENGTH, DATA_DIR


def log_stats(stats: dict):
    """
    Выводит статистику фильтрации.
    """
    print("\nСтатистика очистки:")
    print(f"  Всего исходных текстов: {stats['total']}")
    print(f"  Пустые тексты удалены (до очистки): {stats['empty']}")
    print(f"  Удалены до очистки с битым юникодом: {stats['bad_unicode']}")
    print(f"  Слишком короткие тексты удалены: {stats['too_short']}")
    print(f"  Дубликаты по ID удалены: {stats['duplicate_ids']}")
    print(f"  Дубликаты по тексту удалены: {stats['duplicate_texts']}")
    print(f"  Осталось после очистки: {stats['valid']}")

def preprocess_text_chunks(chunks: list) -> list:
    """
    Очищает и фильтрует текстовые блоки (чанки):
    - удаляет пустые и короткие записи (<20 символов)
    - удаляет дубликаты по ID и по тексту
    - логирует количество удалённых текстов по каждой причине
    - оставляет только id и очищенный текст
    """
    cleaned = []
    seen_ids = set()
    seen_texts = set()

    stats = {
        "total": len(chunks),
        "too_short": 0,
        "empty": 0,
        "bad_unicode": 0,
        "duplicate_ids": 0,
        "duplicate_texts": 0,
        "valid": 0
    }

    for item in chunks:
        chunk_id = item.get("uid")
        raw_text = item.get("text", "")

        # Явная проверка на пустые или "псевдопустые" строки до очистки
        if not raw_text or not raw_text.strip():
            stats["empty"] += 1
            continue

        # 💥 Проверка на битые символы ДО очистки
        if is_suspicious(raw_text):
            stats["bad_unicode"] += 1
            continue

        # Очистка текста
        text = clean_text(raw_text)

        if not text.strip():
            stats["empty"] += 1
            continue

        if len(text) < MIN_TEXT_LENGTH:
            stats["too_short"] += 1
            continue

        if chunk_id in seen_ids:
            stats["duplicate_ids"] += 1
            continue

        if text in seen_texts:
            stats["duplicate_texts"] += 1
            continue

        cleaned.append({"id": chunk_id, "text": text})
        seen_ids.add(chunk_id)
        seen_texts.add(text)
        stats["valid"] += 1

    log_stats(stats)
    return cleaned

if __name__ == "__main__":
    # Убедимся, что папка data существует
    Path(DATA_DIR).mkdir(exist_ok=True)

    raw = load_raw_data(RAW_DATA_PATH)
    cleaned = preprocess_text_chunks(raw)
    save_cleaned_data(cleaned, CLEAN_DATA_PATH)

    print("\nОчистка завершена.")












