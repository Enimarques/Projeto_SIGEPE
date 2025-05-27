// dashboard.js - Dashboard dinâmico de relatórios

document.addEventListener('DOMContentLoaded', function() {
    // Atualiza cards
    fetch('/relatorios/api/cards/')
        .then(r => r.json())
        .then(data => {
            document.getElementById('card-acessos').textContent = data.acessos;
            document.getElementById('card-visitantes').textContent = data.visitantes;
            document.getElementById('card-alertas').textContent = data.alertas;
            document.getElementById('card-tempo').textContent = data.tempo_medio + 's';
        });

    // Atualiza gráficos
    fetch('/relatorios/api/graficos/')
        .then(r => r.json())
        .then(data => {
            // Gráfico de Pizza
            var ctxPizza = document.getElementById('graficoPizza').getContext('2d');
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
            // Gráfico de Linha
            var ctxLinha = document.getElementById('graficoLinha').getContext('2d');
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
        });

    // Função para atualizar tabela
    function atualizarTabela() {
        const data = document.getElementById('filtro-data').value;
        const tipo = document.getElementById('filtro-tipo').value;
        const usuario = document.getElementById('filtro-usuario').value;
        const params = new URLSearchParams({ data, tipo, usuario });
        fetch('/relatorios/api/tabela/?' + params)
            .then(r => r.json())
            .then(data => {
                var tabela = document.getElementById('tabela-relatorios');
                tabela.innerHTML = data.rows.map(r =>
                    `<tr><td>${r.data}</td><td>${r.tipo}</td><td>${r.usuario}</td><td>${r.descricao}</td></tr>`
                ).join('') || '<tr><td colspan="4" class="text-center">Nenhum registro encontrado</td></tr>';
            });
    }
    // Atualiza tabela ao carregar
    atualizarTabela();
    // Atualiza tabela ao mudar filtros
    document.getElementById('filtro-data').addEventListener('change', atualizarTabela);
    document.getElementById('filtro-tipo').addEventListener('change', atualizarTabela);
    document.getElementById('filtro-usuario').addEventListener('input', atualizarTabela);
}); 