# JSON База Данных - `sotikdima1975-star`

Универсальная JSON-база данных, работающая как на **GitHub Pages** (браузер), так и на **локальном сервере** (Python/Node.js).

## 📁 Структура

```
db/
├── sotikdima1975-star/
│   ├── schema.json        # Описание структуры БД
│   ├── users.json         # Таблица пользователей
│   ├── donations.json     # Таблица пожертвований
│   ├── logs.json          # Логи операций
│   └── config.json        # Конфигурация
├── database.py            # Python API для сервера
└── database.js            # JavaScript API для браузера/Node.js
```

## 🚀 Быстрый старт

### Python (локальный сервер)

```python
from db.database import JSONDatabase

# Инициализация
db = JSONDatabase()

# Добавить пользователя
user_id = db.insert("users", {
    "username": "john_doe",
    "email": "john@example.com"
})

# Найти пользователя
user = db.find_one("users", id=user_id)
print(user)

# Обновить пользователя
db.update("users", user_id, {"email": "new@example.com"})

# Получить всех пользователей
users = db.get_all("users")

# Удалить пользователя
db.delete("users", user_id)
```

### JavaScript (браузер/GitHub Pages)

```javascript
// Инициализация
const db = new JSONDatabase('/db/sotikdima1975-star');
await db.init();

// Добавить запись (требует API на сервере)
db.apiEndpoint = 'http://localhost:3000';
const userId = await db.insert('users', {
    username: 'jane_doe',
    email: 'jane@example.com'
});

// Найти записи
const user = await db.findOne('users', { username: 'jane_doe' });
console.log(user);

// Получить по ID
const userById = await db.findById('users', userId);

// Обновить
await db.update('users', userId, { email: 'jane.new@example.com' });

// Получить все
const allUsers = await db.getAll('users');

// Удалить
await db.delete('users', userId);

// Очистить кэш
db.clearCache();
```

### Node.js (локальный сервер)

```javascript
const JSONDatabase = require('./db/database.js');

const db = new JSONDatabase('./db/sotikdima1975-star');
await db.init();

// Используй как в браузере, но без apiEndpoint
const users = await db.getAll('users');
```

## 📊 Поддерживаемые таблицы

### users.json
Данные о пользователях.

```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp"
}
```

**Методы:**
- `db.insert('users', {...})`
- `db.find('users', {username: 'john'})`
- `db.findOne('users', {email: 'john@example.com'})`
- `db.findById('users', 'user-id')`
- `db.update('users', 'user-id', {...})`
- `db.delete('users', 'user-id')`
- `db.getAll('users')`

### donations.json
История пожертвований.

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "amount": "number",
  "currency": "string",
  "status": "string (pending/completed/failed)",
  "created_at": "ISO-8601 timestamp"
}
```

**Пример:**
```python
db.insert("donations", {
    "user_id": "user-123",
    "amount": 100,
    "currency": "RUB",
    "status": "completed"
})
```

### logs.json
Логи всех операций с БД.

```json
{
  "id": "uuid",
  "type": "string (INSERT/UPDATE/DELETE)",
  "message": "string",
  "data": "object",
  "timestamp": "ISO-8601 timestamp"
}
```

**Автоматически заполняется** при каждой операции.

## ⚙️ Конфигурация

`config.json` содержит настройки:

```json
{
  "environment": "development",
  "api_endpoint": "http://localhost:3000",
  "github_pages": {
    "url": "https://sotikdima1975-star.github.io",
    "branch": "main"
  },
  "sync_interval": 300,
  "cache_ttl": 3600
}
```

- `environment`: `development` (локально) или `production` (GitHub Pages)
- `api_endpoint`: URL локального API сервера
- `sync_interval`: Интервал синхронизации в секундах
- `cache_ttl`: Время жизни кэша в секундах

## 🔗 Интеграция

### С Express.js (Node.js сервер)

```javascript
const express = require('express');
const JSONDatabase = require('./db/database.js');

const app = express();
const db = new JSONDatabase('./db/sotikdima1975-star');

app.use(express.json());

// Сохранение файлов БД
app.post('/api/save', (req, res) => {
    const { file, data } = req.body;
    const fs = require('fs');
    const path = require('path');
    
    const filepath = path.join('./db/sotikdima1975-star', file);
    fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
    
    res.json({ success: true });
});

// GET api
app.get('/api/:table', async (req, res) => {
    const { table } = req.params;
    const data = await db.getAll(table);
    res.json(data);
});

app.listen(3000, () => {
    console.log('✓ Сервер запущен на http://localhost:3000');
});
```

### С Flask (Python сервер)

```python
from flask import Flask, jsonify, request
from db.database import JSONDatabase
import os

app = Flask(__name__)
db = JSONDatabase()

@app.route('/api/<table>', methods=['GET'])
def get_table(table):
    return jsonify(db.get_all(table))

