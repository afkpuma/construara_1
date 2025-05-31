# construara_1/app.py
from flask import Flask 
from extensions import db
from routes.main_bp import main_bp
from routes.clientes_bp import clientes_bp
from routes.andaimes_bp import andaimes_bp
from routes.locacoes_bp import locacoes_bp
from flask_migrate import Migrate

# IMPORTANTE: Importa os Modelos do Banco de Dados para que db.create_all() possa descobri-los
from models import Cliente, Andaime, Locacao, LocacaoAndaime

app = Flask(__name__)

# --- Configuração do Banco de Dados MariaDB/MySQL (via XAMPP) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/construara_1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Associa o objeto 'app' com 'db'
db.init_app(app)

# NOVO: Inicializa o Flask-Migrate
migrate = Migrate(app, db) # Passa a instância do app e do db para o Migrate

# --- Registro dos Blueprints ---
app.register_blueprint(main_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(andaimes_bp)
app.register_blueprint(locacoes_bp)

if __name__ == '__main__':
    with app.app_context():
            print("Preparando para iniciar a aplicação. As migrações do banco de dados serão gerenciadas via 'flask db'.")

    app.run(debug=True)

