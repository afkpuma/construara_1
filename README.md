# Projeto locacao andaime

![GitHub last commit](https://img.shields.io/github/last-commit/afkpuma/construara_1?style=flat-square)
![GitHub top language](https://img.shields.io/github/languages/top/afkpuma/construara_1?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/afkpuma/construara_1?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## 📝 Descrição do Projeto

O **construara_1** é um sistema simplificado para gerenciar a locação e devolução de andaimes. Desenvolvido com Flask (Python) para o backend e uma interface web básica em HTML, CSS e JavaScript, este projeto visa oferecer uma solução prática para o controle de inventário de andaimes e registro de locações de clientes.

## ✨ Funcionalidades Atuais

* **Registro de Locação Simplificado:** Permite registrar novas locações de andaimes para clientes, agora especificando o **tipo e a quantidade** de andaimes desejados, em vez de códigos individuais. O sistema seleciona automaticamente os andaimes disponíveis.
* **Devolução de Andaimes:** Gerencia a devolução de andaimes, atualizando o status dos itens para 'disponível' novamente.
* **Visualização de Locações:** Exibe uma lista detalhada de todas as locações registradas, incluindo informações do cliente, datas, valores e os andaimes envolvidos.
* **Cadastro de Andaimes em Massa:** Permite adicionar **múltiplos novos andaimes** ao inventário do sistema de uma vez, especificando o tipo (ex: "Andaime Normal", "Andaime Menor") e a quantidade. Os códigos dos andaimes são gerados automaticamente.
* **Status de Andaimes:** Mantém o controle do status (`disponivel`, `alugado`, `manutencao`) de cada andaime.
* **Listagem de Andaimes Disponíveis:** Fornece uma rota para consultar andaimes com status 'disponível'.
* **Listagem de Clientes:** Rota para visualizar todos os clientes cadastrados.

## 🚀 Tecnologias Utilizadas

**Backend:**
* **Python:** Linguagem de programação principal.
* **Flask:** Micro-framework web para a API RESTful.
* **SQLAlchemy:** ORM (Object-Relational Mapper) para interagir com o banco de dados.
* **SQLite:** Banco de dados relacional leve (para desenvolvimento).

**Frontend:**
* **HTML5:** Estrutura das páginas web.
* **CSS3:** Estilização das páginas.
* **JavaScript:** Lógica de interação com o backend via Fetch API.

**Controle de Versão:**
* **Git:** Para controle de versão e colaboração.
* **GitHub:** Hospedagem do repositório de código.

## 📦 Estrutura do Projeto


construara_1/
├── app.py                  # Aplicação Flask principal, rotas e inicialização

├── extensions.py           # Inicializa o objeto SQLAlchemy (db)

├── models.py               # Definição dos modelos do banco de dados (Cliente, Andaime, Locacao, LocacaoAndaime)

├── templates/              # Contém os arquivos HTML (páginas web)

    │   ├── index.html          # Página principal: Formulário de registro de locação (agora por tipo/quantidade)
    │   ├── locacoes.html       # Página para visualizar todas as locações
    │   └── adicionar_andaime.html # NOVA PÁGINA: Formulário para adicionar andaimes em massa

├── static/                 # Contém arquivos estáticos (CSS, JavaScript)

    │   ├── css/
    │   │   └── style.css       # Estilos CSS globais para as páginas
    │   └── js/
    │       ├── script.js       # Lógica JavaScript para o formulário de registro de locação
    │       ├── locacoes.js     # Lógica JavaScript para a página de visualização de locações
    │       └── adicionar_andaime.js # NOVO JS: Lógica para o formulário de adição de andaimes

├── construara_1.db         # Banco de dados SQLite (gerado automaticamente)

├── .gitignore              # Ignora arquivos e pastas que não devem ser versionados (ex: .venv, .pyc, .db)

└── README.md               # Este arquivo de documentação


## 🛠️ Como Configurar e Rodar o Projeto Localmente

Siga os passos abaixo para configurar e rodar o projeto **construara_1** em sua máquina local.

### Pré-requisitos

* Python 3.8+
* Git

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/afkpuma/construara_1.git](https://github.com/afkpuma/construara_1.git)
    cd construara_1
    ```

2.  **Crie e ative um ambiente virtual:**
    É uma boa prática isolar as dependências do seu projeto.
    ```bash
    python -m venv .venv
    # No Windows:
    .venv\Scripts\activate
    # No macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```

4.  **Execute o aplicativo Flask:**
    Isso criará o banco de dados `construara_1.db` (se não existir) e iniciará o servidor de desenvolvimento.
    ```bash
    python app.py
    ```

5.  **Acesse o aplicativo:**
    Abra seu navegador e acesse:
    * **Página de Registro de Locações:** `http://127.0.0.1:5000/`
    * **Página de Visualização de Locações:** `http://127.0.0.1:5000/visualizar_locacoes`
    * **Página de Adição de Andaimes:** `http://127.0.0.1:5000/adicionar_andaimes`

## ⚙️ Endpoints da API

A API do **construara_1** expõe os seguintes endpoints principais:

### `GET /`
* **Descrição:** Serve a página HTML principal (`index.html`) para registro de locações.
* **Respostas:** Página HTML.

### `GET /visualizar_locacoes`
* **Descrição:** Serve a página HTML (`locacoes.html`) para visualização de todas as locações registradas.
* **Respostas:** Página HTML.

### `GET /adicionar_andaimes`
* **Descrição:** Serve a página HTML (`adicionar_andaime.html`) para adicionar novos andaimes ao inventário.
* **Respostas:** Página HTML.

### `GET /status`
* **Descrição:** Verifica o status da API.
* **Respostas:** `{"status": "ok", "message": "construara_1 API está online!"}` (HTTP 200)

### `GET /clientes`
* **Descrição:** Lista todos os clientes cadastrados no sistema.
* **Respostas:** Lista de objetos cliente (HTTP 200)
    ```json
    [
      {
        "id": 1,
        "nome": "Cliente Teste",
        "endereco": "Rua Exemplo, 123",
        "telefone": "34991234567"
      }
    ]
    ```

### `GET /andaimes_disponiveis`
* **Descrição:** Lista todos os andaimes que estão com o status 'disponivel'.
* **Respostas:** Lista de objetos andaime (HTTP 200)
    ```json
    [
      {
        "id": 1,
        "codigo": "AND-001",
        "descricao": "Andaime Básico 1.5x1.5",
        "status": "disponivel"
      }
    ]
    ```

### `POST /andaimes`
* **Descrição:** Adiciona **múltiplos novos andaimes** ao inventário com base no tipo e quantidade especificados. Códigos são gerados automaticamente (ex: NORMAL-0001, MENOR-0001).
* **Corpo da Requisição (JSON):**
    ```json
    {
      "tipo": "Andaime Normal",  // Ou "Andaime Menor"
      "quantidade": 5,
      "status": "disponivel"   // Opcional, padrão 'disponivel'
    }
    ```
* **Respostas:**
    * Sucesso (HTTP 201): `{"message": "5 Andaime Normal(s) adicionados com sucesso!", "andaimes": ["NORMAL-0001", "NORMAL-0002", ...]}`
    * Erro (HTTP 400): `{"error": "Campos 'tipo' e 'quantidade' são obrigatórios."}`
    * Conflito (HTTP 409): `{"error": "Erro de unicidade: Um código de andaime gerado já existe. Tente novamente."}`

### `POST /registrar_venda`
* **Descrição:** Registra uma nova locação de andaimes, selecionando andaimes disponíveis com base no `tipo` e `quantidade` solicitados.
* **Corpo da Requisição (JSON):**
    ```json
    {
      "nome_cliente": "Nome do Cliente",
      "telefone_cliente": "34999887766",
      "endereco_cliente": "Rua Nova, 456", // Opcional
      "data_inicio_locacao": "AAAA-MM-DD",
      "dias_locacao": 10,
      "valor_total": 500.00,
      "status_pagamento": "pago_a_vista", // ou "pendente", "parcial"
      "anotacoes": "Observações sobre a locação", // Opcional
      "tipo": "Andaime Normal",  // Ou "Andaime Menor"
      "quantidade": 2
    }
    ```
* **Respostas:**
    * Sucesso (HTTP 201): `{"message": "Locação registrada com sucesso!", "locacao_id": 1, "cliente_id": 1, "andaimes_locados": ["NORMAL-0001", "NORMAL-0002"]}`
    * Erro (HTTP 400): `{"error": "Todos os campos obrigatórios..."}`
    * Conflito (HTTP 409): `{"error": "Não há X andaime(s) do tipo 'Y' disponíveis para locação. Apenas Z disponíveis."}`

### `GET /locacoes`
* **Descrição:** Retorna uma lista de todas as locações registradas com detalhes do cliente e dos andaimes associados.
* **Respostas:** Lista de objetos locação (HTTP 200)
    ```json
    [
      {
        "id": 1,
        "cliente_id": 1,
        "data_registro": "AAAA-MM-DDTHH:MM:SS.mmmmmm",
        "data_inicio_locacao": "AAAA-MM-DD",
        "dias_locacao": 10,
        "valor_total": 500.0,
        "status_pagamento": "pago_a_vista",
        "anotacoes": "Observações",
        "cliente": {
          "id": 1,
          "nome": "Cliente Teste",
          "endereco": "Rua Exemplo, 123",
          "telefone": "34991234567"
        },
        "andaimes": [
          {
            "id": 1,
            "codigo": "NORMAL-0001",
            "descricao": "Andaime Normal",
            "status": "alugado"
          },
          {
            "id": 2,
            "codigo": "NORMAL-0002",
            "descricao": "Andaime Normal",
            "status": "alugado"
          }
        ]
      }
    ]
    ```

### `PUT /devolver_andaimes`
* **Descrição:** Atualiza o status de andaimes específicos para 'disponivel', registrando sua devolução.
* **Corpo da Requisição (JSON):**
    ```json
    {
      "codigos_andaimes": ["NORMAL-0001", "NORMAL-0002"]
    }
    ```
* **Respostas:**
    * Sucesso (HTTP 200): `{"message": "Devolução de andaime(s) registrada com sucesso!", "andaimes_devolvidos": ["NORMAL-0001", "NORMAL-0002"]}`
    * Sucesso com ressalvas (HTTP 200): `{"message": "Processamento de devolução concluído com algumas ressalvas.", "andaimes_devolvidos_com_sucesso": ["NORMAL-0001"], "erros": ["Andaime com código 'AND-999' não encontrado.", "Andaime com código 'NORMAL-0003' já está disponível."]}
    * Erro (HTTP 400, 500) com mensagem de erro.

## 🗄️ Modelos de Dados (Database Schema)

O banco de dados do **construara_1** é composto pelas seguintes tabelas:

* **`clientes`**: Informações sobre os clientes.
    * `id` (PK)
    * `nome`
    * `endereco`
    * `telefone`

* **`andaimes`**: Detalhes dos andaimes disponíveis.
    * `id` (PK)
    * `codigo` (Único)
    * `descricao` (agora representa o tipo, ex: "Andaime Normal")
    * `status` (e.g., 'disponivel', 'alugado', 'manutencao')

* **`locacoes`**: Registros das locações de andaimes.
    * `id` (PK)
    * `cliente_id` (FK para clientes)
    * `data_registro`
    * `data_inicio_locacao`
    * `dias_locacao`
    * `valor_total`
    * `status_pagamento` (e.g., 'pendente', 'pago_a_vista', 'parcial')
    * `anotacoes`

* **`locacao_andaimes`**: Tabela de junção (muitos-para-muitos) entre `locacoes` e `andaimes`, para registrar quais andaimes foram alugados em qual locação.
    * `id` (PK)
    * `locacao_id` (FK para locacoes)
    * `andaime_id` (FK para andaimes)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests.

## 📜 Licença

Este projeto está licenciado sob a Licença MIT.

---
