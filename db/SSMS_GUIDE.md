# SQL Server Management Studio (SSMS) — Использование

Пошаговое руководство как работать с БД в SSMS после синхронизации из JSON.

## 1. Подключение к БД

### Запусти SSMS
1. Найди **SQL Server Management Studio** в Windows Start Menu
2. Нажми **New Query** при запуске
3. Или откой уже существующее подключение

### Подключение

**Object Explorer → Connect → Database Engine**
```
Server name:    LAPTOP-ABC\SQLEXPRESS  (или твой server)
Authentication: SQL Server Authentication
                (или Windows Authentication)
Username:       sa  (или твой username)
Password:       ****
```

Нажми **Connect**

✓ Если успешно, увидишь дерево объектов слева

## 2. Выбор БД

В Object Explorer (левая панель):
```
Databases
├── (system databases)
└── sotikdima1975_star  ← Твоя БД
    ├── Tables
    │   ├── dbo.users
    │   ├── dbo.donations
    │   └── dbo.logs
    ├── Views
    ├── Stored Procedures
    └── ...
```

**Правый клик → New Query** чтобы открить редактор

## 3. Просмотр данных

### Способ 1: Через UI (быстро)

Right click на таблицу → **Select Top 1000 Rows**

```sql
SELECT TOP (1000) [id]
      ,[username]
      ,[email]
      ,[created_at]
      ,[updated_at]
  FROM [sotikdima1975_star].[dbo].[users]
```

✓ Видишь все данные в grid'е

### Способ 2: Через T-SQL (точно)

**New Query** (Ctrl+N) и напиши:

```sql
USE sotikdima1975_star;

SELECT * FROM users;
```

Нажми **Execute** (F5) или кнопка ▶

## 4. Основные операции

### READ (Чтение)

```sql
-- Все пользователи
USE sotikdima1975_star;
SELECT * FROM users;

-- С фильтром
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Соединение (joins)
SELECT 
    u.username,
    d.amount,
    d.created_at
FROM users u
JOIN donations d ON u.id = d.user_id
WHERE d.amount > 100;

-- Группировка
SELECT 
    status,
    COUNT(*) as count,
    SUM(amount) as total
FROM donations
GROUP BY status;

-- Последние записи
SELECT TOP 20 * FROM users ORDER BY created_at DESC;
```

### CREATE (Создание)

```sql
-- Добавить пользователя
INSERT INTO users (id, username, email)
VALUES (NEWID(), 'john_doe', 'john@example.com');

-- Проверить что добавилось
SELECT * FROM users WHERE username = 'john_doe';

-- Добавить пожертвование
INSERT INTO donations (id, user_id, amount, currency, status)
VALUES (
    NEWID(),
    (SELECT id FROM users WHERE username = 'john_doe'),
    500,
    'RUB',
    'completed'
);
```

### UPDATE (Обновление)

```sql
-- Обновить email
UPDATE users 
SET email = 'newemail@example.com'
WHERE username = 'john_doe';

-- Обновить несколько полей
UPDATE users
SET email = 'jane@example.com', updated_at = GETUTCDATE()
WHERE id = '123-456-789';

-- Проверить результат
SELECT * FROM users WHERE username = 'john_doe';
```

### DELETE (Удаление)

```sql
-- Удалить пользователя
DELETE FROM users WHERE username = 'john_doe';

-- Внимание! Сначала удали пожертвования (FK constraint)
DELETE FROM donations WHERE user_id = (SELECT id FROM users WHERE username = 'john_doe');
DELETE FROM users WHERE username = 'john_doe';

-- Или отключи constraint (опасно!)
ALTER TABLE donations NOCHECK CONSTRAINT ALL;
DELETE FROM users WHERE username = 'john_doe';
ALTER TABLE donations WITH CHECK CHECK CONSTRAINT ALL;
```

## 5. Анализ данных

### Статистика

```sql
-- Количество пользователей
SELECT COUNT(*) as total_users FROM users;

-- Количество пожертвований
SELECT COUNT(*) as total_donations FROM donations;

-- Сумма пожертвований
SELECT SUM(amount) as total_amount FROM donations WHERE status = 'completed';

-- Среднее пожертвование
SELECT AVG(amount) as average_donation FROM donations WHERE status = 'completed';

-- Максимальное и минимальное
SELECT 
    MAX(amount) as max_donation,
    MIN(amount) as min_donation
FROM donations;
```

### Отчеты

```sql
-- Пожертвования по пользователям
SELECT 
    u.username,
    COUNT(d.id) as donations_count,
    SUM(d.amount) as total_donated,
    MAX(d.created_at) as last_donation
FROM users u
LEFT JOIN donations d ON u.id = d.user_id
GROUP BY u.username
ORDER BY total_donated DESC;

-- Пожертвования по статусам
SELECT 
    status,
    COUNT(*) as count,
    SUM(amount) as total,
    AVG(amount) as average
FROM donations
GROUP BY status;

-- Пожертвования за последние 30 дней
SELECT * FROM donations
WHERE created_at >= DATEADD(DAY, -30, GETUTCDATE())
ORDER BY created_at DESC;
```

