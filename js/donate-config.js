// Конфигурация donate.stream
const DonateConfig = {
    uid: 'c408e441e6d24d538c0c0650e629bb22',
    token: '3RDE38I0NrBVxSJAb1za0I1ygBvdFEKfLruQXom1nf',
    
    // Получение URL для виджета цели
    getGoalWidgetUrl: function() {
        return `https://donate.stream/widget-goal?uid=${this.uid}&token=${this.token}`;
    },
    
    // Получение URL для донат-формы
    getDonateFormUrl: function() {
        return `https://donate.stream/sotikdima`;
    },
    
    // Получение URL для API (если понадобится)
    getApiUrl: function() {
        return `https://api.donate.stream/v1/users/${this.uid}?token=${this.token}`;
    }
};