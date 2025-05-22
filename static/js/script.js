// construara_1/static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('locacaoForm');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        messageDiv.textContent = '';
        messageDiv.className = 'message';

        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            if (key === 'dias_locacao' || key === 'valor_total' || key === 'quantidade') {
                data[key] = parseFloat(value);
            } else {
                data[key] = value;
            }
        }

        try {
            // ALTERADO: URL da API para o Blueprint de locações
            const response = await fetch('/locacoes/', { // Adicionado '/' no final para rota raiz do Blueprint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                messageDiv.textContent = result.message || 'Locação registrada com sucesso!';
                messageDiv.classList.add('success');
                form.reset();
            } else {
                messageDiv.textContent = result.error || 'Erro ao registrar locação.';
                messageDiv.classList.add('error');
                console.error('Erro da API:', result.details || result.error);
            }
        } catch (error) {
            messageDiv.textContent = 'Erro de conexão com o servidor.';
            messageDiv.classList.add('error');
            console.error('Erro de rede ou fetch:', error);
        }
    });
});
