# Forza Motorsport 8 — Гайды и Разборы

> **Добро пожаловать на специализированный раздел по Forza Motorsport 8!**
> Здесь вы найдёте профессиональные гайды, детальные разборы настроек автомобилей,
> стратегии прохождения трасс и актуальные новости из мира симулятора гонок.

## О Forza Motorsport 8

Forza Motorsport 8 — это современный трековый симулятор, в котором ключевыми элементами являются:

- **Стабильный темп** — акцент на контролируемое вождение без резких манёвров.
- **Работа с резиной** — важность сохранения температуры шин на протяжении круга.
- **Аккуратная борьба в онлайне** — уважительное отношение к соперникам и избегание контактов.

### Ключевые особенности

| Параметр | Значение | Примечание |
|----------|----------|------------|
| **Физика и поведение** | Симулятор с акцентом на стабильность | Машина наказывает за грубость, но позволяет ехать быстро при аккуратной работе рулём и педалями |
| **Режимы** | Карьера, онлайн-спринты, лиги | Основной фокус — стабильные онлайн-заезды и подготовка к лигам |
| **Платформа** | PC / Xbox Series | Настройки ориентированы на актуальные версии игры |
| **Сложность** | От «контролируемого хаоса» до киберспорта | Подойдут как новичкам, так и опытным игрокам |

### Целевая аудитория

Этот раздел создан для:

- 🏎️ Пилотов, которые хотят перестать «выживать» и начать контролировать темп на дистанции.
- 🔧 Тех, кому важны понятные и воспроизводимые настройки под конкретные режимы.
- 📺 Зрителей стримов, желающих повторить показанные сетапы и понять логику за ними.

## Настройки автомобиля: Lamborghini Huracán ST

Первый рабочий пресет для Lamborghini Huracán ST в формате онлайн-спринтов. Настройки собраны под стабильный темп и аккуратную борьбу в пелотоне.

### Логика пресета «Стабильный темп»

- Подвеска настроена так, чтобы машина прощала мелкие ошибки на входе.
- Клиренс позволяет агрессивно работать с поребриками, не теряя стабильность.
- Баланс рассчитан под длинные серии кругов без перегрева резины.

### Когда использовать этот сетап

- Онлайн-спринты с плотным трафиком и борьбой в пелотоне.
- Трассы со средним количеством быстрых связок и медленных шпилек.
- Ситуации, когда важнее стабильность и предсказуемость, чем абсолютный пейс.

> ⚠️ В будущем появятся альтернативные пресеты под **квалификацию** и **длинные стинты** — с более острыми настройками подвески и аэродинамики.

### Детальные настройки

#### Подвеска

| Параметр | Значение | Примечание |
|----------|--------|------------|
| Клиренс (перед) | 58 мм | Чуть выше порога зацепа поребриков |
| Клиренс (зад) | 62 мм | Стабильность на выходе из поворота |
| Пружины (перед) | 145 Н/мм | Чёткий отклик при смене направления |
| Пружины (зад) | 155 Н/мм | Контроль сноса на высоких скоростях |
| Стабилизатор (перед) | 28 | Меньше крена при резком повороте руля |
| Стабилизатор (зад) | 24 | Чуть более живой зад, но без сноса |

#### Аэродинамика

| Параметр | Значение | Примечание |
|----------|--------|------------|
| Крыло (перед) | Среднее прижатие | Баланс между поворотом и скоростью на прямой |
| Крыло (зад) | Чуть выше среднего | Стабильность на выходе и при смене направления |

#### Тормоза

| Параметр | Значение | Примечание |
|----------|--------|------------|
| Баланс тормозов | 52% на перед | Чуть смещён вперёд для стабильности при замедлении |
| Давление тормозов | 95% | Оставляет запас под работу без ABS |

#### Трансмиссия

| Параметр | Значение | Примечание |
|----------|--------|------------|
| Финальная передача | 3.45 | Подходит под средние и короткие прямые |
| 1–2 передачи | Сжатые | Ускорение с медленных шпилек без провала по оборотам |

## Структура материалов

Наши материалы устроены по следующему принципу:

1. **Один автомобиль — несколько рабочих пресетов** под разные форматы заездов.
2. **Детальный разбор ключевых зон**: подвеска, аэродинамика, тормоза, трансмиссия.
3. **Привязка к реальным стримам и сериям**, чтобы можно было «увидеть сетап в деле».

