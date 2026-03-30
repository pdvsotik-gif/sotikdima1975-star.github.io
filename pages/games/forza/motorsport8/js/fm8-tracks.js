/* Forza Motorsport 8 - Tracks Slider Module */

/**
 * Основной объект с данными о трассах
 * @type {Object}
 */
const trackData = {
    spa: {
        name: "Circuit de Spa-Francorchamps",
        location: "Бельгия",
        length: "7.004 км",
        features: "Классическая трасса с Eau Rouge, Raidillon и переменной погодой",
        configs: null
    },
    silverstone: {
        name: "Silverstone Circuit",
        location: "Великобритания",
        length: "5.891 км",
        features: "Быстрая трасса с Maggotts-Becketts-Chapel",
        configs: null
    },
    suzuka: {
        name: "Suzuka Circuit",
        location: "Япония",
        length: "5.807 км",
        features: "Уникальная \"восьмёрка\", 130R, техничный серпантин",
        configs: null
    },
    laguna: {
        name: "Laguna Seca",
        location: "США",
        length: "3.607 км",
        features: "Знаменитый \"штопор\" (Corkscrew), подъём и перепад высот",
        configs: null
    },
    daytona: {
        name: "Daytona International Speedway",
        location: "США",
        length: "5.729 км (Oval)",
        features: "Легендарная овальная трасса с высокими поворотами",
        configs: [
            { id: "oval", name: "Oval", desc: "<strong>Oval</strong>: Основная конфигурация. Длина: 5.729 км." },
            { id: "roval", name: "ROVAL", desc: "<strong>ROVAL</strong>: Комбинированная. Длина: 5.730 км." },
            { id: "motorsports", name: "MotorSports", desc: "<strong>MotorSports Blvd</strong>: Внутренний контур. Длина: 4.28 км." }
        ]
    },
    hakone: {
        name: "Hakone Highland Raceway",
        location: "Вымышленная трасса (в стиле Японии)",
        length: "—",
        features: "Современный гоночный автодром в японском стиле, созданный специально для игры.",
        configs: [
            { id: "hakone-full", name: "Полная", desc: "<strong>Полная конфигурация</strong>: Основная версия трассы с полным набором поворотов." },
            { id: "hakone-short", name: "Короткая", desc: "<strong>Короткая конфигурация</strong>: Упрощённая и более динамичная версия трассы." }
        ]
    },
    barcelona: {
        name: "Circuit de Barcelona-Catalunya",
        location: "Испания",
        length: "4.655 км",
        features: "Техничная трасса, используется для тестов F1",
        configs: null
    },
    nurburgring: {
        name: "Nürburgring",
        location: "Германия",
        length: "20.832 км (Nordschleife)",
        features: "Легендарная трасса длиной более 20 км, известная как 'Зелёный ад'",
        configs: null
    },
    indy: {
        name: "Indianapolis Motor Speedway",
        location: "США",
        length: "4.192 км (RC)",
        features: "Комбинированная трасса, используемая в гонках IMSA и IndyCar",
        configs: null
    },
    brands_hatch: {
        name: "Brands Hatch",
        location: "Великобритания",
        length: "4.207 км (Grand Prix)",
        features: "Классическая британская трасса с быстрыми поворотами и перепадами высот",
        configs: null
    },
    hockenheim: {
        name: "Hockenheimring",
        location: "Германия",
        length: "4.574 км",
        features: "Современная трасса с длинными прямыми и скоростными поворотами",
        configs: null
    },
    kyalami: {
        name: "Kyalami Grand Prix Circuit",
        location: "ЮАР",
        length: "4.525 км",
        features: "Техничная трасса с быстрыми поворотами и перепадами высот",
        configs: null
    },
    panorama: {
        name: "Mount Panorama",
        location: "Австралия",
        length: "6.213 км",
        features: "Известная трасса с гонками Bathurst 1000, сложный рельеф и перепад высот",
        configs: null
    },
    yas_marina: {
        name: "Yas Marina Circuit",
        location: "ОАЭ",
        length: "5.554 км",
        features: "Трасса с ночными гонками Формулы 1, современная инфраструктура и температура до 50°C",
        configs: null
    },
    fujimi_kaido: {
        name: "Fujimi Kaidō",
        location: "Япония",
        length: "3.820 км",
        features: "Горная трасса с множеством поворотов, популярная у дрифтеров и любителей тюнинга",
        configs: null
    },
    sunset_peninsula: {
        name: "Sunset Peninsula",
        location: "Вымышленная трасса",
        length: "5.120 км",
        features: "Комбинированная трасса с городскими улицами и прибрежными участками",
        configs: null
    },
    eaglerock: {
        name: "Eaglerock Speedway",
        location: "США",
        length: "1.522 км (Oval)",
        features: "Короткая овальная трасса, идеальная для коротких гонок и дрэг-стартов",
        configs: null
    },
    grand_oak: {
        name: "Grand Oak Raceway",
        location: "США",
        length: "3.450 км",
        features: "Современный автодром с разнообразными поворотами и прямой для разгона",
        configs: null
    },
    homestead: {
        name: "Homestead-Miami Speedway",
        location: "США",
        length: "2.414 км (Oval)",
        features: "Овальная трасса, используемая для финальных гонок NASCAR",
        configs: null
    },
    le_mans: {
        name: "Circuit de la Sarthe (Le Mans)",
        location: "Франция",
        length: "13.629 км",
        features: "Легендарная трасса 24 часов Ле-Мана, сочетающая автодром и общественные дороги",
        configs: null
    },
    lime_rock: {
        name: "Lime Rock Park",
        location: "США",
        length: "1.478 км",
        features: "Короткая, но техничная трасса в живописной горной местности",
        configs: null
    },
    road_atlanta: {
        name: "Road Atlanta",
        location: "США",
        length: "4.088 км",
        features: "Техничная трасса с резкими подъёмами и спусками, известна поворотом \"Эль Торо\"",
        configs: null
    },
    mid_ohio: {
        name: "Mid-Ohio Sports Car Course",
        location: "США",
        length: "3.631 км",
        features: "Техничный автодром в живописной местности, популярен среди гонщиков IndyCar",
        configs: null
    },
    maple_valley: {
        name: "Maple Valley Raceway",
        location: "США",
        length: "3.219 км",
        features: "Техничная трасса с множеством поворотов и изменением высоты",
        configs: null
    },
    mugello: {
        name: "Mugello Circuit",
        location: "Италия",
        length: "5.245 км",
        features: "Быстрая и техничная трасса в живописной местности, используется в MotoGP",
        configs: null
    },
    road_america: {
        name: "Road America",
        location: "США",
        length: "6.437 км",
        features: "Одна из самых длинных и сложных трасс в США, с 14 поворотами",
        configs: null
    },
    sebring: {
        name: "Sebring International Raceway",
        location: "США",
        length: "6.019 км",
        features: "Легендарная трасса 12 часов Себринга, известна неровным покрытием и бетонными участками",
        configs: null
    },
    vir: {
        name: "Virginia International Raceway",
        location: "США",
        length: "5.472 км (Grand)",
        features: "Техничная трасса с резкими подъёмами и спусками, популярна среди любителей и профессионалов",
        configs: null
    },
    watkins_glen: {
        name: "Watkins Glen International",
        location: "США",
        length: "5.430 км",
        features: "Легендарная трасса, ранее принимавшая Гран-при США, известна быстрыми поворотами и прямой",
        configs: null
    },
    fuji: {
        name: "Fuji International Speedway",
        location: "Япония",
        length: "4.563 км",
        features: "Современный автодром с длинной прямой и поворотом Dunlop Curve",
        configs: null
    },
    osterreichring: {
        name: "Österreichring",
        location: "Австрия",
        length: "5.911 км",
        features: "Быстрая и техничная трасса в живописной горной местности",
        configs: null
    },
    mount_panorama_night: {
        name: "Mount Panorama (Night)",
        location: "Австралия",
        length: "6.213 км",
        features: "Ночная версия знаменитой трассы Mount Panorama",
        configs: null
    },
    daytona_road_course: {
        name: "Daytona Road Course",
        location: "США",
        length: "5.730 км",
        features: "Комбинированная версия трассы Daytona",
        configs: null
    },
    sebring_modified: {
        name: "Sebring Modified",
        location: "США",
        length: "6.019 км",
        features: "Модифицированная версия трассы Sebring",
        configs: null
    },
    nurburgring_24h: {
        name: "Nürburgring 24h",
        location: "Германия",
        length: "25.378 км",
        features: "Полная конфигурация Nürburgring для 24-часовой гонки",
        configs: null
    }
};