### Поиск дублей

```sql
-- Найти дублей по email'у
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Найти пользователей без пожертвований
SELECT * FROM users u
WHERE NOT EXISTS (SELECT 1 FROM donations d WHERE d.user_id = u.id);
```

## 6. Экспорт/Бэкап

### Экспортировать в Excel

1. Выполни SELECT запрос
2. Right click на результатах → **Export Data**
3. Выбери Excel / CSV
4. Сохрани файл

### Экспортировать в JSON

**В Python скрипте:**
```python
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync('LAPTOP-ABC\\SQLEXPRESS', 'sotikdima1975_star', 'sa', 'password')
sync.sql_to_json('users')  # → users.json
sync.sql_to_json('donations')  # → donations.json
```

### Бэкап БД

**Backup базы:**

Right click на БД → **Tasks → Back Up...**
```
Backup type: Full
Backup to: File  (выбери путь)
```

Или T-SQL:
```sql
BACKUP DATABASE sotikdima1975_star 
TO DISK = 'C:\Backup\sotikdima1975_star.bak'
WITH INIT, COMPRESSION;
```

## 7. Продвинутое

### Indexes

```sql
-- Посмотреть индексы на таблице
SELECT * FROM sys.indexes
WHERE object_id = OBJECT_ID('users');

-- Создать индекс
CREATE INDEX idx_users_email_created 
ON users(email, created_at);

-- Удалить индекс
DROP INDEX idx_users_email_created ON users;
```

### Execution Plan

Для анализа производительности запроса:

**Query → Include Actual Execution Plan** (Ctrl+L)

Потом Execute (F5) - будет план внизу

### Triggers

```sql
-- Trigger для автоматического обновления updated_at
CREATE TRIGGER trg_users_update
ON users
AFTER UPDATE
AS
BEGIN
    UPDATE users SET updated_at = GETUTCDATE()
    WHERE id IN (SELECT id FROM inserted);
END;
```

## 8. Темная тема и настройки

### Темная тема

**Tools → Options → Environment → General → Color theme → Dark**

### Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| Ctrl+N | New Query |
| F5 | Execute |
| Ctrl+L | Include Execution Plan |
| Ctrl+Shift+L | Чистка Find/Replace |
| Ctrl+Alt+D | Database Diagram |
| F4 | Properties |

## 9. Синхронизация с JSON

### После изменений в SSMS

Экспортировать обратно в JSON для GitHub Pages:

```bash
python -c "
from db.sql_server_sync import SQLServerSync
sync = SQLServerSync('LAPTOP-ABC\\\\SQLEXPRESS', 'sotikdima1975_star', 'sa', 'password')
sync.sync_all_sql_to_json()  # SQL Server → JSON
print('✓ Синхронизировано')
"
```

Или в Python:
```python
from db.sql_server_sync import SQLServerSync

sync = SQLServerSync('LAPTOP-ABC\\SQLEXPRESS', 'sotikdima1975_star', 'sa', 'password')
sync.sync_all_sql_to_json()  # Все таблицы
```

### Перед синхронизацией

Всегда проверяй что всё в порядке:

```sql
-- Проверка целостности данных
DBCC CHECKDB (sotikdima1975_star);

-- Статистика
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM donations;
SELECT COUNT(*) FROM logs;
```

## 10. Частые ошибки

| Ошибка | Решение |
|--------|---------|
| `USE` statement not in batch | Выдели весь текст и выполни F5 |
| Foreign key constraint fails | Удали зависимые записи сначала |
| Timeout | Запрос слишком долгий, добавь WHERE/LIMIT |
| Column not found | Проверь названия колонок (case-sensitive нет, но синтаксис тот же) |
| Incorrect syntax | Проверь синтаксис T-SQL (точка-запятая в конце) |

## 11. Быстрые снипеты

Сохрани их в SSMS для быстрого использования:

```sql
-- Snippet: Все пользователи
USE sotikdima1975_star;
SELECT * FROM users ORDER BY created_at DESC;

-- Snippet: Статистика пожертвований
SELECT status, COUNT(*) as cnt, SUM(amount) as total 
FROM donations GROUP BY status;

-- Snippet: Поиск по email
SELECT * FROM users WHERE email LIKE '%_email_%';

-- Snippet: Последние логи
SELECT TOP 50 * FROM logs ORDER BY timestamp DESC;
```

---

## Дополнительные ресурсы

- [Microsoft T-SQL Documentation](https://learn.microsoft.com/sql/t-sql/language-reference)
- [SSMS Keyboard Shortcuts](https://learn.microsoft.com/sql/ssms/sql-server-management-studio-keyboard-shortcuts)
- [Query Best Practices](https://learn.microsoft.com/sql/t-sql/queries/queries)

---

**Готово! 🎉 Теперь ты можешь полноценно работать с БД в SSMS**
