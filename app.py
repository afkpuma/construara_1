# construara_1/app.py
from flask import Flask, jsonify, request, render_template
from datetime import datetime

# Importa 'db' do nosso arquivo extensions.py
from extensions import db

app = Flask(__name__)

# --- Configuração do Banco de Dados SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construara_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Associa o objeto 'app' com 'db'
db.init_app(app)

# --- Importa os Modelos do Banco de Dados ---
from models import Cliente, Andaime, Locacao, LocacaoAndaime

# --- Rotas ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "ok", "message": "construara_1 API está online!"}), 200

@app.route('/echo', methods=['POST'])
def echo_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({"received_data": data, "message": "Dados POST recebidos com sucesso!"}), 200
    else:
        return jsonify({"error": "Content-Type deve ser application/json"}), 400

@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    clientes_data = []
    for cliente in clientes:
        clientes_data.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "endereco": cliente.endereco,
            "telefone": cliente.telefone
        })
    return jsonify(clientes_data), 200

@app.route('/andaimes_disponiveis', methods=['GET'])
def get_andaimes_disponiveis():
    andaimes = Andaime.query.filter_by(status='disponivel').all()
    andaimes_data = []
    for andaime in andaimes:
        andaimes_data.append({
            "id": andaime.id,
            "codigo": andaime.codigo,
            "descricao": andaime.descricao,
            "status": andaime.status
        })
    return jsonify(andaimes_data), 200

# --- NOVA ROTA: Adicionar Andaime ---
@app.route('/andaimes', methods=['POST'])
def add_andaime():
    """
    Adiciona um novo andaime ao banco de dados.
    Esperar JSON com 'codigo', 'descricao' (opcional), 'status' (opcional, padrão 'disponivel').
    """
    data = request.get_json()

    if 'codigo' not in data:
        return jsonify({"error": "O campo 'codigo' é obrigatório para adicionar um andaime."}), 400

    codigo = data['codigo']
    descricao = data.get('descricao', '') # Descrição é opcional
    status = data.get('status', 'disponivel') # Status padrão é 'disponivel'

    # Verifica se o código do andaime já existe
    if Andaime.query.filter_by(codigo=codigo).first():
        return jsonify({"error": f"Andaime com código '{codigo}' já existe."}), 409 # 409 Conflict

    try:
        novo_andaime = Andaime(codigo=codigo, descricao=descricao, status=status)
        db.session.add(novo_andaime)
        db.session.commit()
        return jsonify({
            "message": "Andaime adicionado com sucesso!",
            "id": novo_andaime.id,
            "codigo": novo_andaime.codigo,
            "status": novo_andaime.status
        }), 201 # 201 Created
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao adicionar andaime.", "details": str(e)}), 500


