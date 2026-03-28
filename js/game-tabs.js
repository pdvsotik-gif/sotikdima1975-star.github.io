// Инициализация вкладок при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
  // Находим все кнопки вкладок и контейнеры содержимого
  const tabButtons = document.querySelectorAll('.game-tab');
  const tabPanes = document.querySelectorAll('.tab-pane');

  // Проверяем, что элементы существуют
  if (tabButtons.length === 0 || tabPanes.length === 0) {
    console.warn('Элементы вкладок не найдены на странице');
    return;
  }

  // Добавляем обработчики кликов для каждой кнопки вкладки
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Получаем ID целевой вкладки из атрибута data-tab
      const targetTab = this.getAttribute('data-tab');
      
      // Снимаем активный класс со всех кнопок
      tabButtons.forEach(btn => {
        btn.classList.remove('active');
      });
      
      // Добавляем активный класс к текущей кнопке
      this.classList.add('active');
      
      // Скрываем все панели содержимого
      tabPanes.forEach(pane => {
        pane.classList.remove('active');
      });
      
      // Показываем целевую панель содержимого
      const targetPane = document.getElementById(targetTab);
      if (targetPane) {
        targetPane.classList.add('active');
      }
      
      // Плавная прокрутка к началу секции вкладок
      document.querySelector('.game-tabs').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    });
  });

  // Активируем первую вкладку по умолчанию, если нет активной
  const activeTab = document.querySelector('.game-tab.active');
  if (!activeTab && tabButtons.length > 0) {
    tabButtons[0].click();
  }
});