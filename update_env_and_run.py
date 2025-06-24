import os
import shutil
import subprocess
from datetime import datetime

# Пути
COLAB_ENV = "llm_env.env"
TARGET_ENV = ".env"
BACKUP_ENV = f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def print_header(msg):
    print("\n" + "="*50)
    print(f"{msg}")
    print("="*50 + "\n")

def update_env():
    # Проверяем наличие файла из Colab
    if not os.path.exists(COLAB_ENV):
        print("❌ Не найден файл llm_env.env. Сначала скачай его из Colab.")
        return False

    # Бэкап текущего .env
    if os.path.exists(TARGET_ENV):
        shutil.copy(TARGET_ENV, BACKUP_ENV)
        print(f"📦 Старый .env сохранён как: {BACKUP_ENV}")

    # Копируем новый .env
    shutil.copy(COLAB_ENV, TARGET_ENV)
    print("✅ Новый .env установлен из llm_env.env")
    return True

def run_docker():
    print_header("🚀 Запускаем docker-compose...")
    try:
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при запуске docker-compose: {e}")

def main():
    print_header("🔧 Обновление .env и запуск проекта")
    if update_env():
        run_docker()

if __name__ == "__main__":
    main()
