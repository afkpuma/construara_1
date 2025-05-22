# construara_1/app.py
from flask import Flask
from extensions import db
import os # Importa o módulo os para lidar com caminhos de arquivo

# Importa os Blueprints
from routes.main_bp import main_bp
from routes.clientes_bp import clientes_bp
from routes.andaimes_bp import andaimes_bp
from routes.locacoes_bp import locacoes_bp

app = Flask(__name__)

# --- Configuração do Banco de Dados SQLite ---
# Garante que o caminho do banco de dados seja absoluto
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'construara_1.db')
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
        # Cria as tabelas no banco de dados se não existirem
        # Isso deve ser executado apenas uma vez ou em ambiente de desenvolvimento
        db.create_all()
        print("Tabelas criadas no banco de dados 'construara_1.db'!")
    app.run(debug=True)

