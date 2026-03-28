import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

class JSONDatabase:
    """JSON-база данных, совместимая с GitHub Pages и локальным сервером"""
    
    def __init__(self, db_path: str = "db/sotikdima1975-star"):
        self.db_path = db_path
        self.schema_file = os.path.join(db_path, "schema.json")
        self.tables = {}
        self._load_schema()
    
    def _load_schema(self):
        """Загружает схему БД"""
        try:
            with open(self.schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
                self.schema = schema
        except FileNotFoundError:
            print(f"Схема не найдена: {self.schema_file}")
    
    def _load_table(self, table_name: str):
        """Загружает таблицу из JSON файла"""
        table_file = os.path.join(self.db_path, f"{table_name}.json")
        try:
            with open(table_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_table(self, table_name: str, data: List[Dict]):
        """Сохраняет таблицу в JSON файл"""
        table_file = os.path.join(self.db_path, f"{table_name}.json")
        with open(table_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def insert(self, table_name: str, data: Dict) -> Optional[str]:
        """Добавляет новую запись в таблицу"""
        if table_name not in self.schema['tables']:
            raise ValueError(f"Таблица {table_name} не найдена в схеме")
        
        # Генерируем ID если его нет
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        
        # Добавляем временные метки
        data['created_at'] = datetime.utcnow().isoformat()
        if 'updated_at' not in data:
            data['updated_at'] = data['created_at']
        
        # Загружаем現現ноевое содержимое таблицы
        table = self._load_table(table_name)
        table.append(data)
        self._save_table(table_name, table)
        
        # Логируем операцию
        self._log("INSERT", f"Добавлена запись в {table_name}", {"id": data['id'], "table": table_name})
        
        return data['id']
    
    def find(self, table_name: str, **kwargs) -> List[Dict]:
        """Поиск записей по условиям"""
        table = self._load_table(table_name)
        results = []
        
        for record in table:
            match = True
            for key, value in kwargs.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                results.append(record)
        
        return results
    
    def find_one(self, table_name: str, **kwargs) -> Optional[Dict]:
        """Поиск первой записи по условиям"""
        results = self.find(table_name, **kwargs)
        return results[0] if results else None
    
    def update(self, table_name: str, record_id: str, data: Dict) -> bool:
        """Обновляет запись"""
        table = self._load_table(table_name)
        updated = False
        
        for i, record in enumerate(table):
            if record.get('id') == record_id:
                record.update(data)
                record['updated_at'] = datetime.utcnow().isoformat()
                table[i] = record
                updated = True
                break
        
        if updated:
            self._save_table(table_name, table)
            self._log("UPDATE", f"Обновлена запись в {table_name}", {"id": record_id, "table": table_name})
        
        return updated
    
    def delete(self, table_name: str, record_id: str) -> bool:
        """Удаляет запись"""
        table = self._load_table(table_name)
        new_table = [r for r in table if r.get('id') != record_id]
        
        if len(new_table) < len(table):
            self._save_table(table_name, new_table)
            self._log("DELETE", f"Удалена запись из {table_name}", {"id": record_id, "table": table_name})
            return True
        
        return False
    
    def get_all(self, table_name: str) -> List[Dict]:
        """Получает все записи из таблицы"""
        return self._load_table(table_name)
    
    def _log(self, operation: str, message: str, data: Dict = None):
        """Логирует операцию"""
        log_entry = {
            "id": str(uuid.uuid4()),
            "type": operation,
            "message": message,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        logs = self._load_table("logs")
        logs.append(log_entry)
        self._save_table("logs", logs)


# Пример использования
if __name__ == "__main__":
    db = JSONDatabase()
    
    # Добавление пользователя
    user_id = db.insert("users", {
        "username": "testuser",
        "email": "test@example.com"
    })
    print(f"Создан пользователь: {user_id}")
    
    # Поиск пользователя
    user = db.find_one("users", id=user_id)
    print(f"Найден пользователь: {user}")
    
    # Обновление пользователя
    db.update("users", user_id, {"email": "newemail@example.com"})
    
    # Все пользователи
    all_users = db.get_all("users")
    print(f"Всего пользователей: {len(all_users)}")
