# construara_1/models.py
from extensions import db
from datetime import datetime

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20), nullable=False)
    locacoes = db.relationship('Locacao', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

    # NOVO: Método para serializar para dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone
        }

class Andaime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    # status pode ser 'disponivel', 'alugado', 'manutencao', etc.
    status = db.Column(db.String(50), default='disponivel')
    locacoes_associadas = db.relationship('LocacaoAndaime', backref='andaime', lazy=True)

    def __repr__(self):
        return f'<Andaime {self.codigo} ({self.status})>'

    # NOVO: Método para serializar para dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'status': self.status
        }

class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    data_inicio_locacao = db.Column(db.Date, nullable=False)
    dias_locacao = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status_pagamento = db.Column(db.String(50), nullable=False) # Ex: 'pendente', 'pago_a_vista', 'parcial'
    anotacoes = db.Column(db.Text)
    andaimes_locados = db.relationship('LocacaoAndaime', backref='locacao', lazy=True)

    def __repr__(self):
        return f'<Locacao {self.id} - Cliente: {self.cliente_id}>'

    # NOVO: Método para serializar para dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_registro': self.data_registro.isoformat(), # Formato ISO para datas
            'data_inicio_locacao': self.data_inicio_locacao.isoformat(),
            'dias_locacao': self.dias_locacao,
            'valor_total': self.valor_total,
            'status_pagamento': self.status_pagamento,
            'anotacoes': self.anotacoes,
            'cliente': self.cliente.to_dict() if self.cliente else None, # Inclui dados do cliente
            'andaimes': [la.andaime.to_dict() for la in self.andaimes_locados] # Inclui andaimes
        }

class LocacaoAndaime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacao.id'), nullable=False)
    andaime_id = db.Column(db.Integer, db.ForeignKey('andaime.id'), nullable=False)

    def __repr__(self):
        return f'<LocacaoAndaime Locacao: {self.locacao_id} Andaime: {self.andaime_id}>'