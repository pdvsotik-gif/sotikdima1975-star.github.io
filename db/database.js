/**
 * JSONDatabase - универсальная JSON-база данных для GitHub Pages и локального сервера
 * Работает как в браузере, так и на сервере Node.js
 */

class JSONDatabase {
    constructor(dbPath = '/db/sotikdima1975-star', apiEndpoint = null) {
        this.dbPath = dbPath;
        this.apiEndpoint = apiEndpoint;
        this.schema = null;
        this.cache = new Map();
        this.cacheExpiry = 3600000; // 1 час
    }

    /**
     * Инициализирует БД - загружает схему
     */
    async init() {
        try {
            this.schema = await this._fetchFile('schema.json');
            console.log('✓ БД инициализирована', this.schema);
        } catch (error) {
            console.error('✗ Ошибка инициализации БД:', error);
        }
    }

    /**
     * Загружает файл (JSON)
     */
    async _fetchFile(filename) {
        const cacheKey = `file:${filename}`;
        
        // Проверяем кэш
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheExpiry) {
                return cached.data;
            }
        }

        try {
            const url = `${this.dbPath}/${filename}`;
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Кэшируем результат
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });
            
            return data;
        } catch (error) {
            console.error(`Ошибка при загрузке ${filename}:`, error);
            throw error;
        }
    }

    /**
     * Сохраняет файл (требует API на сервере)
     */
    async _saveFile(filename, data) {
        if (!this.apiEndpoint) {
            console.warn('API endpoint не установлен. Используй: db.apiEndpoint = "http://localhost:3000"');
            return false;
        }

        try {
            const response = await fetch(`${this.apiEndpoint}/api/save`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file: filename,
                    data: data
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            // Инвалидируем кэш
            this.cache.delete(`file:${filename}`);
            
            return true;
        } catch (error) {
            console.error(`Ошибка при сохранении ${filename}:`, error);
            return false;
        }
    }

    /**
     * Генерирует UUID
     */
    _generateId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Добавляет запись в таблицу
     */
    async insert(tableName, data) {
        if (!this.schema || !this.schema.tables[tableName]) {
            throw new Error(`Таблица ${tableName} не найдена`);
        }

        // Генерируем ID если не задан
        if (!data.id) {
            data.id = this._generateId();
        }

        // Добавляем временные метки
        data.created_at = new Date().toISOString();
        data.updated_at = data.created_at;

        // Загружаем таблицу
        const table = await this._fetchFile(`${tableName}.json`);
        table.push(data);

        // Сохраняем
        const saved = await this._saveFile(`${tableName}.json`, table);
        
        if (saved) {
            this._log('INSERT', `Добавлена запись в ${tableName}`, { id: data.id, table: tableName });
        }

        return data.id;
    }

    /**
     * Ищет записи по условиям
     */
    async find(tableName, conditions = {}) {
        const table = await this._fetchFile(`${tableName}.json`);
        
        return table.filter(record => {
            return Object.entries(conditions).every(([key, value]) => {
                return record[key] === value;
            });
        });
    }

    /**
     * Ищет первую запись по условиям
     */
    async findOne(tableName, conditions = {}) {
        const results = await this.find(tableName, conditions);
        return results.length > 0 ? results[0] : null;
    }

    /**
     * Получает запись по ID
     */
    async findById(tableName, id) {
        return this.findOne(tableName, { id });
    }

    /**
     * Обновляет запись
     */
    async update(tableName, recordId, data) {
        const table = await this._fetchFile(`${tableName}.json`);
        let found = false;

        const updated = table.map(record => {
            if (record.id === recordId) {
                found = true;
                return {
                    ...record,
                    ...data,
                    updated_at: new Date().toISOString(),
                    id: record.id,
                    created_at: record.created_at
                };
            }
            return record;
        });

        if (found) {
            const saved = await this._saveFile(`${tableName}.json`, updated);
            if (saved) {
                this._log('UPDATE', `Обновлена запись ${recordId} в ${tableName}`, { id: recordId, table: tableName });
            }
        }

        return found;
    }

    /**
     * Удаляет запись
     */
    async delete(tableName, recordId) {
        const table = await this._fetchFile(`${tableName}.json`);
        const filtered = table.filter(record => record.id !== recordId);

        if (filtered.length < table.length) {
            const saved = await this._saveFile(`${tableName}.json`, filtered);
            if (saved) {
                this._log('DELETE', `Удалена запись ${recordId} из ${tableName}`, { id: recordId, table: tableName });
            }
            return true;
        }

        return false;
    }

    /**
     * Получает все записи из таблицы
     */
    async getAll(tableName) {
        return this._fetchFile(`${tableName}.json`);
    }

    /**
     * Копирует логирование
     */
    async _log(operation, message, data = {}) {
        try {
            const logs = await this._fetchFile('logs.json');
            logs.push({
                id: this._generateId(),
                type: operation,
                message: message,
                data: data,
                timestamp: new Date().toISOString()
            });
            await this._saveFile('logs.json', logs);
        } catch (error) {
            console.warn('Не удалось залогировать операцию:', error);
        }
    }

    /**
     * Очищает кэш
     */
    clearCache() {
        this.cache.clear();
        console.log('✓ Кэш очищен');
    }
}

// Экспорт для Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JSONDatabase;
}
