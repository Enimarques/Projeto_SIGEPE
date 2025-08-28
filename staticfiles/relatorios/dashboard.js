// dashboard.js - Dashboard dinâmico de relatórios

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard carregado, iniciando carregamento de dados...');
    
    // Atualiza cards
    fetch('/relatorios/api/cards/')
        .then(r => {
            console.log('Resposta da API cards:', r.status);
            return r.json();
        })
        .then(data => {
            console.log('Dados dos cards recebidos:', data);
            document.getElementById('card-acessos').textContent = data.acessos;
            document.getElementById('card-visitantes').textContent = data.visitantes;
            document.getElementById('card-alertas').textContent = data.alertas;
            document.getElementById('card-tempo').textContent = data.tempo_medio + 's';
        })
        .catch(error => {
            console.error('Erro ao carregar cards:', error);
        });

    // Atualiza gráficos
    fetch('/relatorios/api/graficos/')
        .then(r => {
            console.log('Resposta da API gráficos:', r.status);
            return r.json();
        })
        .then(data => {
            console.log('Dados dos gráficos recebidos:', data);
            
            // Verificar se Chart.js está carregado
            if (typeof Chart === 'undefined') {
                console.error('Chart.js não foi carregado!');
                return;
            }
            
            // Gráfico de Pizza
            var pizzaCanvas = document.getElementById('grafico-pizza');
            if (pizzaCanvas) {
                var ctxPizza = pizzaCanvas.getContext('2d');
                new Chart(ctxPizza, {
                    type: 'doughnut',
                    data: {
                        labels: data.pizza.labels,
                        datasets: [{
                            data: data.pizza.values,
                            backgroundColor: ['#43cea2', '#f7971e', '#ff9966'],
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
                console.log('Gráfico de pizza criado com sucesso');
            } else {
                console.error('Elemento grafico-pizza não encontrado!');
            }
            
            // Gráfico de Linha
            var linhaCanvas = document.getElementById('grafico-linha');
            if (linhaCanvas) {
                var ctxLinha = linhaCanvas.getContext('2d');
                new Chart(ctxLinha, {
                    type: 'line',
                    data: {
                        labels: data.linha.labels,
                        datasets: [
                            {
                                label: 'Acessos',
                                data: data.linha.acessos,
                                borderColor: '#43cea2',
                                fill: false
                            },
                            {
                                label: 'Alertas',
                                data: data.linha.alertas,
                                borderColor: '#f7971e',
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
                console.log('Gráfico de linha criado com sucesso');
            } else {
                console.error('Elemento grafico-linha não encontrado!');
            }
        })
        .catch(error => {
            console.error('Erro ao carregar gráficos:', error);
        });

    // Função para atualizar tabela (global)
    window.atualizarTabela = function() {
        const data = document.getElementById('filtro-data').value;
        const tipo = document.getElementById('filtro-tipo').value;
        const usuario = document.getElementById('filtro-usuario').value;
        const params = new URLSearchParams({ data, tipo, usuario });
        fetch('/relatorios/api/tabela/?' + params)
            .then(r => {
                console.log('Resposta da API tabela:', r.status);
                return r.json();
            })
            .then(data => {
                console.log('Dados da tabela recebidos:', data);
                var tabela = document.getElementById('tabela-relatorios');
                tabela.innerHTML = data.rows.map(r =>
                    `<tr><td>${r.data}</td><td>${r.tipo}</td><td>${r.usuario}</td><td>${r.descricao}</td></tr>`
                ).join('') || '<tr><td colspan="4" class="text-center">Nenhum registro encontrado</td></tr>';
            })
            .catch(error => {
                console.error('Erro ao carregar tabela:', error);
            });
    };
    // Atualiza tabela ao carregar
    window.atualizarTabela();
    // Atualiza tabela ao mudar filtros
    document.getElementById('filtro-data').addEventListener('change', window.atualizarTabela);
    document.getElementById('filtro-tipo').addEventListener('change', window.atualizarTabela);
    document.getElementById('filtro-usuario').addEventListener('input', window.atualizarTabela);
}); 