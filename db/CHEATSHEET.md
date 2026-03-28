# 🗄️ JSON + SQL Server — Глобальный Чит-лист

## 📍 Где хранятся данные?

```
📁 db/
├── 📁 sotikdima1975-star/
│   ├── users.json          ← JSON таблица (GitHub Pages)
│   ├── donations.json
│   ├── logs.json
│   ├── schema.json         ← Структура БД
│   └── config.json
├── database.py             ← Python для JSON
├── database.js             ← JavaScript для JSON
├── sql_server_sync.py      ← Синхронизация JSON ↔ SQL Server ⭐
├── quick_start.py          ← Первоначальная настройка ⭐
├── README.md               ← JSON полная документация
└── SQL_SERVER_SETUP.md     ← SQL Server инструкция ⭐
```

---

## 🚀 БЫСТРЫЙ СТАРТ

### 1️⃣ Первая настройка (один раз)

```bash
# Интерактивная настройка SQL Server
python db/quick_start.py
```

**Ответь на вопросы:**
- Server name: `LAPTOP-ABC\SQLEXPRESS` или `..\SQLEXPRESS`
- Username: `sa` (обычно)
- Password: твой пароль SQL Server

✓ Таблицы создаются автоматически
✓ JSON данные импортируются в SQL Server

### 2️⃣ Синхронизация (регулярно)

```bash
# Импортировать JSON → SQL Server
python -c "
from db.sql_server_sync import SQLServerSync
sync = SQLServerSync('LAPTOP-ABC\\\\SQLEXPRESS', 'sotikdima1975_star', 'sa', 'password')
sync.sync_all_json_to_sql()
sync.compare_databases()
"

# Или наоборот: SQL Server → JSON
python -c "
from db.sql_server_sync import SQLServerSync
sync = SQLServerSync('LAPTOP-ABC\\\\SQLEXPRESS', 'sotikdima1975_star', 'sa', 'password')
sync.sync_all_sql_to_json()
"
```

---

## 🔧 ОСНОВНЫЕ ОПЕРАЦИИ

### JSON (JavaScript для GitHub Pages)

```javascript
const db = new JSONDatabase('/db/sotikdima1975-star');
await db.init();

// Добавить
const id = await db.insert('users', {username: 'john', email: 'john@example.com'});

// Найти
const user = await db.findOne('users', {username: 'john'});
const all = await db.getAll('users');

// Обновить
await db.update('users', id, {email: 'newemail@example.com'});

// Удалить
await db.delete('users', id);
```

### JSON (Python для сервера)

```python
from db.database import JSONDatabase

db = JSONDatabase('db/sotikdima1975-star')

# Добавить
id = db.insert('users', {'username': 'john', 'email': 'john@example.com'})

# Найти
user = db.find_one('users', username='john')
all = db.get_all('users')

# Обновить
db.update('users', id, {'email': 'newemail@example.com'})

# Удалить
db.delete('users', id)
```

### SQL Server (T-SQL в SSMS)

```sql
USE sotikdima1975_star;

-- Найти
SELECT * FROM users WHERE username = 'john';

-- Добавить
INSERT INTO users (id, username, email) 
VALUES (NEWID(), 'jane', 'jane@example.com');

-- Обновить
UPDATE users SET email = 'jane.new@example.com' WHERE username = 'jane';

-- Удалить
DELETE FROM users WHERE username = 'jane';

-- Статистика
SELECT COUNT(*) as total_users FROM users;
SELECT SUM(amount) as total_donations FROM donations WHERE status = 'completed';
```

### SQL Server → JSON (Python)

```python
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync('LAPTOP-ABC\\SQLEXPRESS', 'sotikdima1975_star', 'sa', 'password')

# Одна таблица
sync.sql_to_json('users')

# Все таблицы
sync.sync_all_sql_to_json()
```

---

## 🗺️ АРХИТЕКТУРА

```
┌─────────────────────────────────────────────────────┐
│                  GitHub Pages                       │
│                  (браузер)                          │
└──────────────────────┬────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────┐
│           JSON БД (читать/писать)                   │
│     - users.json                                    │
│     - donations.json                                │
│     - logs.json                                     │
└──────────────────────┬────────────────────────────┘
                       │
              СИНХРОНИЗАЦИЯ
         (json_to_sql / sql_to_json)
                       │
                       ↓
┌─────────────────────────────────────────────────────┐
│          SQL Server (основное)                      │
│     - users (T-SQL таблица)                         │
│     - donations (T-SQL таблица)                     │
│     - logs (T-SQL таблица)                          │
└──────────────────────┬────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────┐
│           Локальный сервер                          │
│     - SQL запросы                                   │
│     - Анализ данных                                 │
│     - API для приложений                            │
│     - Резервные копии                               │
└─────────────────────────────────────────────────────┘
```

