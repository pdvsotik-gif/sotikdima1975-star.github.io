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