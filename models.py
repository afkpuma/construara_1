# construara_1/models.py
from app import db # Importa a instância 'db' de app.py
from datetime import datetime # Para trabalhar com datas e horas

# Tabela clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20), nullable=False)
    locacoes = db.relationship('Locacao', backref='cliente', lazy=True)

    def __repr__(self):
        return f"Cliente('{self.nome}', '{self.telefone}')"

# Tabela andaimes
class Andaime(db.Model):
    __tablename__ = 'andaimes'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    status = db.Column(db.String(50), nullable=False, default='disponivel')
    locacoes_associadas = db.relationship('LocacaoAndaime', backref='andaime', lazy=True)

    def __repr__(self):
        return f"Andaime('{self.codigo}', '{self.status}')"

# Tabela locacoes
class Locacao(db.Model):
    __tablename__ = 'locacoes'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_inicio_locacao = db.Column(db.Date, nullable=False)
    dias_locacao = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status_pagamento = db.Column(db.String(50), nullable=False)
    anotacoes = db.Column(db.Text)
    andaimes_locados = db.relationship('LocacaoAndaime', backref='locacao', lazy=True)

    def __repr__(self):
        return f"Locacao('{self.id}', Cliente ID: '{self.cliente_id}', '{self.data_registro}')"

# Tabela de junção locacao_andaimes
class LocacaoAndaime(db.Model):
    __tablename__ = 'locacao_andaimes'
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacoes.id'), primary_key=True)
    andaime_id = db.Column(db.Integer, db.ForeignKey('andaimes.id'), primary_key=True)

    def __repr__(self):
        return f"LocacaoAndaime(Locacao ID: {self.locacao_id}, Andaime ID: {self.andaime_id})"