---

## ⚡ КОМАНДЫ

### Тестирование соединения

```python
from db.sql_server_sync import SQLServerSync
sync = SQLServerSync('SERVER_NAME', 'sotikdima1975_star', 'USERNAME', 'PASSWORD')
sync.test_connection()  # ✓ или ✗
```

### Синхронизация

```python
# Все направления
sync.sync_all_json_to_sql()  # JSON → SQL Server
sync.sync_all_sql_to_json()  # SQL Server → JSON

# Отдельные таблицы
sync.json_to_sql('users')
sync.sql_to_json('donations')

# Сравнение
sync.compare_databases()
```

### Статистика

```python
sync.get_json_stats()   # {'users': 5, 'donations': 12, ...}
sync.get_sql_stats()    # {'users': 5, 'donations': 12, ...}
```

---

## 📊 ТАБЛИЦЫ

### users
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

### donations
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "amount": "number",
  "currency": "RUB|USD|EUR",
  "status": "pending|completed|failed",
  "created_at": "ISO-8601"
}
```

### logs
```json
{
  "id": "uuid",
  "type": "INSERT|UPDATE|DELETE",
  "message": "string",
  "data": "object",
  "timestamp": "ISO-8601"
}
```

---

## 🔑 SQL SERVER НАСТРОЙКА

| Параметр | Значение | Пример |
|----------|----------|--------|
| Server | Server name | `LAPTOP-ABC\SQLEXPRESS` |
| Database | БД имя | `sotikdima1975_star` |
| Username | SQL User | `sa` |
| Password | SQL Password | `YourPassword123` |

**Где найти server name?**
1. Открой SQL Server Management Studio
2. В диалоге "Connect to Server" → Server name поле

---

## 🐛 ДЕБАГ

### Ошибка: "Login failed"
```
✗ Проверь username/password
✗ Убедись что SQL Server запущен
✗ Переподключись в SSMS с теми же credentials
```

### Ошибка: "Server not found"
```
✗ Скопируй точный Server name из SSMS
✗ Используй: LAPTOP-ABC\SQLEXPRESS (с кавычками если есть пробел)
✗ Или: .\SQLEXPRESS для локального
```

### Ошибка: "ODBC Driver not found"
```
✗ Установи: ODBC Driver 17 for SQL Server
✗ Ссылка: https://learn.microsoft.com/sql/connect/odbc/...
```

### Ошибка: "Database does not exist"
```
✗ Запусти: sync.create_tables()
✗ Или используй quick_start.py
```

---

## 📚 ДОКУМЕНТАЦИЯ

| Файл | Для | Содержание |
|------|-----|-----------|
| [README.md](db/README.md) | JSON API | Полная документация JSON БД |
| [SQL_SERVER_SETUP.md](db/SQL_SERVER_SETUP.md) | SQL Server | Полная инструкция синхронизации |
| [quick_start.py](db/quick_start.py) | Новички | Интерактивная первоначальная настройка |
| [sql_server_sync.py](db/sql_server_sync.py) | Разработчики | Исходный код синхронизатора |

---

## 🤖 АГЕНТ

Для управления БД используй:
```
/database-manager
```

Примеры:
- "Добавь нового пользователя с email test@example.com"
- "Синхронизируй JSON → SQL Server"
- "Покажи последние 10 пожертвований"
- "Мигрируй данные из CSV"

---

## 📋 ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ

### Q: Какую базу использовать?
**Q:** GitHub Pages? → JSON
**Q:** Локальное приложение? → SQL Server (и JSON для синхронизации)
**Q:** Both? → JSON + SQL Server с синхронизацией

### Q: Как часто синхронизировать?
- Раз в день (автоматически через Task Scheduler)
- Раз в час (через schedule Python)
- Вручную перед/после важных операций

### Q: Отключится ли JSON если используется SQL Server?
**A:** Нет! JSON остается основным для GitHub Pages. SQL Server подстраховка и для сложных операций.

### Q: Потеряются ли данные при синхронизации?
**A:** Нет. Но всегда делай бэкап перед массовыми операциями:
```python
import shutil
shutil.copy('db/sotikdima1975-star/users.json', 'db/sotikdima1975-star/users.json.backup')
```

---

## ✅ ЧЕК-ЛИСТ

- [ ] Установлен SQL Server Management Studio
- [ ] Установлен ODBC Driver 17
- [ ] Найден твой Server Name
- [ ] Запущен `python db/quick_start.py`
- [ ] Тест соединения пройден ✓
- [ ] Таблицы созданы в SQL Server
- [ ] JSON данные импортированы
- [ ] Сравнение показывает синхронизацию

**Готово! 🎉**

---

**Última обновление:** 2026-03-23
**Версия:** 1.0.0
