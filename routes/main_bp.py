# construara_1/routes/main_bp.py
from flask import Blueprint, render_template, jsonify, request

# Cria um objeto Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Rota principal que serve a página de registro de locações.
    """
    return render_template('index.html')

@main_bp.route('/status', methods=['GET'])
def get_status():
    """
    Rota de teste para verificar o status do aplicativo.
    """
    return jsonify({"status": "ok", "message": "construara_1 API está online!"}), 200

@main_bp.route('/echo', methods=['POST'])
def echo_data():
    """
    Rota de teste para ecoar dados recebidos via POST.
    """
    if request.is_json:
        data = request.get_json()
        return jsonify({"received_data": data, "message": "Dados POST recebidos com sucesso!"}), 200
    else:
        return jsonify({"error": "Content-Type deve ser application/json"}), 400
