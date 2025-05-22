# construara_1/routes/clientes_bp.py
from flask import Blueprint, jsonify
from services.cliente_service import get_all_clientes

# Cria um objeto Blueprint
clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/', methods=['GET'])
def list_clientes():
    """
    Retorna uma lista de todos os clientes registrados.
    """
    clientes_data = get_all_clientes() # Chama a função do serviço
    return jsonify(clientes_data), 200
