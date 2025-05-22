// construara_1/static/js/adicionar_andaime.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addAndaimeForm');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        messageDiv.textContent = '';
        messageDiv.className = 'message';

        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            if (key === 'quantidade') {
                data[key] = parseInt(value);
            } else {
                data[key] = value;
            }
        }

        try {
            // ALTERADO: URL da API para o Blueprint de andaimes
            const response = await fetch('/andaimes/', { // Adicionado '/' no final para rota raiz do Blueprint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                messageDiv.textContent = result.message || 'Andaimes adicionados com sucesso!';
                messageDiv.classList.add('success');
                form.reset();
            } else {
                messageDiv.textContent = result.error || 'Erro ao adicionar andaimes.';
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
