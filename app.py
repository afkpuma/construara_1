from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# Removido: from datetime import datetime (agora é importado em models.py)

app = Flask(__name__)

# --- Configuração do Banco de Dados SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construara_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Importa os Modelos do Banco de Dados ---
# É importante importar *todos* os modelos aqui para que o SQLAlchemy os reconheça
# quando for criar as tabelas com db.create_all()
# ... (código existente do app.py, incluindo imports e configuração do db) ...

# Importa os Modelos do Banco de Dados
from models import Cliente, Andaime, Locacao, LocacaoAndaime # Importa os modelos do seu novo arquivo
# ... (suas rotas existentes: '/', '/status', '/echo', '/user/<int:user_id>') ...

@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    """
    Rota para registrar uma nova venda/locação de andaimes no banco de dados.
    Recebe dados em formato JSON.
    """
    data = request.get_json() # Pega os dados JSON enviados na requisição

    # --- Validação básica de dados (melhorar futuramente!) ---
    # É uma boa prática validar *todos* os campos, mas para começar, validamos os essenciais.
    required_fields = ['nome_cliente', 'telefone_cliente', 'data_inicio_locacao', 
                       'dias_locacao', 'valor_total', 'status_pagamento', 'codigos_andaimes']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo '{field}' é obrigatório."}), 400

    try:
        # 1. Encontrar ou Criar Cliente
        # Busca por um cliente existente pelo nome e telefone (assumindo que seja uma combinação única o suficiente para fins de teste)
        cliente = Cliente.query.filter_by(
            nome=data['nome_cliente'], 
            telefone=data['telefone_cliente']
        ).first()

        if not cliente:
            # Se o cliente não existir, cria um novo
            cliente = Cliente(
                nome=data['nome_cliente'],
                endereco=data.get('endereco_cliente'), # .get() para campos opcionais
                telefone=data['telefone_cliente']
            )
            db.session.add(cliente)
            # db.session.commit() # Não commitamos ainda, tudo em uma transação no final

        # 2. Preparar Dados da Locação
        # Converte as datas de string para objetos date do Python
        # Espera formato 'YYYY-MM-DD'
        data_inicio = datetime.strptime(data['data_inicio_locacao'], '%Y-%m-%d').date()

        nova_locacao = Locacao(
            cliente=cliente, # Associa o objeto cliente
            data_registro=datetime.utcnow(), # Data e hora atual do registro
            data_inicio_locacao=data_inicio,
            dias_locacao=data['dias_locacao'],
            valor_total=data['valor_total'],
            status_pagamento=data['status_pagamento'],
            anotacoes=data.get('anotacoes', '') # Anotações são opcionais, valor padrão vazio
        )
        db.session.add(nova_locacao)
        # db.session.commit() # Não commitamos ainda

        # 3. Processar Andaimes Locados
        codigos_andaimes = data['codigos_andaimes'] # Deve ser uma lista de códigos de andaimes, ex: ["AND-001", "AND-003"]
        andaimes_para_locar = []
        
        if not codigos_andaimes:
            return jsonify({"error": "Nenhum código de andaime fornecido para locação."}), 400

        for codigo in codigos_andaimes:
            andaime = Andaime.query.filter_by(codigo=codigo).first()
            if not andaime:
                db.session.rollback() # Desfaz qualquer adição anterior
                return jsonify({"error": f"Andaime com código '{codigo}' não encontrado."}), 404
            
            if andaime.status != 'disponivel':
                db.session.rollback() # Desfaz qualquer adição anterior
                return jsonify({"error": f"Andaime com código '{codigo}' não está disponível (status: {andaime.status})."}), 409 # 409 Conflict

            # Se o andaime está disponível, adiciona à lista e muda o status
            andaimes_para_locar.append(andaime)
            andaime.status = 'alugado' # ATUALIZA O STATUS DO ANDAIME

        # 4. Criar Entradas na Tabela de Junção (LocacaoAndaime)
        for andaime in andaimes_para_locar:
            locacao_andaime_entry = LocacaoAndaime(locacao=nova_locacao, andaime=andaime)
            db.session.add(locacao_andaime_entry)

        # --- Salvar todas as mudanças no banco de dados (Transação) ---
        db.session.commit()

        return jsonify({
            "message": "Locação registrada com sucesso!",
            "locacao_id": nova_locacao.id,
            "cliente_id": cliente.id,
            "andaimes_locados_count": len(codigos_andaimes)
        }), 201 # 201 Created

    except Exception as e:
        db.session.rollback() # Em caso de erro, desfaz todas as operações no banco de dados
        print(f"Erro ao registrar venda: {e}") # Para depuração
        return jsonify({"error": "Ocorreu um erro ao registrar a venda.", "details": str(e)}), 500

# ... (restante do seu app.py, incluindo o bloco if __name__ == '__main__':) ...


if __name__ == '__main__':
    # --- Criação das Tabelas (APENAS PARA O PRIMEIRO SETUP OU RESET!) ---
    # Este bloco continua aqui. Ele precisa importar os modelos para que o db.create_all()
    # saiba quais tabelas criar. Por isso, a importação em cima é crucial.
    with app.app_context():
        db.create_all()
        print("Tabelas criadas no banco de dados 'construara_1.db'!")
    # --- Fim do bloco de criação de tabelas ---

    app.run(debug=True)