# cleaner.py
import re

# Регулярка для поиска битых и невидимых юникод-символов
SUSPICIOUS_UNICODE_RE = re.compile(r"[\u200b\u200c\u200d\u200e\u200f\u202a-\u202e\ufeff\ufffd]", flags=re.UNICODE)

def clean_text(text: str) -> str:
    """
    Расширенная очистка текста:
    - убирает пробелы по краям
    - заменяет переносы строк на пробелы
    - удаляет невидимые и битые символы (но сохраняет языки, фонетику и валюты)
    - убирает лишние пробелы внутри
    """
    text = text.strip().replace('\n', ' ')
    text = SUSPICIOUS_UNICODE_RE.sub('', text)
    text = re.sub(r"\s+", " ", text)
    return text

def is_suspicious(text: str) -> bool:
    """
    Определяет, содержит ли текст подозрительные невидимые/битые юникод-символы.
    """
    return bool(SUSPICIOUS_UNICODE_RE.search(text))