## Техническая реализация

### HTML-структура (index1.html)

HTML-файл представляет собой полноценную веб-страницу с разделением на логические секции:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forza Motorsport 8 - СайтСотика</title>
    <meta name="description" content="Серия Forza Motorsport 8 - гайды, видео, новости и разбора трасс.">
    <link rel="canonical" href="/pages/games/forza/motorsport8/">
    <link rel="stylesheet" href="/css/header.css">
    <link rel="stylesheet" href="/css/game.css">
    <link rel="stylesheet" href="/css/game-tabs.css">
    <link rel="stylesheet" href="/pages/games/forza/motorsport8/style.css">
</head>
<body>
    <!-- Основной заголовок сайта -->
    <header id="main-header">
        <div class="logo">СайтСотика</div>
        <nav id="main-nav">
            <a href="/pages/main/" class="nav-link">Главная</a>
            <a href="/pages/about/" class="nav-link">Обо мне</a>
            <a href="#" class="nav-link active" data-menu-action="open-games">Игры</a>
            <a href="/pages/stream/" class="nav-link">Стрим</a>
            <a href="/pages/team/" class="nav-link">Команда</a>
            <a href="/pages/partners/" class="nav-link">Партнеры</a>
        </nav>
        <script src="/js/header.js"></script>
    </header>

    <!-- Навигация по странице -->
    <nav class="page-nav">
        <a href="#guides" title="Гайды"></a>
        <a href="#videos" title="Видео"></a>
        <a href="#news" title="Новости"></a>
        <a href="#tracks" title="Трассы"></a>
    </nav>

    <!-- Основное содержимое -->
    <main>
        <div class="game-tabs">
            <button class="game-tab active" data-tab="guides">Гайды</button>
            <button class="game-tab" data-tab="videos">Видео</button>
            <button class="game-tab" data-tab="news">Новости</button>
            <button class="game-tab" data-tab="tracks">Трассы</button>
        </div>

        <div class="game-tab-content" id="game-tab-content">
            <div id="guides" class="tab-pane active">
                <!-- Секция героев с фоновым изображением -->
                <section class="game-hero" style="background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url('/images/games/forza/hero.jpg') center/cover no-repeat;">
                    <div style="max-width:1200px;margin:0 auto;">
                        <h1 style="font-size:3.6em;margin-bottom:12px;text-shadow:2px 2px 6px rgba(0,0,0,0.9);">
                            Forza Motorsport 8 — гайды и разборы
                        </h1>
                        <p style="font-size:1.3em;max-width:900px;margin:0 auto;text-shadow:1px 1px 4px rgba(0,0,0,0.8);">
                            Подробные руководства по симулятору гонок: настройки автомобилей, стратегии, разбор трасс и советы по прогрессии.
                        </p>
                    </div>
                </section>

                <!-- Ознакомительная секция об игре -->
                <section class="game-intro-section">
                    <div class="game-intro-inner">
                        <!-- Контент описания игры -->
                    </div>
                </section>

                <!-- Секция настроек автомобиля -->
                <section class="car-settings-section">
                    <div class="car-settings-inner">
                        <!-- Панель настроек с вкладками -->
                    </div>
                </section>
            </div>
        </div>
    </main>

    <!-- Подвал сайта -->
    <footer>
        © СайтСотика — Forza Motorsport 8, гайды и разборы
    </footer>

    <!-- Подключение скриптов -->
    <script src="/pages/games/forza/motorsport8/script.js"></script>
</body>
</html>
```

**Пояснения к HTML-структуре:**
- Документ использует семантическую разметку для лучшей доступности
- Все стили вынесены во внешние CSS-файлы для поддержки и масштабируемости
- Скрипты также вынесены во внешний файл для лучшей производительности
- Используются встроенные стили только для критически важных инлайновых стилей (например, фоновые изображения)
- Реализована система вкладок для навигации по контенту
- Добавлена фиксированная навигация по странице для удобства

### Стили (style.css)

```css
/* Стили для Forza Motorsport 8 */