/**
 * Массив ID трасс для навигации
 * @type {string[]}
 */
const trackIds = Object.keys(trackData);

/**
 * Текущий индекс активной трассы
 * @type {number}
 */
let currentIndex = 0;

/**
 * Инициализация переключения основных вкладок
 */
function initMainTabs() {
    document.querySelectorAll('.fm8-main-tab').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.mainTab;
            document.querySelectorAll('.fm8-main-tab').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.fm8-main-pane').forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(tabId)?.classList.add('active');
        });
    });
}

/**
 * Инициализация переключения подвкладок (например, в разделе "Физика")
 */
function initPhysicsSubtabs() {
    document.querySelectorAll('.fm8-subtab').forEach(btn => {
        btn.addEventListener('click', () => {
            const group = btn.dataset.subtabGroup;
            const tabId = btn.dataset.subtab;

            document.querySelectorAll(`.fm8-subtab[data-subtab-group="${group}"]`)
                .forEach(b => b.classList.remove('active'));
            document.querySelectorAll(`#${group} .fm8-subpane`)
                .forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`${group}-${tabId}`)?.classList.add('active');
        });
    });
}

/**
 * Создание кнопок трасс в слайдере
 * @returns {NodeList|Array} Список созданных кнопок
 */
function createTrackButtons() {
    const container = document.querySelector('.fm8-tracks-list');
    if (!container) return [];

    // Очищаем контейнер перед созданием
    container.innerHTML = '';

    trackIds.forEach((id, index) => {
        const btn = document.createElement('button');
        btn.className = 'fm8-tracks-item';
        btn.textContent = trackData[id].name;
        btn.dataset.trackId = id;
        if (index === 0) btn.classList.add('active');
        btn.onclick = () => switchTrack(index);
        container.appendChild(btn);
    });

    return Array.from(container.children);
}

