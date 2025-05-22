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
    """
    Rota principal que serve a página de registro de locações.
    """
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def get_status():
    """
    Rota de teste para verificar o status do aplicativo.
    """
    return jsonify({"status": "ok", "message": "construara_1 API está online!"}), 200

@app.route('/echo', methods=['POST'])
def echo_data():
    """
    Rota de teste para ecoar dados recebidos via POST.
    """
    if request.is_json:
        data = request.get_json()
        return jsonify({"received_data": data, "message": "Dados POST recebidos com sucesso!"}), 200
    else:
        return jsonify({"error": "Content-Type deve ser application/json"}), 400

@app.route('/clientes', methods=['GET'])
def get_clientes():
    """
    Retorna uma lista de todos os clientes registrados.
    """
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
    """
    Retorna uma lista de todos os andaimes com status 'disponivel'.
    """
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

# --- ALTERADO: Rota para Adicionar Andaimes em Massa ---
@app.route('/andaimes', methods=['POST'])
def add_andaimes_em_massa():
    """
    Adiciona vários andaimes ao sistema com base no tipo e quantidade.
    Gera códigos únicos automaticamente.
    Espera um JSON com 'tipo', 'quantidade' e 'status' (opcional, padrão 'disponivel').
    """
    data = request.get_json()

    tipo = data.get('tipo')
    quantidade = data.get('quantidade')
    status = data.get('status', 'disponivel')

    if not tipo or not quantidade:
        return jsonify({"error": "Campos 'tipo' e 'quantidade' são obrigatórios."}), 400

    if tipo not in ['Andaime Normal', 'Andaime Menor']:
        return jsonify({"error": "Tipo inválido. Escolha entre 'Andaime Normal' ou 'Andaime Menor'."}), 400

    try:
        andaimes_adicionados = []
        prefixo_codigo = {
            'Andaime Normal': 'NORMAL',
            'Andaime Menor': 'MENOR'
        }.get(tipo, 'AND')

        for i in range(quantidade):
            codigo_potencial = f"{prefixo_codigo}-{str(i + 1).zfill(4)}"
            
            # Aprimoramento: Verifica se o código já existe antes de adicionar
            # Isso evita IntegrityError no commit para códigos já gerados
            if Andaime.query.filter_by(codigo=codigo_potencial).first():
                # Se o código já existe, tenta gerar um novo com um sufixo diferente
                codigo_potencial = f"{prefixo_codigo}-{str(i + 1).zfill(4)}-{datetime.now().strftime('%f')}"
                if Andaime.query.filter_by(codigo=codigo_potencial).first(): # Última tentativa
                    return jsonify({"error": f"Não foi possível gerar um código único para o {i+1}º andaime do tipo '{tipo}'. Tente novamente."}), 500

            novo_andaime = Andaime(codigo=codigo_potencial, descricao=tipo, status=status)
            db.session.add(novo_andaime)
            andaimes_adicionados.append(codigo_potencial)

        db.session.commit()

        return jsonify({
            "message": f"{quantidade} {tipo}(s) adicionados com sucesso!",
            "andaimes": andaimes_adicionados
        }), 201

    except Exception as e:
        db.session.rollback()
        # Captura IntegrityError especificamente para códigos duplicados se a verificação acima falhar
        if "UNIQUE constraint failed" in str(e):
            return jsonify({"error": "Erro de unicidade: Um código de andaime gerado já existe. Tente novamente.", "details": str(e)}), 409
        return jsonify({"error": "Erro ao adicionar andaimes.", "details": str(e)}), 500

