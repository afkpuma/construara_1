# construara_1/routes/andaimes_bp.py
from flask import Blueprint, jsonify, render_template, request
from services.andaime_service import get_all_andaimes_disponiveis, add_andaimes_em_massa, update_andaime_status
from sqlalchemy.exc import IntegrityError # Importa para tratamento de erro específico

# Cria um objeto Blueprint
andaimes_bp = Blueprint('andaimes', __name__, url_prefix='/andaimes')

@andaimes_bp.route('/disponiveis', methods=['GET'])
def list_andaimes_disponiveis():
    """
    Retorna uma lista de todos os andaimes com status 'disponivel'.
    """
    andaimes_data = get_all_andaimes_disponiveis() # Chama a função do serviço
    return jsonify(andaimes_data), 200

@andaimes_bp.route('/', methods=['POST'])
def add_andaimes():
    """
    Adiciona vários andaimes ao sistema com base no tipo e quantidade.
    """
    data = request.get_json()

    tipo = data.get('tipo')
    quantidade = data.get('quantidade')
    status = data.get('status', 'disponivel')

    try:
        # Chama a função de serviço para adicionar os andaimes
        result = add_andaimes_em_massa(tipo, quantidade, status)
        return jsonify(result), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except IntegrityError: # Captura erro de unicidade do DB
        return jsonify({"error": "Erro de unicidade: Um código de andaime gerado já existe. Tente novamente."}), 409
    except Exception as e:
        return jsonify({"error": "Erro interno ao adicionar andaimes.", "details": str(e)}), 500

@andaimes_bp.route('/adicionar', methods=['GET']) # Rota para servir a página HTML
def add_andaime_page():
    """
    Serve a página HTML para adicionar andaimes.
    """
    return render_template('adicionar_andaime.html')
