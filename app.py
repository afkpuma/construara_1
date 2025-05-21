from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # Para trabalhar com datas e horas

app = Flask(__name__)

# --- Configuração do Banco de Dados SQLite ---
# Define o URI do banco de dados. 'sqlite:///site.db' cria um arquivo 'site.db' na mesma pasta do app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construara_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa o rastreamento de modificações para economizar memória

db = SQLAlchemy(app) # Inicializa o SQLAlchemy com o aplicativo Flask

# --- Definição dos Modelos do Banco de Dados ---

# Tabela clientes
class Cliente(db.Model):
    __tablename__ = 'clientes' # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) # String para TEXT, 100 caracteres max
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20), nullable=False)

    # Relacionamento com Locacoes: um cliente pode ter muitas locacoes
    locacoes = db.relationship('Locacao', backref='cliente', lazy=True)

    def __repr__(self):
        return f"Cliente('{self.nome}', '{self.telefone}')"

# Tabela andaimes
class Andaime(db.Model):
    __tablename__ = 'andaimes'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    status = db.Column(db.String(50), nullable=False, default='disponivel') # 'disponivel', 'alugado', 'manutencao'

    # Relacionamento com LocacaoAndaime (tabela de junção)
    locacoes_associadas = db.relationship('LocacaoAndaime', backref='andaime', lazy=True)

    def __repr__(self):
        return f"Andaime('{self.codigo}', '{self.status}')"

# Tabela locacoes
class Locacao(db.Model):
    __tablename__ = 'locacoes'
    id = db.Column(db.Integer, primary_key=True)
    
    # Chave estrangeira para Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    data_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Data e hora do registro
    data_inicio_locacao = db.Column(db.Date, nullable=False) # Apenas a data de início da locação
    dias_locacao = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False) # Float para REAL
    status_pagamento = db.Column(db.String(50), nullable=False) # 'pago_a_vista', 'pendente_entrega', etc.
    anotacoes = db.Column(db.Text) # Text para TEXT

    # Relacionamento com LocacaoAndaime (tabela de junção)
    andaimes_locados = db.relationship('LocacaoAndaime', backref='locacao', lazy=True)

    def __repr__(self):
        return f"Locacao('{self.id}', Cliente ID: '{self.cliente_id}', '{self.data_registro}')"

# Tabela de junção locacao_andaimes (para Many-to-Many)
class LocacaoAndaime(db.Model):
    __tablename__ = 'locacao_andaimes'
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacoes.id'), primary_key=True)
    andaime_id = db.Column(db.Integer, db.ForeignKey('andaimes.id'), primary_key=True)

    def __repr__(self):
        return f"LocacaoAndaime(Locacao ID: {self.locacao_id}, Andaime ID: {self.andaime_id})"




if __name__ == '__main__':
    # --- Criação das Tabelas (APENAS PARA O PRIMEIRO SETUP OU RESET!) ---
    # Este bloco é para criar as tabelas no banco de dados.
    # Em um ambiente de produção, você usaria migrations (Flask-Migrate).
    # Para desenvolvimento, pode rodar uma vez ou quando precisar resetar.
    with app.app_context():
        db.create_all()
        print("Tabelas criadas no banco de dados 'construara_1.db'!")
    # --- Fim do bloco de criação de tabelas ---

    app.run(debug=True)