# construara_1/app.py
from flask import Flask
from extensions import db
import os # Importa o módulo os para lidar com variáveis de ambiente e caminhos de arquivo

# Importa os Blueprints
from routes.main_bp import main_bp
from routes.clientes_bp import clientes_bp
from routes.andaimes_bp import andaimes_bp
from routes.locacoes_bp import locacoes_bp

app = Flask(__name__)

# --- Configuração do Banco de Dados PostgreSQL (via variável de ambiente Docker) ---
# ALTERADO: Pega a URI do banco de dados da variável de ambiente DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///construara_1.db')
# O segundo argumento ('sqlite:///construara_1.db') é um fallback para desenvolvimento local sem Docker,
# mas com Docker, a variável DATABASE_URL será sempre definida.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Associa o objeto 'app' com 'db'
db.init_app(app)

# --- Registro dos Blueprints ---
app.register_blueprint(main_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(andaimes_bp)
app.register_blueprint(locacoes_bp)

if __name__ == '__main__':
    with app.app_context():
        # Quando rodando com Docker Compose, o banco de dados 'construara_1' já será criado
        # pelo serviço 'db' e db.create_all() criará as tabelas dentro dele.
        db.create_all()
        print("Tabelas criadas no banco de dados!") # Mensagem mais genérica
    app.run(debug=True)

