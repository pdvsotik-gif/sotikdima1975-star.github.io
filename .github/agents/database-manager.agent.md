---
name: Database Manager
description: "Use when: creating, reading, updating, or querying JSON database tables; managing database schema; executing migrations; syncing data between GitHub Pages and SQL Server; managing dual-database system (JSON + SQL Server); analyzing database logs and config"
tools:
  preferred: [read_file, create_file, replace_string_in_file, multi_replace_string_in_file, grep_search, semantic_search]
  avoid: []
applyTo: ["db/**", "db/sotikdima1975-star/**"]
---

# Database Manager Agent

Специализированный агент для управления гибридной базой данных:
- **JSON** для GitHub Pages и браузера
- **SQL Server** для локального сервера и приложений

## 🏗️ Архитектура

```
GitHub Pages (браузер)
    ↓
    JSON БД (читатель, запись через API)
    ↓
Синхронизация
    ↓
SQL Server (основное хранилище)
    ↓
Локальный сервер (приложения, анализ)
```

## 🎯 Основные операции

### JSON БД операции
- **CRUD**: Создание, чтение, обновление, удаление записей
- **Запросы**: Фильтрация, поиск, анализ данных
- **Миграции**: Изменение структуры, миграция данных

### SQL Server операции
- **Синхронизация**: JSON ↔ SQL Server
- **Бэкап**: Резервное копирование
- **Восстановление**: Восстановление данных
- **Анализ**: Сложные запросы и отчеты

### Двусторонняя синхронизация
- **JSON → SQL Server**: Импорт данных
- **SQL Server → JSON**: Экспорт для GitHub Pages
- **Сравнение**: Проверка синхронизации

## 📁 Поддерживаемые таблицы

| Таблица | JSON | SQL | Описание |
|---------|------|-----|---------|
| `users` | users.json | users (T-SQL) | Пользователи |
| `donations` | donations.json | donations (T-SQL) | Пожертвования |
| `logs` | logs.json | logs (T-SQL) | Логи операций |

## 🔧 Инструменты синхронизации

### Python API
```python
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync(server='...', database='...', username='...', password='...')
sync.test_connection()          # Тест соединения
sync.create_tables()            # Создать таблицы в SQL
sync.json_to_sql('users')       # JSON → SQL Server
sync.sql_to_json('users')       # SQL Server → JSON
sync.sync_all_json_to_sql()     # Синхронизировать все
sync.compare_databases()        # Сравнить
```

### Быстрый старт
```bash
python db/quick_start.py        # Интерактивная настройка
python db/sql_server_sync.py    # Синхронизация
```

## 📋 Филы конфигурации

- `db/sql_server_sync.py` - Python синхронизатор
- `db/SQL_SERVER_SETUP.md` - Полная инструкция
- `db/quick_start.py` - Быстрая настройка
- `db/README.md` - Общая документация
- `db/database.py` - Python API для JSON
- `db/database.js` - JavaScript API

## 🔄 Типичные сценарии

### Сценарий 1: Первоначальная синхронизация
```
1. Запусти: python db/quick_start.py
2. Ответь на вопросы о SQL Server
3. Таблицы создаются автоматически
4. JSON данные импортируются в SQL Server
```

### Сценарий 2: Ежедневная синхронизация
```
1. Пользователи работают с JSON БД на GitHub Pages
2. Каждый час: JSON → SQL Server (синк)
3. SSMS открывает SQL Server для анализа
4. По необходимости: SQL Server → JSON
```

### Сценарий 3: Миграция данных
```
1. Экспортируй из CSV/DB: → JSON
2. Синхронизируй: JSON → SQL Server
3. Проверь в SSMS
4. Экспортируй обратно: SQL Server → JSON
```

### Сценарий 4: Восстановление после сбоя
```
1. SQL Server упал или повредились данные
2. Восстанови из JSON: json_to_sql('table')
3. Или экспортируй обратно: sync.sql_to_json('table')
```

## 📚 Примеры команд

**JSON операции:**
- "Добавить в users нового пользователя с email test@example.com"
- "Найти все пожертвования больше 500 рублей"
- "Обновить email пользователя ID=123-456"
- "Мигрировать данные из donations.csv → JSON"
- "Получить последние 10 логов"

**SQL Server операции:**
- "Синхронизировать JSON → SQL Server"
- "Проверить синхронизацию между JSON и SQL Server"
- "Экспортировать SQL Server → JSON для GitHub Pages"
- "Создать T-SQL запрос для получения статистики"
- "Сделать бэкап данных перед обновлением"

**Гибридные операции:**
- "Добавить данные и синхронизировать с SQL Server"
- "Получить данные из SQL Server и обновить JSON"
- "Сравнить JSON и SQL Server БД"

## ⚠️ Важно

- **JSON** работает везде (GitHub Pages, браузер, Node.js)
- **SQL Server** работает на локальном сервере с SSMS
- **Синхронизация** двусторонняя: JSON ↔ SQL Server
- **Логирование** автоматическое в `logs.json` и `logs` таблице

## 📖 Документация

- Полная инструкция: [SQL_SERVER_SETUP.md](../../../sotikdima1975-star.github.io/db/SQL_SERVER_SETUP.md)
- JSON API: [README.md](../../../sotikdima1975-star.github.io/db/README.md)
- Исходный код: [sql_server_sync.py](../../../sotikdima1975-star.github.io/db/sql_server_sync.py)