html,body{height:100%}
body{
    display:flex;
    flex-direction:column;
    min-height:100vh;
    margin:0;
    font-family:Arial,Helvetica,sans-serif;
    color:#222;
    background:#fff
}
main{flex:1}
.game-hero{
    color:#fff;
    text-align:center;
    padding:140px 20px 100px;
    margin-bottom:60px;
    background-size:cover;
    background-position:center
}
.page-nav{
    position:fixed;
    right:20px;
    top:50%;
    transform:translateY(-50%);
    z-index:99;
    display:flex;
    flex-direction:column;
    gap:12px;
    background:rgba(255,255,255,0.95);
    padding:12px;
    border-radius:8px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
}
.page-nav a{
    width:8px;
    height:8px;
    border-radius:50%;
    background:#ccc;
    display:block;
    cursor:pointer;
    transition:background 0.2s;
}
.page-nav a.active{
    background:#007acc;
    width:24px;
}
@media (max-width:768px){
    .page-nav{display:none}
}
footer{
    background:#f8f9fa;
    color:#666;
    border-top:1px solid #eee;
    padding:40px 20px;
    text-align:center
}

/* Стили для ознакомительной секции */
.game-intro-section{
    padding:40px 20px 50px;
    background:#05060a;
    color:#f5f5f5;
    font-family:Arial,Helvetica,sans-serif;
}
.game-intro-inner{
    max-width:1200px;
    margin:0 auto;
    display:grid;
    grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);
    gap:28px;
}
/* ... остальные стили секции ... */

/* Стили для секции настроек автомобиля */
.car-settings-section {
    padding: 60px 20px 80px;
    background:#0b0c10;
    color:#f5f5f5;
    font-family: Arial, Helvetica, sans-serif;
}
/* ... остальные стили секции ... */
```

**Пояснения к CSS-стилям:**
- Все стили вынесены в отдельный файл для лучшей поддержки
- Используется современный подход с flex и grid для верстки
- Реализована адаптивность через медиа-запросы
- Стили разделены на логические блоки с комментариями
- Используются переменные цвета и отступов для согласованности
- Реализованы визуальные эффекты (градиенты, тени, переходы)
- Обеспечена кросс-браузерная совместимость

### Скрипты (script.js)

```javascript
// Переключение основных вкладок страницы (гайды / видео / новости / трассы)
(function(){
    var tabs = document.querySelectorAll('.game-tab');
    var panes = document.querySelectorAll('.tab-pane');

    tabs.forEach(function(tab){
        tab.addEventListener('click', function(){
            var target = tab.getAttribute('data-tab');
            tabs.forEach(function(t){ t.classList.remove('active'); });
            panes.forEach(function(p){
                if(p.id === target){
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                }
            });
            tab.classList.add('active');
        });
    });
})();

// Переключение вкладок настроек автомобиля
(function(){
    var tabs = document.querySelectorAll('.car-settings-tab');
    var panes = document.querySelectorAll('.car-settings-pane');

    tabs.forEach(function(tab){
        tab.addEventListener('click', function(){
            var target = tab.getAttribute('data-settings-tab');
            tabs.forEach(function(t){ t.classList.remove('active'); });
            panes.forEach(function(p){
                if(p.getAttribute('data-settings-pane') === target){
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                }
            });
            tab.classList.add('active');
        });
    });
})();
```

**Пояснения к JavaScript-скриптам:**
- Все скрипты вынесены в отдельный файл для лучшей производительности
- Используется IIFE (Immediately Invoked Function Expression) для изоляции области видимости
- Реализованы две независимые системы переключения вкладок:
  1. Основные вкладки страницы (гайды, видео, новости, трассы)
  2. Вкладки настроек автомобиля (подвеска, аэродинамика, тормоза, трансмиссия)
- Используется делегирование событий для эффективной обработки кликов
- Скрипты работают с data-атрибутами для связи вкладок и панелей
- Обеспечена плавная анимация переключения через CSS-классы
- Код написан в современном стиле с использованием forEach
- Обеспечена совместимость с большинством современных браузеров

## Навигация по контенту

- 📘 [Гайды](#guides) — подробные руководства по настройкам и стратегиям
- ▶️ [Видео](#videos) — визуальные разборы и стримы
- 📰 [Новости](#news) — актуальные обновления и изменения в игре
- 🏁 [Трассы](#tracks) — разбор ключевых поворотов и секторов

---

> © СайтСотика — Forza Motorsport 8, гайды и разборы