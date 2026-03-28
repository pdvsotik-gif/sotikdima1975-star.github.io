"""
Синхронизация между JSON БД и Microsoft SQL Server
Поддерживает двустороннюю синхронизацию JSON ↔ SQL Server
"""

import json
import pyodbc
from datetime import datetime
from typing import List, Dict, Optional
import logging
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class SQLServerSync:
    """Синхронизирует JSON БД с Microsoft SQL Server"""
    
    def __init__(self, server: str, database: str, username: str, password: str, 
                 json_db_path: str = "db/sotikdima1975-star"):
        """
        Инициализация синхронизатора
        
        Args:
            server: SQL Server hostname (e.g., 'localhost' или 'LAPTOP-ABC\\SQLEXPRESS')
            database: Database name
            username: SQL Server username
            password: SQL Server password
            json_db_path: Путь к JSON БД
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.json_db_path = json_db_path
        self.connection_string = (
            f'Driver={{ODBC Driver 17 for SQL Server}};'
            f'Server={server};'
            f'Database={database};'
            f'UID={username};'
            f'PWD={password};'
        )
        
        # Поддерживаемые таблицы
        self.tables = {
            'users': {
                'fields': ['id', 'username', 'email', 'created_at', 'updated_at']
            },
            'donations': {
                'fields': ['id', 'user_id', 'amount', 'currency', 'status', 'created_at']
            },
            'logs': {
                'fields': ['id', 'type', 'message', 'data', 'timestamp']
            }
        }
    
    def test_connection(self) -> bool:
        """Тестирует соединение с SQL Server"""
        try:
            conn = pyodbc.connect(self.connection_string, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT @@version")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            logger.info(f"✓ Соединение успешно: {version[:50]}...")
            return True
        except Exception as e:
            logger.error(f"✗ Ошибка соединения: {e}")
            return False
    
    def create_tables(self) -> bool:
        """Создает таблицы в SQL Server"""
        sql_scripts = {
            'users': """
                IF OBJECT_ID('users', 'U') IS NOT NULL DROP TABLE users;
                CREATE TABLE users (
                    id NVARCHAR(36) PRIMARY KEY,
                    username NVARCHAR(100) NOT NULL,
                    email NVARCHAR(100) UNIQUE NOT NULL,
                    created_at DATETIME2 DEFAULT GETUTCDATE(),
                    updated_at DATETIME2 DEFAULT GETUTCDATE()
                );
                CREATE INDEX idx_users_email ON users(email);
            """,
            'donations': """
                IF OBJECT_ID('donations', 'U') IS NOT NULL DROP TABLE donations;
                CREATE TABLE donations (
                    id NVARCHAR(36) PRIMARY KEY,
                    user_id NVARCHAR(36) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    currency NVARCHAR(3) DEFAULT 'RUB',
                    status NVARCHAR(20) DEFAULT 'pending',
                    created_at DATETIME2 DEFAULT GETUTCDATE(),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                CREATE INDEX idx_donations_user_id ON donations(user_id);
                CREATE INDEX idx_donations_created_at ON donations(created_at);
            """,
            'logs': """
                IF OBJECT_ID('logs', 'U') IS NOT NULL DROP TABLE logs;
                CREATE TABLE logs (
                    id NVARCHAR(36) PRIMARY KEY,
                    type NVARCHAR(50) NOT NULL,
                    message NVARCHAR(MAX),
                    data NVARCHAR(MAX),
                    timestamp DATETIME2 DEFAULT GETUTCDATE()
                );
                CREATE INDEX idx_logs_timestamp ON logs(timestamp);
            """
        }
        
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            for table_name, script in sql_scripts.items():
                cursor.execute(script)
                logger.info(f"✓ Таблица {table_name} создана")
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"✗ Ошибка при создании таблиц: {e}")
            return False
    
    def json_to_sql(self, table_name: str) -> bool:
        """
        Импортирует данные из JSON в SQL Server
        JSON → SQL Server
        """
        try:
            json_file = os.path.join(self.json_db_path, f"{table_name}.json")
            
            if not os.path.exists(json_file):
                logger.warning(f"JSON файл не найден: {json_file}")
                return False
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                logger.info(f"✓ {table_name}: JSON пуст, SQL таблица очищена")
                return True
            
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            # Очищаем таблицу перед импортом
            cursor.execute(f"TRUNCATE TABLE {table_name}")
            
            # Вставляем данные
            for record in data:
                columns = ', '.join(record.keys())
                placeholders = ', '.join(['?' for _ in record])
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(record.values()))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✓ {table_name}: JSON → SQL Server ({len(data)} записей)")
            return True
        
        except Exception as e:
            logger.error(f"✗ Ошибка при импорте {table_name}: {e}")
            return False
    
    def sql_to_json(self, table_name: str) -> bool:
        """
        Экспортирует данные из SQL Server в JSON
        SQL Server → JSON
        """
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY created_at DESC")
            
            # Получаем названия колонок
            columns = [description[0] for description in cursor.description]
            
            # Получаем данные
            data = []
            for row in cursor.fetchall():
                record = {col: val for col, val in zip(columns, row)}
                # Конвертируем datetime в ISO format
                for key, value in record.items():
                    if isinstance(value, datetime):
                        record[key] = value.isoformat()
                data.append(record)
            
            cursor.close()
            conn.close()
            
            # Сохраняем в JSON
            json_file = os.path.join(self.json_db_path, f"{table_name}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✓ {table_name}: SQL Server → JSON ({len(data)} записей)")
            return True
        
        except Exception as e:
            logger.error(f"✗ Ошибка при экспорте {table_name}: {e}")
            return False
    
    def sync_all_json_to_sql(self) -> bool:
        """Синхронизирует все таблицы: JSON → SQL Server"""
        logger.info("=" * 60)
        logger.info("СИНХРОНИЗАЦИЯ: JSON → SQL Server")
        logger.info("=" * 60)
        
        success = True
        for table_name in self.tables.keys():
            if not self.json_to_sql(table_name):
                success = False
        
        if success:
            logger.info("✓ Синхронизация завершена успешно")
        return success
    
    def sync_all_sql_to_json(self) -> bool:
        """Синхронизирует все таблицы: SQL Server → JSON"""
        logger.info("=" * 60)
        logger.info("СИНХРОНИЗАЦИЯ: SQL Server → JSON")
        logger.info("=" * 60)
        
        success = True
        for table_name in self.tables.keys():
            if not self.sql_to_json(table_name):
                success = False
        
        if success:
            logger.info("✓ Синхронизация завершена успешно")
        return success
    
    def get_sql_stats(self) -> Dict[str, int]:
        """Получает статистику таблиц SQL Server"""
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            stats = {}
            for table_name in self.tables.keys():
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                stats[table_name] = count
            
            cursor.close()
            conn.close()
            return stats
        except Exception as e:
            logger.error(f"✗ Ошибка при получении статистики: {e}")
            return {}
    
    def get_json_stats(self) -> Dict[str, int]:
        """Получает статистику JSON файлов"""
        stats = {}
        for table_name in self.tables.keys():
            json_file = os.path.join(self.json_db_path, f"{table_name}.json")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    stats[table_name] = len(data)
            except:
                stats[table_name] = 0
        return stats
    
    def compare_databases(self):
        """Сравнивает JSON и SQL Server"""
        logger.info("=" * 60)
        logger.info("СРАВНЕНИЕ БД: JSON vs SQL Server")
        logger.info("=" * 60)
        
        json_stats = self.get_json_stats()
        sql_stats = self.get_sql_stats()
        
        print(f"\n{'Таблица':<20} {'JSON':<10} {'SQL Server':<10} {'Статус':<20}")
        print("-" * 60)
        
        for table in self.tables.keys():
            json_count = json_stats.get(table, 0)
            sql_count = sql_stats.get(table, 0)
            
            if json_count == sql_count:
                status = "✓ Синхронизирована"
            else:
                status = f"✗ Отличается ({json_count - sql_count})"
            
            print(f"{table:<20} {json_count:<10} {sql_count:<10} {status:<20}")


# Примеры использования
if __name__ == "__main__":
    # ============================================
    # КОНФИГУРАЦИЯ SQL SERVER
    # ============================================
    
    # Вариант 1: Локальный SQL Server Express
    sync = SQLServerSync(
        server='LAPTOP-ABC\\SQLEXPRESS',  # Замени на свой server name
        database='sotikdima1975_star',
        username='sa',  # Замени на свой username
        password='your_password',  # Замени на свой password
        json_db_path='db/sotikdima1975-star'
    )
    
    # Вариант 2: Azure SQL Server
    # sync = SQLServerSync(
    #     server='your_server.database.windows.net',
    #     database='sotikdima1975_star',
    #     username='admin@your_server',
    #     password='your_password'
    # )
    
    # ============================================
    # ИСПОЛЬЗУЙ ОДИН ИЗ ЭТИХ СЦЕНАРИЕВ:
    # ============================================
    
    # 1. Тест соединения
    if sync.test_connection():
        
        # 2. Создать таблицы (выполни один раз)
        sync.create_tables()
        
        # 3. Синхронизация JSON → SQL Server
        sync.sync_all_json_to_sql()
        
        # 4. Синхронизация SQL Server → JSON
        # sync.sync_all_sql_to_json()
        
        # 5. Сравнить БД
        sync.compare_databases()
