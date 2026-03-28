# SQL Server Синхронизация — Пошаговая инструкция

Полная интеграция JSON БД с Microsoft SQL Server с двусторонней синхронизацией.

## 0️⃣ Предварительные требования

### Установи:
1. **Microsoft SQL Server** (Express, Developer или Standard Edition)
   - Скачать: https://www.microsoft.com/sql-server/sql-server-downloads
   - Или используй Azure SQL Server

2. **SQL Server Management Studio (SSMS)**
   - Скачать: https://learn.microsoft.com/sql/ssms/download-sql-server-management-studio-ssms

3. **ODBC Driver 17 for SQL Server**
   ```powershell
   # Обычно устанавливается вместе с SQL Server
   # Если нет - скачай отсюда:
   # https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server
   ```

4. **Python пакет pyodbc**
   ```bash
   pip install pyodbc
   ```

---

## 1️⃣ Найди Server Name в SQL Server Management Studio

1. Открой **SQL Server Management Studio**
2. В диалоге "Connect to Server" увидишь **Server name**
   - Локальный: `LAPTOP-ABC\SQLEXPRESS` 
   - Azure: `your_server.database.windows.net`

📸 **Скопируй ровный server name!**

---

## 2️⃣ Настрой скрипт синхронизации

Отредактируй `db/sql_server_sync.py`:

```python
sync = SQLServerSync(
    server='LAPTOP-ABC\\SQLEXPRESS',      # ← Твой server name
    database='sotikdima1975_star',        # ← Имя БД (создается автоматически)
    username='sa',                        # ← SQL Server username
    password='your_password',             # ← SQL Server password
    json_db_path='db/sotikdima1975-star'
)
```

### Примеры Server Names:

**Локальный SQL Server Express:**
```
LAPTOP-ABC\SQLEXPRESS
DESKTOP-XYZ123\SQLEXPRESS
.\SQLEXPRESS
(local)\SQLEXPRESS
localhost\SQLEXPRESS
```

**Azure SQL Server:**
```
myserver.database.windows.net
company-db.database.windows.net
```

**Удаленный сервер:**
```
192.168.1.100
server.example.com
```

---

## 3️⃣ Первоначальная настройка

### Шаг 1: Тест соединения

```bash
python db/sql_server_sync.py
```

**Ожидаемый результат:**
```
[2026-03-23 12:34:56,789] INFO: ✓ Соединение успешно: Microsoft SQL Server 2019 (RTM) - 15.0.2000.5...
```

Если ошибка — проверь:
- Запущен ли SQL Server Service
- Правильно ли указан server name
- Верные ли username/password
- Установлен ли ODBC Driver 17

### Шаг 2: Создание таблиц

Добавь в скрипт:

```python
if sync.test_connection():
    # Создать таблицы в SQL Server
    sync.create_tables()
```

**Ожидаемый результат:**
```
✓ Таблица users создана
✓ Таблица donations создана
✓ Таблица logs создана
```

Проверь в SSMS: объекты → базы данных → sotikdima1975_star → таблицы

---

## 4️⃣ Синхронизация данных

### A) JSON → SQL Server (импорт)

```python
# Когда ты хочешь загрузить JSON данные в SQL Server
sync.sync_all_json_to_sql()
```

```
[INFO] JSON → SQL Server синхронизация
✓ users: JSON → SQL Server (5 записей)
✓ donations: JSON → SQL Server (12 записей)
✓ logs: JSON → SQL Server (0 записей)
```

### B) SQL Server → JSON (экспорт)

```python
# Когда ты хочешь выгрузить SQL Server данные в JSON
sync.sync_all_sql_to_json()
```

```
[INFO] SQL Server → JSON синхронизация
✓ users: SQL Server → JSON (5 записей)
✓ donations: SQL Server → JSON (12 записей)
✓ logs: SQL Server → JSON (0 записей)
```

### C) Сравнить оба хранилища

```python
# Проверить статус синхронизации
sync.compare_databases()
```

```
СРАВНЕНИЕ БД: JSON vs SQL Server
Таблица           JSON       SQL Server    Статус
-------
users             5          5             ✓ Синхронизирована
donations         12         12            ✓ Синхронизирована
logs              0          0             ✓ Синхронизирована
```

---

## 5️⃣ Автоматическая синхронизация

### Вариант 1: Расписание (каждый час)

```python
import schedule
import time
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync(
    server='LAPTOP-ABC\\SQLEXPRESS',
    database='sotikdima1975_star',
    username='sa',
    password='your_password'
)

def sync_job():
    """Синхронизирует JSON → SQL Server каждый час"""
    print(f"\n[{datetime.now()}] Запуск синхронизации...")
    
    if sync.test_connection():
        sync.sync_all_json_to_sql()
        sync.compare_databases()

# Расписание
schedule.every(1).hours.do(sync_job)

# Запуск
print("✓ Синхронизация активирована (каждый час)")
while True:
    schedule.run_pending()
    time.sleep(60)
```

