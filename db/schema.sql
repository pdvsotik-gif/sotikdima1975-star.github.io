-- ============================================================
-- SQL Server Schema для БД: sotikdima1975_star
-- Версия: 1.0.0
-- Дата: 2026-03-23
-- ============================================================

-- Использовать master БД для создания новой БД
USE master;
GO

-- Проверить существует ли БД, если да - удалить
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'sotikdima1975_star')
BEGIN
    ALTER DATABASE sotikdima1975_star SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE sotikdima1975_star;
END
GO

-- Создать новую БД
CREATE DATABASE sotikdima1975_star;
GO

USE sotikdima1975_star;
GO

-- ============================================================
-- ТАБЛИЦА 1: USERS (Пользователи)
-- ============================================================
CREATE TABLE users (
    -- Первичный ключ
    id NVARCHAR(36) PRIMARY KEY,
    
    -- Основные поля
    username NVARCHAR(100) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    
    -- Прозрачность и аудит
    created_at DATETIME2 DEFAULT GETUTCDATE() NOT NULL,
    updated_at DATETIME2 DEFAULT GETUTCDATE() NOT NULL,
    
    -- Индекс по email для быстрого поиска
    INDEX idx_users_email (email),
    INDEX idx_users_username (username),
    INDEX idx_users_created_at (created_at)
);

-- Вставить тестовых пользователей (опционально)
-- INSERT INTO users (id, username, email) 
-- VALUES (NEWID(), 'test_user', 'test@example.com');

PRINT '✓ Таблица users создана';
GO

-- ============================================================
-- ТАБЛИЦА 2: DONATIONS (Пожертвования)
-- ============================================================
CREATE TABLE donations (
    -- Первичный ключ
    id NVARCHAR(36) PRIMARY KEY,
    
    -- Внешний ключ на пользователя
    user_id NVARCHAR(36) NOT NULL,
    
    -- Данные пожертвования
    amount DECIMAL(10, 2) NOT NULL,
    currency NVARCHAR(3) DEFAULT 'RUB' NOT NULL,  -- RUB, USD, EUR
    status NVARCHAR(20) DEFAULT 'pending' NOT NULL,  -- pending, completed, failed
    
    -- Прозрачность
    created_at DATETIME2 DEFAULT GETUTCDATE() NOT NULL,
    
    -- Ограничения целостности
    CONSTRAINT fk_donations_user_id FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    
    -- Индексы для оптимизации
    INDEX idx_donations_user_id (user_id),
    INDEX idx_donations_status (status),
    INDEX idx_donations_created_at (created_at),
    INDEX idx_donations_amount (amount)
);

PRINT '✓ Таблица donations создана';
GO

-- ============================================================
-- ТАБЛИЦА 3: LOGS (Логи операций)
-- ============================================================
CREATE TABLE logs (
    -- Первичный ключ
    id NVARCHAR(36) PRIMARY KEY,
    
    -- Тип и описание операции
    type NVARCHAR(50) NOT NULL,  -- INSERT, UPDATE, DELETE
    message NVARCHAR(MAX),
    
    -- JSON данные операции
    data NVARCHAR(MAX),
    
    -- Временная метка
    timestamp DATETIME2 DEFAULT GETUTCDATE() NOT NULL,
    
    -- Индекс для поиска по времени
    INDEX idx_logs_timestamp (timestamp),
    INDEX idx_logs_type (type)
);

PRINT '✓ Таблица logs создана';
GO

-- ============================================================
-- TRIGGERS (Триггеры для автоматических операций)
-- ============================================================

-- Триггер: Автоматически обновлять updated_at при изменении users
CREATE TRIGGER trg_users_update
ON users
AFTER UPDATE
AS
BEGIN
    UPDATE users 
    SET updated_at = GETUTCDATE()
    WHERE id IN (SELECT id FROM inserted);
END;
GO

PRINT '✓ Триггер trg_users_update создан';
GO

-- ============================================================
-- VIEWS (Представления для удобства)
-- ============================================================

-- View 1: Пожертвования с информацией о пользователе
CREATE VIEW vw_donations_with_users AS
SELECT 
    d.id as donation_id,
    d.amount,
    d.currency,
    d.status,
    d.created_at as donation_date,
    u.id as user_id,
    u.username,
    u.email
FROM donations d
INNER JOIN users u ON d.user_id = u.id;
GO

PRINT '✓ View vw_donations_with_users создан';
GO

-- View 2: Статистика по пользователям
CREATE VIEW vw_users_statistics AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(d.id) as total_donations,
    SUM(CASE WHEN d.status = 'completed' THEN d.amount ELSE 0 END) as completed_amount,
    SUM(CASE WHEN d.status = 'pending' THEN d.amount ELSE 0 END) as pending_amount,
    MAX(d.created_at) as last_donation_date,
    u.created_at as user_created_date
FROM users u
LEFT JOIN donations d ON u.id = d.user_id
GROUP BY u.id, u.username, u.email, u.created_at;
GO