/**
 * Ожидание готовности макета перед выполнением операций
 * @param {Function} callback - Функция, которая будет вызвана, когда макет будет готов
 */
function waitForLayout(callback) {
    const checkLayout = () => {
        const item = document.querySelector('.fm8-tracks-item');
        if (item && item.offsetWidth > 0) {
            callback();
        } else {
            requestAnimationFrame(checkLayout);
        }
    };
    checkLayout();
}

/**
 * Переключение на указанную трассу с центрированием и отображением деталей
 * @param {number} index - Индекс трассы
 */
function switchTrack(index) {
    if (index < 0 || index >= trackIds.length) return;

    // Обновляем индекс и сохраняем в localStorage
    currentIndex = index;
    localStorage.setItem('fm8-last-track', trackIds[index]);

    // Обновляем кнопки
    document.querySelectorAll('.fm8-tracks-item').forEach((btn, i) => {
        btn.classList.toggle('active', i === index);
    });

    // Центрируем активную кнопку
    const container = document.querySelector('.fm8-tracks-list-wrapper');
    const item = document.querySelector(`.fm8-tracks-item:nth-child(${index + 1})`);
    if (!container || !item) return;

    const containerWidth = container.offsetWidth;
    const itemWidth = item.offsetWidth;
    const scrollLeft = item.offsetLeft - (containerWidth - itemWidth) / 2;

    container.scrollTo({
        left: scrollLeft,
        behavior: 'smooth'
    });

    // Отображаем детали трассы
    renderTrackDetails(trackIds[index]);
}

