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
                window.pizzaChart = new Chart(ctxPizza, {
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
                window.linhaChart = new Chart(ctxLinha, {
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
        const params = new URLSearchParams();
        
        const dataInicio = document.getElementById('filtro-data-inicio')?.value || '';
        const dataFim = document.getElementById('filtro-data-fim')?.value || '';
        const setor = document.getElementById('filtro-setor')?.value || '';
        const status = document.getElementById('filtro-status')?.value || '';
        const localizacao = document.getElementById('filtro-localizacao')?.value || '';
        const objetivo = document.getElementById('filtro-objetivo')?.value || '';
        const usuario = document.getElementById('filtro-usuario')?.value || '';
        
        if (dataInicio) params.append('data_inicio', dataInicio);
        if (dataFim) params.append('data_fim', dataFim);
        if (setor) params.append('setor', setor);
        if (status) params.append('status', status);
        if (localizacao) params.append('localizacao', localizacao);
        if (objetivo) params.append('objetivo', objetivo);
        if (usuario) params.append('usuario', usuario);
        
        fetch('/relatorios/api/tabela/?' + params)
            .then(r => {
                console.log('Resposta da API tabela:', r.status);
                return r.json();
            })
            .then(data => {
                console.log('Dados da tabela recebidos:', data);
                var tabela = document.getElementById('tabela-relatorios');
                tabela.innerHTML = data.rows.map(r =>
                    `<tr>
                        <td>${r.data}</td>
                        <td><span class="badge bg-${r.tipo === 'Em Andamento' ? 'primary' : r.tipo === 'Finalizada' ? 'success' : r.tipo === 'Cancelada' ? 'danger' : 'secondary'}">${r.tipo}</span></td>
                        <td>${r.usuario}</td>
                        <td>${r.setor || '-'}</td>
                        <td>${r.localizacao || '-'}</td>
                        <td>${r.objetivo || r.descricao || '-'}</td>
                    </tr>`
                ).join('') || '<tr><td colspan="6" class="text-center">Nenhum registro encontrado</td></tr>';
            })
            .catch(error => {
                console.error('Erro ao carregar tabela:', error);
            });
    };
    
    // Atualiza cards e gráficos com filtros
    function atualizarCardsEGraficos() {
        const params = new URLSearchParams();
        
        const dataInicio = document.getElementById('filtro-data-inicio')?.value || '';
        const dataFim = document.getElementById('filtro-data-fim')?.value || '';
        const setor = document.getElementById('filtro-setor')?.value || '';
        const status = document.getElementById('filtro-status')?.value || '';
        const localizacao = document.getElementById('filtro-localizacao')?.value || '';
        const objetivo = document.getElementById('filtro-objetivo')?.value || '';
        
        if (dataInicio) params.append('data_inicio', dataInicio);
        if (dataFim) params.append('data_fim', dataFim);
        if (setor) params.append('setor', setor);
        if (status) params.append('status', status);
        if (localizacao) params.append('localizacao', localizacao);
        if (objetivo) params.append('objetivo', objetivo);
        
        // Atualiza cards
        fetch('/relatorios/api/cards/?' + params)
            .then(r => r.json())
            .then(data => {
                document.getElementById('card-acessos').textContent = data.acessos;
                document.getElementById('card-visitantes').textContent = data.visitantes;
                document.getElementById('card-alertas').textContent = data.alertas;
                document.getElementById('card-tempo').textContent = data.tempo_medio + 's';
            })
            .catch(error => {
                console.error('Erro ao carregar cards:', error);
            });
        
        // Atualiza gráficos
        fetch('/relatorios/api/graficos/?' + params)
            .then(r => r.json())
            .then(data => {
                // Atualizar gráfico de pizza
                if (window.pizzaChart) {
                    window.pizzaChart.data.datasets[0].data = data.pizza.values;
                    window.pizzaChart.update();
                }
                // Atualizar gráfico de linha
                if (window.linhaChart) {
                    window.linhaChart.data.labels = data.linha.labels;
                    window.linhaChart.data.datasets[0].data = data.linha.acessos;
                    window.linhaChart.data.datasets[1].data = data.linha.alertas;
                    window.linhaChart.update();
                }
            })
            .catch(error => {
                console.error('Erro ao carregar gráficos:', error);
            });
    }
    
    // Atualiza tabela ao carregar
    window.atualizarTabela();
    
    // Atualiza tabela e cards/gráficos ao mudar filtros
    const filtros = ['filtro-data-inicio', 'filtro-data-fim', 'filtro-setor', 'filtro-status', 'filtro-localizacao', 'filtro-objetivo'];
    filtros.forEach(id => {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.addEventListener('change', function() {
                window.atualizarTabela();
                atualizarCardsEGraficos();
            });
        }
    });
    
    const filtroUsuario = document.getElementById('filtro-usuario');
    if (filtroUsuario) {
        let timeout;
        filtroUsuario.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                window.atualizarTabela();
            }, 500); // Aguarda 500ms após parar de digitar
        });
    }
}); 