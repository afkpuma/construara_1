# construara_1/app.py
from flask import Flask 
from extensions import db
from routes.main_bp import main_bp
from routes.clientes_bp import clientes_bp
from routes.andaimes_bp import andaimes_bp
from routes.locacoes_bp import locacoes_bp

# IMPORTANTE: Importa os Modelos do Banco de Dados para que db.create_all() possa descobri-los
from models import Cliente, Andaime, Locacao, LocacaoAndaime

app = Flask(__name__)

# --- Configuração do Banco de Dados MariaDB/MySQL (via XAMPP) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/construara_1'
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
        db.create_all()
        print("Tabelas criadas no banco de dados 'construara_1' (MariaDB/MySQL)!")

        # --- Bloco de adição de Andaimes de Teste (Certifique-se de que está removido ou comentado) ---
        # Remova ou comente este bloco COMPLETAMENTE, pois a nova rota /andaimes fará o trabalho.
        # if Andaime.query.count() == 0:
        #     print("Adicionando andaimes de teste...")
        #     andaime1 = Andaime(codigo="AND-001", descricao="Andaime Básico 1.5x1.5", status="disponivel")
        #     andaime2 = Andaime(codigo="AND-002", descricao="Andaime Básico 1.5x1.5", status="disponivel")
        #     andaime3 = Andaime(codigo="AND-003", descricao="Andaime com Rodas", status="disponivel")
        #     db.session.add_all([andaime1, andaime2, andaime3])
        #     db.session.commit()
        #     print("Andaimes de teste adicionados.")

    app.run(debug=True)

