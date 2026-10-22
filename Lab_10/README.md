# Warehouse Manager (Система обліку складських запасів)

REST API застосунок для автоматизації та обліку складських операцій, побудований на базі **FastAPI**, **SQLAlchemy** та **Pydantic**. Проєкт повністю підготовлений до розгортання в production-середовищі (включно з контейнеризацією через Docker, управлінням через змінні середовища та CI/CD на GitHub Actions).

---

## 📋 Основні можливості (Features)
* **Управління товарами:** Створення нових товарів, перегляд списку запасів.
* **Складські операції:** Облік надходження товарів на склад (`incoming`) та списання (`write-off`).
* **Захист від помилок:** Валідація кількості запасів (заборона надмірного списання при нестачі товару).
* **Персистентність:** Зберігання даних за допомогою SQLite / реляційної бази даних.
* **Health Check:** Ендпоінт для моніторингу працездатності сервісу (`/health`).
* **Автоматизована перевірка та збірка:** Повноцінний CI/CD pipeline через GitHub Actions.

---

## 🛠 Технологічний стек
* **Python** 3.11+
* **FastAPI** (сучасний асинхронний вебфреймворк)
* **SQLAlchemy** (ORM для роботи з БД)
* **Pydantic / Pydantic Settings** (валідація даних та конфігурація)
* **Docker** (контейнеризація)
* **Ruff & Mypy** (лінтування та статична перевірка типів)
* **Pytest** (модульне тестування)

---

## ⚙️ Вимоги та встановлення (Installation)

1. Клонуйте репозиторій та перейдіть до папки проєкту:
   ```bash
   git clone [https://github.com/nainastiia/warehouse-manager.git](https://github.com/nainastiia/warehouse-manager.git)
   cd warehouse-manager
   ```
2. Створіть та активуйте віртуальне середовище:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # На Windows: .venv\Scripts\activate
   ```
3. Встановіть пакет у режимі розробки разом із інструментами для тестування (dev-dependencies):
   ```bash
   pip install --upgrade pip
   pip install -e ".[dev]"
   ```
# 4. Налаштування змінних середовища (.env)
cp .env.example .env

# 5. Запуск юніт-тестів та перевірка якості коду (лінт + типізація)
pytest -v
ruff check
ruff format --check
mypy src

# 6. Збірка дистрибутивних пакетів (wheel та sdist)
python -m build

# 7. Локальний запуск REST API застосунку
warehouse-manager
# Або через uvicorn напряму:
# uvicorn warehouse_manager.api:app --reload

# 8. Збірка та запуск у Docker-контейнері (в іншій вкладці термінала)
docker build -t warehouse-manager:1.0 .
docker run --rm -p 8000:8000 \
  -v warehouse_data:/app/data \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  -e DATABASE_URL=sqlite:////app/data/app.db \
  warehouse-manager:1.0