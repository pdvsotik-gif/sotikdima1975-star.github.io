# Webhook для СайтСотика

Принимает донаты от `donate.stream` и сохраняет в лог.

## Как использовать

1. Установите Node.js (если ещё не установлен)
2. Установите зависимости:
   ```bash
   npm install
   ```
3. Запустите сервер:
   ```bash
   npm start
   ```
4. Ваш webhook работает на:
   ```
   http://localhost:3000/webhook/donate
   ```

## Важно!

👉 **Локально** (`localhost`) `donate.stream` не сможет достучаться.  
Чтобы webhook работал публично — задеплойте его на:

- [Render](https://render.com)
- [Railway](https://railway.app)
- [Vercel](https://vercel.com) (с функциями)
- [Fly.io](https://fly.io)

После деплоя вы получите URL вида:
```
https://sotikdima-webhook.onrender.com/webhook/donate
```
— его и укажите в настройках `donate.stream`.  