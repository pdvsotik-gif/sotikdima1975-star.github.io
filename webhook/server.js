const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Создаём папку для логов, если её нет
if (!fs.existsSync('webhook/logs')) {
    fs.mkdirSync('webhook/logs', { recursive: true });
}

// Middleware для парсинга JSON (если donate.stream отправляет данные в JSON)
app.use(express.json());

// Middleware для парсинга application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// CORS — разрешаем запросы с вашего сайта
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

// Основной маршрут для вебхука
app.post('/webhook/donate', (req, res) => {
    const data = req.body;
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] Новый донат: ${JSON.stringify(data)}\n`;

    // Сохраняем в файл
    fs.appendFile('webhook/logs/donates.log', logEntry, (err) => {
        if (err) {
            console.error('Ошибка записи в лог:', err);
        }
    });

    // Выводим в консоль
    console.log('Получен донат:', data);

    // Ответ серверу
    res.status(200).send('OK');
});

// Простая страница для проверки
app.get('/', (req, res) => {
    res.send(`
        <h1>Webhook для СайтСотика</h1>
        <p>✅ Сервер запущен. Отправьте POST-запрос на <code>http://localhost:3000/webhook/donate</code></p>
    `);
});

// Запуск сервера
app.listen(PORT, () => {
    console.log(`
🚀 Webhook-сервер запущен: http://localhost:${PORT}
📌 Отправляйте данные на: http://localhost:${PORT}/webhook/donate
📁 Логи донатов сохраняются в: webhook/logs/donates.log

💡 Чтобы использовать в интернете — нужен хостинг (Vercel, Render, Railway и т.п.)
    `);
});