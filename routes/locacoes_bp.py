# construara_1/routes/locacoes_bp.py
from flask import Blueprint, jsonify, request, render_template
from services.locacao_service import get_all_locacoes, register_locacao, devolve_andaimes

# Cria um objeto Blueprint
locacoes_bp = Blueprint('locacoes', __name__, url_prefix='/locacoes')

@locacoes_bp.route('/', methods=['GET'])
def list_locacoes():
    """
    Retorna uma lista de todas as locações com detalhes completos.
    """
    locacoes_data = get_all_locacoes() # Chama a função do serviço
    return jsonify(locacoes_data), 200

@locacoes_bp.route('/', methods=['POST'])
def create_locacao():
    """
    Registra uma nova locação com base no tipo e quantidade de andaimes.
    """
    data = request.get_json()
    try:
        result = register_locacao(data) # Chama a função de serviço
        return jsonify(result), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro ao registrar locação.", "details": str(e)}), 500

@locacoes_bp.route('/devolver', methods=['PUT'])
def return_andaimes():
    """
    Processa a devolução de uma lista de andaimes por seus códigos.
    """
    data = request.get_json()
    codigos_andaimes = data.get('codigos_andaimes', [])

    try:
        result = devolve_andaimes(codigos_andaimes) # Chama a função de serviço
        if result.get("erros"):
            return jsonify(result), 200 # Ainda 200 se houver sucesso parcial
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro ao processar devolução.", "details": str(e)}), 500

@locacoes_bp.route('/visualizar', methods=['GET']) # Rota para servir a página HTML
def view_locacoes_page():
    """
    Serve a página HTML para visualização de locações.
    """
    return render_template('locacoes.html')
