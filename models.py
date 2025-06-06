# construara_1/models.py
from extensions import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20), nullable=False)
    locacoes = db.relationship('Locacao', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone
        }

class Andaime(db.Model):
    __tablename__ = 'andaimes'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    status = db.Column(db.String(50), nullable=False, default='disponivel')
    locacoes_associadas = db.relationship('LocacaoAndaime', backref='andaime', lazy=True)

    def __repr__(self):
        return f'<Andaime {self.codigo} ({self.status})>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'status': self.status
        }

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
        return f'<Locacao {self.id} - Cliente: {self.cliente_id}>'

    # ALTERADO: Método para serializar para dicionário, agora com contagem e tipo de andaimes
    def to_dict(self):
        # Assumimos que todos os andaimes em uma locação são do mesmo tipo
        # baseado na lógica de registro de venda por tipo/quantidade.
        # Se houver andaimes, pega o tipo do primeiro.
        tipo_andaimes = self.andaimes_locados[0].andaime.descricao if self.andaimes_locados else None
        quantidade_andaimes = len(self.andaimes_locados)

        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_registro': self.data_registro.isoformat(),
            'data_inicio_locacao': self.data_inicio_locacao.isoformat(),
            'dias_locacao': self.dias_locacao,
            'valor_total': self.valor_total,
            'status_pagamento': self.status_pagamento,
            'anotacoes': self.anotacoes,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            # ALTERADO: Retorna a quantidade e o tipo, não a lista de andaimes
            'andaimes_info': {
                'quantidade': quantidade_andaimes,
                'tipo': tipo_andaimes
            } if tipo_andaimes else None
        }

class LocacaoAndaime(db.Model):
    __tablename__ = 'locacao_andaimes'
    id = db.Column(db.Integer, primary_key=True)
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacoes.id'), nullable=False)
    andaime_id = db.Column(db.Integer, db.ForeignKey('andaimes.id'), nullable=False)

    def __repr__(self):
        return f'<LocacaoAndaime Locacao: {self.locacao_id} Andaime: {self.andaime_id}>'