PRINT '✓ View vw_users_statistics создан';
GO

-- View 3: Статистика по статусам пожертвований
CREATE VIEW vw_donations_summary AS
SELECT 
    status,
    COUNT(*) as donation_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM donations
GROUP BY status;
GO

PRINT '✓ View vw_donations_summary создан';
GO

-- ============================================================
-- STORED PROCEDURES (Хранимые процедуры)
-- ============================================================

-- Procedure 1: Добавить пожертвование и залогировать
CREATE PROCEDURE sp_insert_donation
    @donation_id NVARCHAR(36),
    @user_id NVARCHAR(36),
    @amount DECIMAL(10, 2),
    @currency NVARCHAR(3) = 'RUB',
    @status NVARCHAR(20) = 'pending'
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Проверить что пользователь существует
        IF NOT EXISTS (SELECT 1 FROM users WHERE id = @user_id)
        BEGIN
            THROW 50001, 'Пользователь не найден', 1;
        END
        
        -- Вставить пожертвование
        INSERT INTO donations (id, user_id, amount, currency, status)
        VALUES (@donation_id, @user_id, @amount, @currency, @status);
        
        -- Залогировать операцию
        INSERT INTO logs (id, type, message, data, timestamp)
        VALUES (
            NEWID(),
            'INSERT',
            'Добавлено пожертвование',
            CONCAT('{"donation_id":"', @donation_id, '","user_id":"', @user_id, '","amount":', @amount, '}'),
            GETUTCDATE()
        );
        
        COMMIT TRANSACTION;
        PRINT CONCAT('✓ Пожертвование добавлено: ', @donation_id);
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

PRINT '✓ Procedure sp_insert_donation создана';
GO

-- Procedure 2: Получить статистику пользователя
CREATE PROCEDURE sp_get_user_stats
    @user_id NVARCHAR(36)
AS
BEGIN
    SELECT 
        u.id,
        u.username,
        u.email,
        COUNT(d.id) as total_donations,
        SUM(CASE WHEN d.status = 'completed' THEN 1 ELSE 0 END) as completed_donations,
        SUM(CASE WHEN d.status = 'completed' THEN d.amount ELSE 0 END) as total_completed_amount
    FROM users u
    LEFT JOIN donations d ON u.id = d.user_id
    WHERE u.id = @user_id
    GROUP BY u.id, u.username, u.email;
END
GO

PRINT '✓ Procedure sp_get_user_stats создана';
GO

-- ============================================================
-- CONSTRAINTS и правила целостности
-- ============================================================

-- Ограничение: Amount должен быть положительным
ALTER TABLE donations
ADD CONSTRAINT ck_donations_amount CHECK (amount > 0);

-- Ограничение: currency только из списка
ALTER TABLE donations
ADD CONSTRAINT ck_donations_currency 
    CHECK (currency IN ('RUB', 'USD', 'EUR', 'GBP', 'JPY', 'CNY', 'BTC'));

-- Ограничение: status из определенного набора
ALTER TABLE donations
ADD CONSTRAINT ck_donations_status 
    CHECK (status IN ('pending', 'completed', 'failed', 'cancelled'));

PRINT '✓ Constraints добавлены';
GO

-- ============================================================
-- РЕЗУЛЬТАТ
-- ============================================================
PRINT '';
PRINT '========================================';
PRINT '✓ БАЗА ДАННЫХ УСПЕШНО СОЗДАНА!';
PRINT '========================================';
PRINT '';
PRINT 'Таблицы:';
PRINT '  1. users (пользователи)';
PRINT '  2. donations (пожертвования)';
PRINT '  3. logs (логи операций)';
PRINT '';
PRINT 'Представления (Views):';
PRINT '  1. vw_donations_with_users';
PRINT '  2. vw_users_statistics';
PRINT '  3. vw_donations_summary';
PRINT '';
PRINT 'Процедуры (Procedures):';
PRINT '  1. sp_insert_donation';
PRINT '  2. sp_get_user_stats';
PRINT '';
PRINT 'Готово для синхронизации с JSON БД!';
PRINT '========================================';
GO

-- ============================================================
-- ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ (раскомментируй чтобы использовать)
-- ============================================================

/*
-- Добавить пользователя
INSERT INTO users (id, username, email)
VALUES (NEWID(), 'john_doe', 'john@example.com');

-- Добавить пожертвование
DECLARE @newDonationId NVARCHAR(36) = NEWID();
DECLARE @userId NVARCHAR(36) = (SELECT TOP 1 id FROM users);

EXEC sp_insert_donation 
    @donation_id = @newDonationId,
    @user_id = @userId,
    @amount = 500.00,
    @currency = 'RUB',
    @status = 'completed';

-- Получить статистику
EXEC sp_get_user_stats @user_id = @userId;

-- Просмотреть данные
SELECT * FROM users;
SELECT * FROM donations;
SELECT * FROM logs;
SELECT * FROM vw_donations_with_users;
SELECT * FROM vw_users_statistics;
SELECT * FROM vw_donations_summary;
*/
