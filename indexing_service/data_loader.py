import json


def load_raw_data(path: str) -> list:
    """
    Загружает JSON-файл с текстовыми блоками (чанками).
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_cleaned_data(text_chunks: list, out_path: str):
    """
    Сохраняет очищенные текстовые блоки в JSON.
    """
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(text_chunks, f, ensure_ascii=False, indent=2)
