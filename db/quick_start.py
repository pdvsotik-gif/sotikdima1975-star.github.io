"""
Быстрый старт: SQL Server синхронизация
Запусти это для первоначальной настройки
"""

from db.sql_server_sync import SQLServerSync
import sys

print("\n" + "=" * 70)
print("🗄️  SQL SERVER СИНХРОНИЗАЦИЯ - ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА")
print("=" * 70 + "\n")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ШАГИ НАСТРОЙКИ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("📋 СЛЕДУЙ ИНСТРУКЦИЯМ:\n")

# Шаг 1: Параметры SQL Server
print("ШАГ 1️⃣ : Введи параметры SQL Server")
print("-" * 70)

server = input("   Server name (e.g., LAPTOP-ABC\\SQLEXPRESS или .\\SQLEXPRESS): ").strip()
if not server:
    server = ".\\SQLEXPRESS"
    print(f"   [используется default: {server}]")

username = input("   Username (default 'sa'): ").strip()
if not username:
    username = "sa"

password = input("   Password: ").strip()
if not password:
    print("   ⚠️  Пароль не введен!")
    sys.exit(1)

print()

# Создай синхронизатор
sync = SQLServerSync(
    server=server,
    database='sotikdima1975_star',
    username=username,
    password=password,
    json_db_path='db/sotikdima1975-star'
)

# Шаг 2: Тест соединения
print("ШАГ 2️⃣ : Тест соединения с SQL Server")
print("-" * 70)

if not sync.test_connection():
    print("\n❌ ОШИБКА: Не удалось подключиться к SQL Server")
    print("\nПроверь:")
    print("   • Запущен ли SQL Server Service")
    print("   • Верно ли указан server name")
    print("   • Правильно ли введены username/password")
    print("   • Установлен ли ODBC Driver 17")
    sys.exit(1)

print()

# Шаг 3: Создание таблиц
print("ШАГ 3️⃣ : Создание таблиц в SQL Server")
print("-" * 70)

if sync.create_tables():
    print("\n✓ Таблицы успешно созданы!\n")
else:
    print("\n❌ Ошибка при создании таблиц\n")
    sys.exit(1)

# Шаг 4: Синхронизация
print("ШАГ 4️⃣ : Синхронизация JSON → SQL Server")
print("-" * 70)

sync.sync_all_json_to_sql()
print()

# Шаг 5: Сравнение
print("ШАГ 5️⃣ : Проверка синхронизации")
print("-" * 70)
print()

sync.compare_databases()

# Завершение
print("\n" + "=" * 70)
print("✅ НАСТРОЙКА ЗАВЕРШЕНА!")
print("=" * 70)

print("""
🎯 ЧТО ДАЛЬШЕ:

1. Открой SQL Server Management Studio (SSMS)
   • Подключись к: соответствующему server name
   • База данных: sotikdima1975_star
   • Проверь таблицы: users, donations, logs

2. Используй синхронизацию:
   • JSON → SQL Server: sync.sync_all_json_to_sql()
   • SQL Server → JSON: sync.sync_all_sql_to_json()
   • Сравнить: sync.compare_databases()

3. Автоматическая синхронизация (опционально):
   • Запусти: python db/sync_scheduled.py
   • Добавь в Windows Task Scheduler для самозапуска

4. Помощь:
   • Документация: db/SQL_SERVER_SETUP.md
   • Агент: /database-manager

📚 Полная документация в: db/README.md
""")

print("=" * 70)