/**
 * Рендер информации о выбранной трассе
 * @param {string} trackId - ID трассы
 */
function renderTrackDetails(trackId) {
    const data = trackData[trackId];
    const contentDiv = document.getElementById('track-detail-content');
    if (!contentDiv || !data) return;

    let html = `
        <table class="fm8-table">
            <tr><th>Трасса</th><td>${data.name}</td></tr>
            <tr><th>Расположение</th><td>${data.location}</td></tr>
            <tr><th>Длина</th><td>${data.length}</td></tr>
            <tr><th>Особенности</th><td>${data.features}</td></tr>
        </table>
    `;

    // Если есть конфигурации трассы, добавляем слайдер конфигураций
    if (data.configs?.length) {
        const firstConfig = data.configs[0];
        html += `
            <div class="fm8-track-config-slider" style="margin-top:12px;">
                <div class="fm8-track-config-container">
        `;
        data.configs.forEach(cfg => {
            const active = cfg.id === firstConfig.id ? 'active' : '';
            html += `<button class="fm8-track-config-item ${active}" data-config="${cfg.id}">${cfg.name}</button>`;
        });
        html += `
                </div>
            </div>
            <div class="fm8-track-config-content" style="margin-top:8px;">
                <div class="fm8-config-pane active">${firstConfig.desc}</div>
            </div>
        `;
    }

    contentDiv.innerHTML = html;

    // Назначаем обработчики конфигураций
    if (data.configs?.length) {
        contentDiv.querySelectorAll('.fm8-track-config-item').forEach(btn => {
            btn.onclick = () => {
                const configId = btn.dataset.config;
                const config = data.configs.find(c => c.id === configId);
                if (config) {
                    btn.parentElement.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
                    btn.classList.add('active');
                    document.querySelector('.fm8-config-pane').innerHTML = config.desc;
                }
            };
        });
    }
}

/**
 * Инициализация слайдера трасс
 */
function initTracksSlider() {
    // Создаём кнопки трасс
    const trackItems = createTrackButtons();
    
    // Получаем элементы управления
    const prevBtn = document.querySelector('.fm8-tracks-arrow.left');
    const nextBtn = document.querySelector('.fm8-tracks-arrow.right');
    const container = document.querySelector('.fm8-tracks-list-wrapper');

    // Получаем последнюю выбранную трассу из localStorage
    const savedTrackId = localStorage.getItem('fm8-last-track');
    const startIndex = savedTrackId && trackIds.includes(savedTrackId)
        ? trackIds.indexOf(savedTrackId)
        : 0;

    // Ждём готовности макета перед инициализацией
    waitForLayout(() => {
        switchTrack(startIndex);
    });

    // Обработчики кнопок переключения
    prevBtn?.addEventListener('click', () => {
        switchTrack((currentIndex - 1 + trackIds.length) % trackIds.length);
    });

    nextBtn?.addEventListener('click', () => {
        switchTrack((currentIndex + 1) % trackIds.length);
    });

    // Обработка свайпов на мобильных устройствах
    let startX = 0;
    container.addEventListener('touchstart', e => {
        startX = e.touches[0].clientX;
    }, { passive: true });

    container.addEventListener('touchend', e => {
        const dist = startX - e.changedTouches[0].clientX;
        if (Math.abs(dist) > 30) {
            switchTrack(dist > 0 ? currentIndex + 1 : currentIndex - 1);
        }
    }, { passive: true });

    // Поддержка клавиш ← →
    container.setAttribute('tabindex', '0');
    container.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            switchTrack((currentIndex - 1 + trackIds.length) % trackIds.length);
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            switchTrack((currentIndex + 1) % trackIds.length);
        }
    });
}

// Инициализация всех компонентов после загрузки DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initMainTabs();
        initPhysicsSubtabs();
        initTracksSlider();
    });
} else {
    initMainTabs();
    initPhysicsSubtabs();
    initTracksSlider();
}