@app.route('/api/<table>', methods=['POST'])
def insert_record(table):
    data = request.get_json()
    record_id = db.insert(table, data)
    return jsonify({'id': record_id}), 201

@app.route('/api/<table>/<record_id>', methods=['PUT'])
def update_record(table, record_id):
    data = request.get_json()
    db.update(table, record_id, data)
    return jsonify({'success': True})

@app.route('/api/<table>/<record_id>', methods=['DELETE'])
def delete_record(table, record_id):
    db.delete(table, record_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
```

## 🤖 Использование с Agent

Для управления БД используй специализированный агент **Database Manager**:

```
/database-manager
```

Этот агент оптимизирован для:
- CRUD операций с таблицами
- Поиска и фильтрации данных
- Миграции и изменения схемы
- Синхронизации между GitHub Pages и сервером
- Анализа логов

**Примеры запросов:**
- "Добавь нового пользователя с email admin@example.com"
- "Найди все пожертвования больше 500 рублей"
- "Мигрируй данные из donations.csv в donations.json"
- "Покажи последние 10 операций в логах"

## 🔄 Синхронизация GitHub Pages ↔ Локальный сервер

### Двусторонняя синхронизация

1. **GitHub Pages → Локальный сервер**
   ```python
   # Пол получить свежие данные
   db.clearCache()  # Очистить кэш
   users = db.get_all('users')
   ```

2. **Локальный сервер → GitHub Pages**
   ```python
   # Коммит в GitHub
   # git add db/
   # git commit -m "Update database"
   # git push origin main
   ```

### Автоматическая синхронизация

Используй GitHub Actions для синхронизации каждые `sync_interval` секунд:

```yaml
name: Sync Database
on:
  schedule:
    - cron: '*/5 * * * *'  # Каждые 5 минут

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sync database
        run: |
          curl http://localhost:3000/api/users > db/sotikdima1975-star/users.json
          git add db/
          git commit -m "Auto sync database" || true
          git push
```

## 📝 API Методы

### Все методы асинхронные в JavaScript

| Метод | Python | JavaScript | Описание |
|-------|--------|------------|---------|
| `init()` | - | `await db.init()` | Инициализация, загрузка схемы |
| `insert(table, data)` | `db.insert()` | `await db.insert()` | Добавить запись |
| `find(table, **kwargs)` | `db.find()` | `await db.find()` | Найти записи по условиям |
| `findOne(table, **kwargs)` | `db.find_one()` | `await db.findOne()` | Найти первую запись |
| `findById(table, id)` | - | `await db.findById()` | Найти по ID |
| `update(table, id, data)` | `db.update()` | `await db.update()` | Обновить запись |
| `delete(table, id)` | `db.delete()` | `await db.delete()` | Удалить запись |
| `getAll(table)` | `db.get_all()` | `await db.getAll()` | Получить все записи |

## 🐛 Дебаг и Логирование

### View логов

```python
# Python
logs = db.get_all('logs')
for log in logs:
    print(f"{log['type']}: {log['message']}")
```

```javascript
// JavaScript
const logs = await db.getAll('logs');
logs.forEach(log => {
    console.log(`${log.type}: ${log.message}`);
});
```

### Очистка БД

```python
# Полная очистка (ОСТОРОЖНО!)
db._save_table('users', [])
db._save_table('donations', [])
db._save_table('logs', [])
```

## 📚 Примеры использования

### Подсчет пожертвований

```python
donations = db.find('donations', status='completed')
total = sum(d['amount'] for d in donations)
print(f"Всего пожертвовано: {total}")
```

### Экспорт в CSV

```python
import csv

users = db.get_all('users')
with open('users_export.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'username', 'email', 'created_at'])
    writer.writeheader()
    writer.writerows(users)
```

### Статистика по дням

```javascript
const donations = await db.getAll('donations');
const byDate = {};

donations.forEach(d => {
    const date = new Date(d.created_at).toLocaleDateString();
    byDate[date] = (byDate[date] || 0) + d.amount;
});

console.log(byDate);
```

## ⚠️ Важные замечания

1. **JSON не блокируется** - при одновременных записях может быть конфликт
2. **Производительность** - БД замедляется при файлах > 10MB
3. **Безопасность** - не храни чувствительные данные (пароли) в JSON
4. **Валидация** - всегда валидируй данные перед сохранением
5. **Кэширование** - JavaScript кэширует данные на 1 час по умолчанию

## 🔐 Безопасность

- Используй HTTPS для API запросов
- Защити API эндпоинты аутентификацией
- Логируй все операции (автоматически)
- Исключи sensitive данные из логов

```python
# Пример: не логируй пароли
sensitive_fields = ['password', 'api_key', 'token']
def safe_data(data):
    return {k: v for k, v in data.items() if k not in sensitive_fields}
```

---

**Для вопросов и помощи используй агент `Database Manager` - просто напиши `/database-manager`**