Установи `schedule`:
```bash
pip install schedule
```

### Вариант 2: Windows Task Scheduler (автозапуск)

Создай скрипт `sync_scheduled.py`:

```python
from datetime import datetime
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync(
    server='LAPTOP-ABC\\SQLEXPRESS',
    database='sotikdima1975_star',
    username='sa',
    password='your_password'
)

if sync.test_connection():
    print(f"[{datetime.now()}] Синхронизация JSON ↔ SQL Server...")
    sync.sync_all_json_to_sql()
    sync.compare_databases()
    print("✓ Завершено")
```

**Добавь в Windows Task Scheduler:**

1. Открой Task Scheduler (taskschd.msc)
2. Create Basic Task → Имя: "DBSync"
3. Trigger: Daily / Hourly (выбери интервал)
4. Action: Start program
   - Program: `C:\Python310\python.exe`
   - Arguments: `sync_scheduled.py`
   - Start in: `C:\Users\sotik\IdeaProjects\sotikdima1975-star.github.io`

---

## 6️⃣ Работа через SSMS

После синхронизации ты можешь:

### Просмотреть данные
```sql
USE sotikdima1975_star;

-- Все пользователи
SELECT * FROM users;

-- Пожертвования больше 100 рублей
SELECT * FROM donations WHERE amount > 100;

-- Последние операции
SELECT TOP 20 * FROM logs ORDER BY timestamp DESC;
```

### Добавить данные в SSMS

```sql
INSERT INTO users (id, username, email) 
VALUES (NEWID(), 'john_doe', 'john@example.com');

INSERT INTO donations (id, user_id, amount, currency, status)
VALUES (NEWID(), 
        (SELECT id FROM users WHERE username='john_doe'),
        500, 'RUB', 'completed');
```

### Экспортировать в JSON

```python
# Любые изменения в SSMS → JSON
sync.sql_to_json('users')  # Только таблица users
sync.sync_all_sql_to_json()  # Все таблицы
```

---

## 7️⃣ Архитектура (JSON + SQL Server)

```
GitHub Pages (браузер)
    ↓
    └─→ JSON БД (json_files)
        ├─ READ: fetch('/db/sotikdima1975-star/users.json')
        └─ WRITE: Через API на сервере

Локальный сервер (Node.js/Flask)
    ↓
    ├─→ JSON БД (для GitHub Pages)
    └─→ SQL Server (для приложения)
        ├─ High-load операции
        ├─ Complex queries
        ├─ Резервные копии
        └─ Reporting

Синхронизация:
    JSON ←→ SQL Server (schedule или по требованию)
```

---

## 8️⃣ Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `Login failed` | Неверные credentials | Проверь username/password в SSMS |
| `Server not found` | Неверный server name | Скопируй точный server name из SSMS |
| `Timeout expired` | SQL Server не запущен | Запусти SQL Server Service |
| `ODBC Driver not found` | Не установлен драйвер | Установи ODBC Driver 17 |
| `Database does not exist` | БД не создана | Запусти `sync.create_tables()` |

---

## 9️⃣ Бэкап и восстановление

### Бэкап SQL Server → JSON

```python
# Перед обновлением системы
sync.sql_to_json('users')
sync.sql_to_json('donations')
sync.sql_to_json('logs')

# JSON файлы теперь содержат полный бэкап
```

### Восстановление JSON → SQL Server

```python
# После сбоя
sync.create_tables()  # Пересоздать
sync.sync_all_json_to_sql()  # Восстановить из JSON
```

---

## 🔟 Python API для программирования

```python
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync(
    server='LAPTOP-ABC\\SQLEXPRESS',
    database='sotikdima1975_star',
    username='sa',
    password='your_password'
)

# Тест соединения
if sync.test_connection():
    print("✓ SQL Server доступен")

# Получить статистику
stats = sync.get_sql_stats()
print(f"Пользователей в БД: {stats['users']}")

# Импортировать одну таблицу
sync.json_to_sql('users')

# Экспортировать одну таблицу
sync.sql_to_json('donations')

# Сравнить
sync.compare_databases()

# Синхронизировать все
sync.sync_all_json_to_sql()
sync.sync_all_sql_to_json()
```

---

## 📞 Нужна помощь?

**Используй агент Database Manager:**
```
/database-manager
```

Он поможет с:
- Миграцией данных
- Синхронизацией
- SQL queries
- Структурой БД

---

**Status:** ✓ Готово к использованию JSON + SQL Server 🎉