@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    """
    Rota para registrar uma nova venda/locação de andaimes no banco de dados.
    Recebe dados em formato JSON.
    """
    data = request.get_json()

    required_fields = ['nome_cliente', 'telefone_cliente', 'data_inicio_locacao',
                       'dias_locacao', 'valor_total', 'status_pagamento', 'codigos_andaimes']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo '{field}' é obrigatório."}), 400

    try:
        cliente = Cliente.query.filter_by(
            nome=data['nome_cliente'],
            telefone=data['telefone_cliente']
        ).first()

        if not cliente:
            cliente = Cliente(
                nome=data['nome_cliente'],
                endereco=data.get('endereco_cliente'),
                telefone=data['telefone_cliente']
            )
            db.session.add(cliente)

        data_inicio = datetime.strptime(data['data_inicio_locacao'], '%Y-%m-%d').date()

        nova_locacao = Locacao(
            cliente=cliente,
            data_registro=datetime.utcnow(),
            data_inicio_locacao=data_inicio,
            dias_locacao=data['dias_locacao'],
            valor_total=data['valor_total'],
            status_pagamento=data['status_pagamento'],
            anotacoes=data.get('anotacoes', '')
        )
        db.session.add(nova_locacao)

        codigos_andaimes = data['codigos_andaimes']
        andaimes_para_locar = []

        if not codigos_andaimes:
            return jsonify({"error": "Nenhum código de andaime fornecido para locação."}), 400

        for codigo in codigos_andaimes:
            andaime = Andaime.query.filter_by(codigo=codigo).first()
            if not andaime:
                db.session.rollback()
                return jsonify({"error": f"Andaime com código '{codigo}' não encontrado."}), 404

            if andaime.status != 'disponivel':
                db.session.rollback()
                return jsonify({"error": f"Andaime com código '{codigo}' não está disponível (status: {andaime.status})."}), 409

            andaimes_para_locar.append(andaime)
            andaime.status = 'alugado'

        for andaime in andaimes_para_locar:
            locacao_andaime_entry = LocacaoAndaime(locacao=nova_locacao, andaime=andaime)
            db.session.add(locacao_andaime_entry)

        db.session.commit()

        return jsonify({
            "message": "Locação registrada com sucesso!",
            "locacao_id": nova_locacao.id,
            "cliente_id": cliente.id,
            "andaimes_locados_count": len(codigos_andaimes)
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao registrar venda: {e}")
        return jsonify({"error": "Ocorreu um erro ao registrar a venda.", "details": str(e)}), 500

@app.route('/devolver_andaimes', methods=['PUT'])
def devolver_andaimes():
    """
    Rota para registrar a devolução de um ou mais andaimes.
    Recebe uma lista de códigos de andaimes em formato JSON.
    """
    data = request.get_json()

    if 'codigos_andaimes' not in data or not isinstance(data['codigos_andaimes'], list):
        return jsonify({"error": "Campo 'codigos_andaimes' é obrigatório e deve ser uma lista."}), 400

    codigos_a_devolver = data['codigos_andaimes']
    andaimes_devolvidos = []
    erros_devolucao = []

    try:
        for codigo in codigos_a_devolver:
            andaime = Andaime.query.filter_by(codigo=codigo).first()

            if not andaime:
                erros_devolucao.append(f"Andaime com código '{codigo}' não encontrado.")
                continue

            if andaime.status == 'disponivel':
                erros_devolucao.append(f"Andaime com código '{codigo}' já está disponível.")
                continue

            andaime.status = 'disponivel'
            andaimes_devolvidos.append(codigo)

        db.session.commit()

        if erros_devolucao:
            return jsonify({
                "message": "Processamento de devolução concluído com algumas ressalvas.",
                "andaimes_devolvidos_com_sucesso": andaimes_devolvidos,
                "erros": erros_devolucao
            }), 200
        else:
            return jsonify({
                "message": "Devolução de andaime(s) registrada com sucesso!",
                "andaimes_devolvidos": andaimes_devolvidos
            }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao registrar devolução: {e}")
        return jsonify({"error": "Ocorreu um erro ao registrar a devolução.", "details": str(e)}), 500
    
# ... (código existente, incluindo as importações) ...

# --- NOVA ROTA: Visualizar Todas as Locações Detalhadas ---
@app.route('/locacoes', methods=['GET'])
def get_locacoes():
    """
    Retorna uma lista de todas as locações com detalhes do cliente e dos andaimes.
    """
    locacoes = Locacao.query.all()
    
    locacoes_data = []
    for locacao in locacoes:
        locacoes_data.append(locacao.to_dict()) # Usa o novo método to_dict()

    return jsonify(locacoes_data), 200

# ... (restante do seu app.py, incluindo outras rotas e o bloco if __name__ == '__main__':) ...

# ... (código existente no app.py) ...

# --- NOVA ROTA: Servir a página de Visualização de Locações ---
@app.route('/visualizar_locacoes', methods=['GET'])
def get_locacoes_page():
    return render_template('locacoes.html')

# ... (resto do seu app.py) ...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tabelas criadas no banco de dados 'construara_1.db'!")

        # --- Bloco de adição de Andaimes de Teste (AGORA PODE SER REMOVIDO!) ---
        # Remova ou comente este bloco COMPLETAMENTE, pois a nova rota /andaimes fará o trabalho.
        # if Andaime.query.count() == 0:
        #     print("Adicionando andaimes de teste...")
        #     andaime1 = Andaime(codigo="AND-001", descricao="Andaime Básico 1.5x1.5", status="disponivel")
        #     andaime2 = Andaime(codigo="AND-002", descricao="Andaime Básico 1.5x1.5", status="disponivel")
        #     andaime3 = Andaime(codigo="AND-003", descricao="Andaime com Rodas", status="disponivel")
            
        #     db.session.add_all([andaime1, andaime2, andaime3])
        #     db.session.commit()
        #     print("Andaimes de teste adicionados com sucesso!")
        # else:
        #     print("Andaimes já existem no banco de dados, pulando adição de teste.")
        # --- Fim do Bloco de Andaimes de Teste ---

    app.run(debug=True)