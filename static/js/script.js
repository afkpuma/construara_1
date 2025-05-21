// construara_1/static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('locacaoForm');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário (que recarregaria a página)

        // Limpa mensagens anteriores
        messageDiv.textContent = '';
        messageDiv.className = 'message';

        // Coleta os dados do formulário
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            if (key === 'dias_locacao' || key === 'valor_total') {
                data[key] = parseFloat(value); // Converte para número
            } else if (key === 'codigos_andaimes') {
                data[key] = value.split(',').map(code => code.trim()).filter(code => code !== ''); // Divide por vírgula e limpa espaços
            } else {
                data[key] = value;
            }
        }

        try {
            // Envia os dados para a API usando fetch
            const response = await fetch('/registrar_venda', { // Caminho para a sua rota Flask
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' // Indica que estamos enviando JSON
                },
                body: JSON.stringify(data) // Converte o objeto JavaScript para uma string JSON
            });

            const result = await response.json(); // Pega a resposta JSON da API

            if (response.ok) { // Status 2xx (ex: 200, 201)
                messageDiv.textContent = result.message || 'Locação registrada com sucesso!';
                messageDiv.classList.add('success');
                form.reset(); // Limpa o formulário
            } else { // Status de erro (4xx, 5xx)
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