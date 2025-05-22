# construara_1/services/cliente_service.py
from models import Cliente
from extensions import db

def get_all_clientes():
    """Retorna todos os clientes cadastrados."""
    clientes = Cliente.query.all()
    return [cliente.to_dict() for cliente in clientes]

def get_or_create_cliente(nome, telefone, endereco=None):
    """
    Busca um cliente existente pelo nome e telefone, ou o cria se não existir.
    """
    cliente = Cliente.query.filter_by(nome=nome, telefone=telefone).first()
    if not cliente:
        cliente = Cliente(nome=nome, telefone=telefone, endereco=endereco)
        db.session.add(cliente)
        db.session.commit()
    return cliente
