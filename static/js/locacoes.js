// construara_1/static/js/locacoes.js

document.addEventListener('DOMContentLoaded', async () => {
    const locacoesTableBody = document.querySelector('#locacoesTable tbody');
    const loadingMessage = document.getElementById('loadingMessage');
    const errorMessage = document.getElementById('errorMessage');
    const locacoesTable = document.getElementById('locacoesTable');

    try {
        const response = await fetch('/locacoes');
        const locacoes = await response.json();

        loadingMessage.style.display = 'none';

        if (response.ok) {
            if (locacoes.length === 0) {
                errorMessage.textContent = 'Nenhuma locação encontrada.';
                errorMessage.style.display = 'block';
            } else {
                locacoesTable.style.display = 'table';
                locacoes.forEach(locacao => {
                    const row = locacoesTableBody.insertRow();

                    row.insertCell().textContent = locacao.id;
                    row.insertCell().textContent = locacao.cliente ? locacao.cliente.nome : 'N/A';
                    row.insertCell().textContent = locacao.cliente ? locacao.cliente.telefone : 'N/A';
                    
                    const dataRegistro = new Date(locacao.data_registro).toLocaleDateString('pt-BR');
                    const dataInicio = new Date(locacao.data_inicio_locacao + 'T00:00:00').toLocaleDateString('pt-BR');
                    row.insertCell().textContent = dataRegistro;
                    row.insertCell().textContent = dataInicio;
                    
                    row.insertCell().textContent = locacao.dias_locacao;
                    row.insertCell().textContent = `R$ ${locacao.valor_total.toFixed(2).replace('.', ',')}`;
                    row.insertCell().textContent = locacao.status_pagamento;
                    
                    const andaimesCell = row.insertCell();
                    if (locacao.andaimes && locacao.andaimes.length > 0) {
                        const andaimesList = locacao.andaimes.map(a => `${a.codigo} (${a.status})`).join(', ');
                        andaimesCell.textContent = andaimesList;
                    } else {
                        andaimesCell.textContent = 'Nenhum andaime';
                    }
                    
                    row.insertCell().textContent = locacao.anotacoes || 'N/A';
                });
            }
        } else {
            errorMessage.textContent = `Erro ao carregar locações: ${locacoes.error || 'Erro desconhecido'}`;
            errorMessage.style.display = 'block';
            console.error('Erro da API:', locacoes.details || locacoes.error);
        }
    } catch (error) {
        loadingMessage.style.display = 'none';
        errorMessage.textContent = 'Erro de conexão com o servidor.';
        errorMessage.style.display = 'block';
        console.error('Erro de rede ou fetch:', error);
    }
});
