// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // Responsive behavior for mobile
    function checkWindowSize() {
        if (window.innerWidth < 768) {
            document.body.classList.add('sidebar-collapsed');
        }
    }

    // Initial check
    checkWindowSize();

    // Check on resize
    window.addEventListener('resize', checkWindowSize);
    
    // Inicializar os elementos do dashboard
    initDashboard();
    
    // Adicionar event listeners
    setupEventListeners();
    
    // Carregar dados iniciais
    loadSensorData();
    
    // Configurar atualização periódica
    setInterval(loadSensorData, 30000); // Atualiza a cada 30 segundos
});

function initDashboard() {
    console.log('Dashboard inicializado');
    // Inicializar gráficos vazios
    const chartElements = document.querySelectorAll('.sensor-chart');
    chartElements.forEach(element => {
        // Placeholder para inicialização de gráficos
        element.innerHTML = '<div class="chart-placeholder">Carregando gráfico...</div>';
    });
}

function setupEventListeners() {
    // Botão de atualização
    const refreshButton = document.querySelector('.btn-refresh');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            loadSensorData();
        });
    }
    
    // Botões de detalhes
    const detailButtons = document.querySelectorAll('.btn-details');
    detailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sensorId = this.getAttribute('data-sensor-id');
            showSensorDetails(sensorId);
        });
    });
    
    // Botão de adicionar sensor
    const addSensorButton = document.querySelector('.btn-add-sensor');
    if (addSensorButton) {
        addSensorButton.addEventListener('click', function() {
            showAddSensorForm();
        });
    }
}

function loadSensorData() {
    console.log('Carregando dados dos sensores...');
    
    // Simulação de carregamento de dados
    // Em produção, isso seria uma chamada AJAX para a API Django
    fetch('/api/sensors/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar dados dos sensores');
            }
            return response.json();
        })
        .then(data => {
            updateSensorCards(data);
        })
        .catch(error => {
            console.error('Erro:', error);
            // Mostrar mensagem de erro para o usuário
        });
}

function updateSensorCards(data) {
    // Esta função seria implementada para atualizar os cards com dados reais
    console.log('Atualizando cards com novos dados');
    
    // Simulação de atualização
    const cards = document.querySelectorAll('.sensor-card');
    if (cards.length === 0 && data.length > 0) {
        // Se não houver cards mas temos dados, recarregar a página
        window.location.reload();
        return;
    }
    
    // Atualizar timestamps para simular atualização
    const timestamps = document.querySelectorAll('.sensor-timestamp');
    const now = new Date();
    timestamps.forEach(timestamp => {
        timestamp.textContent = 'Última atualização: ' + now.toLocaleTimeString();
    });
}

function showSensorDetails(sensorId) {
    console.log('Mostrando detalhes do sensor ID:', sensorId);
    // Implementação para mostrar detalhes do sensor
    // Poderia abrir um modal ou redirecionar para uma página de detalhes
    window.location.href = '/sensors/details/' + sensorId + '/';
}

function showAddSensorForm() {
    console.log('Mostrando formulário para adicionar sensor');
    // Implementação para mostrar formulário de adição de sensor
    window.location.href = '/sensors/add/';
}