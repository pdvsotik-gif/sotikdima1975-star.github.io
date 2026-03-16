document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("main-header");
    const mainNav = document.getElementById("main-nav");
    const logo = header.querySelector(".logo");
    const links = header.querySelectorAll(".nav-link");

    // === Подсветка активной страницы ===
    const path = window.location.pathname;
    const currentPage = path.split("/").pop() || "index.html";

    links.forEach(link => {
        if (link.getAttribute("href") === currentPage) {
            link.style.background = "#6a11cb";
            link.style.color = "white";
            link.style.fontWeight = "600";
        }
    });

    // === Удалить все дополнительные nav, кроме main-nav ===
    function cleanup() {
        header.querySelectorAll("nav[id]:not(#main-nav)").forEach(nav => nav.remove());
    }

    // === Применить стили к любому nav ===
    function styleNav(nav) {
        nav.style.cssText = `
            display: flex;
            gap: 4px;
            height: 100%;
            align-items: center;
            margin-right: 12px;
        `;
    }

    // === Создать меню выбора серии ===
    function createGamesNav() {
        cleanup();
        const gamesNav = document.createElement("nav");
        gamesNav.id = "games-nav";
        gamesNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад</a>
            <a href="#" class="nav-link game-series" data-series="forza">Forza Motorsport</a>
            <a href="#" class="nav-link game-series" data-series="ac">Assetto Corsa</a>
            <a href="#" class="nav-link game-series" data-series="pc">Project Cars</a>
        `;
        styleNav(gamesNav);
        header.appendChild(gamesNav);
        logo.textContent = "Игры • СайтСотика";
    }

    // === Создать подменю Forza ===
    function createForzaNav() {
        cleanup();
        const forzaNav = document.createElement("nav");
        forzaNav.id = "forza-nav";
        forzaNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="games/forza/motorsport7.html" class="nav-link">Forza Motorsport 7</a>
            <a href="games/forza/motorsport8.html" class="nav-link">Forza Motorsport 8</a>
        `;
        styleNav(forzaNav);
        header.appendChild(forzaNav);
        logo.textContent = "Forza Motorsport • СайтСотика";
    }

    // === Создать подменю Assetto Corsa ===
    function createAcNav() {
        cleanup();
        const acNav = document.createElement("nav");
        acNav.id = "ac-nav";
        acNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="games/ac/carrera.html" class="nav-link">Assetto Corsa</a>
            <a href="games/ac/competizione.html" class="nav-link">Assetto Corsa Competizione</a>
        `;
        styleNav(acNav);
        header.appendChild(acNav);
        logo.textContent = "Assetto Corsa • СайтСотика";
    }

    // === Создать подменю Project Cars ===
    function createPcNav() {
        cleanup();
        const pcNav = document.createElement("nav");
        pcNav.id = "pc-nav";
        pcNav.innerHTML = `
            <a href="#" class="nav-link back-link" data-back>← Назад к сериям</a>
            <a href="games/pc/1.html" class="nav-link">Project Cars 1</a>
            <a href="games/pc/2.html" class="nav-link">Project Cars 2</a>
            <a href="games/pc/3.html" class="nav-link">Project Cars 3</a>
        `;
        styleNav(pcNav);
        header.appendChild(pcNav);
        logo.textContent = "Project Cars • СайтСотика";
    }

    // === Клик по "Игры" ===
    header.querySelector("[data-page='games']").addEventListener("click", function (e) {
        e.preventDefault();
        mainNav.style.display = "none";
        createGamesNav();
        attachEventListeners();
    });

    // === Общая функция для привязки событий ===
    function attachEventListeners() {
        // Кнопка "Назад"
        header.querySelectorAll("[data-back]").forEach(button => {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                const parentId = this.closest("nav").id;

                cleanup();

                if (["forza-nav", "ac-nav", "pc-nav"].includes(parentId)) {
                    createGamesNav();
                } else if (parentId === "games-nav") {
                    mainNav.style.display = "flex";
                    logo.textContent = "СайтСотика";
                }
                attachEventListeners();
            });
        });

        // Выбор серии
        header.querySelectorAll("[data-series]").forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault();
                const series = this.getAttribute("data-series");
                if (series === "forza") createForzaNav();
                if (series === "ac") createAcNav();
                if (series === "pc") createPcNav();
                attachEventListeners();
            });
        });
    }

    // === Применение стилей к хэдеру и основному меню ===
    header.style.cssText = `
        width: 100%;
        height: 60px;
        background: #f8f9fa;
        border-bottom: 1px solid #dee2e6;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        font-family: 'Segoe UI', sans-serif;
        overflow: hidden;
        padding: 0;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;

    logo.style.cssText = `
        color: #6a11cb;
        font-size: 1.1em;
        font-weight: 700;
        margin-left: 16px;
        letter-spacing: 0.5px;
        white-space: nowrap;
        transition: all 0.3s ease;
    `;

    styleNav(mainNav);

    // === Анимация фона при движении мыши ===
    header.addEventListener("mousemove", (e) => {
        const x = e.clientX;
        const max = window.innerWidth;
        const hue = Math.floor((x / max) * 360);
        header.style.background = `linear-gradient(to right, #f8f9fa, hsl(${hue}, 40%, 90%), #f8f9fa)`;
    });

    header.addEventListener("mouseleave", () => {
        header.style.background = "#f8f9fa";
    });

    // === Инициализация ===
    attachEventListeners();
});