# --- ALTERADO: Rota de Registro de Venda ---
@app.route('/registrar_venda', methods=['POST'])
def registrar_venda_refatorada():
    """
    Registra uma nova locação com base no tipo e quantidade de andaimes.
    """
    data = request.get_json()

    tipo = data.get('tipo')
    quantidade = data.get('quantidade')
    nome_cliente = data.get('nome_cliente')
    telefone_cliente = data.get('telefone_cliente')
    endereco_cliente = data.get('endereco_cliente') # NOVO: Pega o endereço
    data_inicio_locacao = data.get('data_inicio_locacao')
    dias_locacao = data.get('dias_locacao')
    valor_total = data.get('valor_total')
    status_pagamento = data.get('status_pagamento')
    anotacoes = data.get('anotacoes', '') # NOVO: Pega anotações

    if not all([tipo, quantidade, nome_cliente, telefone_cliente, data_inicio_locacao, dias_locacao, valor_total, status_pagamento]):
        return jsonify({"error": "Todos os campos obrigatórios (tipo, quantidade, nome_cliente, telefone_cliente, data_inicio_locacao, dias_locacao, valor_total, status_pagamento) são necessários."}), 400

    if tipo not in ['Andaime Normal', 'Andaime Menor']:
        return jsonify({"error": "Tipo inválido. Escolha entre 'Andaime Normal' ou 'Andaime Menor'."}), 400

    try:
        # Aprimoramento: Verifica disponibilidade E FILTRA PELO TIPO
        andaimes_disponiveis = Andaime.query.filter_by(
            status='disponivel',
            descricao=tipo # Filtra pelo tipo/descrição do andaime
        ).limit(quantidade).all()

        if len(andaimes_disponiveis) < quantidade:
            return jsonify({"error": f"Não há {quantidade} andaime(s) do tipo '{tipo}' disponíveis para locação. Apenas {len(andaimes_disponiveis)} disponíveis."}), 409

        cliente = Cliente.query.filter_by(nome=nome_cliente, telefone=telefone_cliente).first()
        if not cliente:
            # Aprimoramento: Inclui o endereço ao criar o cliente
            cliente = Cliente(nome=nome_cliente, telefone=telefone_cliente, endereco=endereco_cliente)
            db.session.add(cliente)

        nova_locacao = Locacao(
            cliente=cliente,
            data_registro=datetime.utcnow(),
            data_inicio_locacao=datetime.strptime(data_inicio_locacao, '%Y-%m-%d').date(),
            dias_locacao=dias_locacao,
            valor_total=valor_total,
            status_pagamento=status_pagamento,
            anotacoes=anotacoes # NOVO: Adiciona anotações
        )
        db.session.add(nova_locacao)

        for andaime in andaimes_disponiveis:
            andaime.status = 'alugado'
            locacao_andaime = LocacaoAndaime(locacao=nova_locacao, andaime=andaime)
            db.session.add(locacao_andaime)

        db.session.commit()

        return jsonify({
            "message": "Locação registrada com sucesso!",
            "locacao_id": nova_locacao.id,
            "cliente_id": cliente.id,
            "andaimes_locados": [a.codigo for a in andaimes_disponiveis]
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao registrar locação: {e}")
        return jsonify({"error": "Erro ao registrar locação.", "details": str(e)}), 500

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

@app.route('/locacoes', methods=['GET'])
def get_locacoes():
    """
    Retorna uma lista de todas as locações com detalhes do cliente e dos andaimes.
    """
    locacoes = Locacao.query.all()
    locacoes_data = []
    for locacao in locacoes:
        locacoes_data.append(locacao.to_dict())
    return jsonify(locacoes_data), 200

# --- NOVO: Rota para Servir a página de Visualização de Locações ---
@app.route('/visualizar_locacoes', methods=['GET'])
def get_locacoes_page():
    """
    Serve a página HTML para visualização de locações.
    """
    return render_template('locacoes.html')

# --- NOVO: Rota para Servir a página de Adição de Andaimes ---
@app.route('/adicionar_andaimes', methods=['GET'])
def add_andaime_page():
    """
    Serve a página HTML para adicionar andaimes.
    """
    return render_template('adicionar_andaime.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tabelas criadas no banco de dados 'construara_1.db'!")
        # --- ALTERADO: Bloco de adição de Andaimes de Teste REMOVIDO ---
        # Este bloco foi removido pois agora temos a rota POST /andaimes para adicionar andaimes.
    app.run(debug=True)
