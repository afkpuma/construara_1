# construara_1/services/locacao_service.py
from models import Andaime, Locacao, LocacaoAndaime
from extensions import db
from datetime import datetime, date
from services.cliente_service import get_or_create_cliente
from services.andaime_service import get_andaimes_by_type_and_status, update_andaimes_status_batch

def get_all_locacoes():
    """Retorna todas as locações com detalhes completos."""
    locacoes = Locacao.query.all()
    return [locacao.to_dict() for locacao in locacoes]

def register_locacao(data):
    """
    Registra uma nova locação, incluindo criação/busca de cliente
    e associação de andaimes por tipo/quantidade.
    """
    # Validações básicas dos dados de entrada
    required_fields = [
        'nome_cliente', 'telefone_cliente', 'data_inicio_locacao',
        'dias_locacao', 'valor_total', 'status_pagamento',
        'tipo', 'quantidade'
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Campo '{field}' é obrigatório.")

    try:
        nome_cliente = data['nome_cliente']
        telefone_cliente = data['telefone_cliente']
        endereco_cliente = data.get('endereco_cliente')
        data_inicio_locacao_str = data['data_inicio_locacao']
        dias_locacao = data['dias_locacao']
        valor_total = data['valor_total']
        status_pagamento = data['status_pagamento']
        anotacoes = data.get('anotacoes')
        tipo_andaime = data['tipo']
        quantidade_andaimes = data['quantidade']

        # Converte a data de string para objeto date
        data_inicio_locacao = datetime.strptime(data_inicio_locacao_str, '%Y-%m-%d').date()
        if not isinstance(dias_locacao, int) or dias_locacao <= 0:
            raise ValueError("Número de dias de locação inválido.")
        if not isinstance(valor_total, (float, int)) or valor_total <= 0:
            raise ValueError("Valor total da locação inválido.")

        # 1. Obter ou criar o cliente
        cliente = get_or_create_cliente(nome_cliente, telefone_cliente, endereco_cliente)

        # 2. Buscar andaimes disponíveis do tipo e quantidade solicitados
        andaimes_disponiveis = get_andaimes_by_type_and_status(tipo_andaime, 'disponivel')

        if len(andaimes_disponiveis) < quantidade_andaimes:
            raise ValueError(f"Não há {quantidade_andaimes} andaime(s) do tipo '{tipo_andaime}' disponíveis para locação. Apenas {len(andaimes_disponiveis)} disponíveis.")

        # Seleciona os primeiros 'quantidade_andaimes' disponíveis
        andaimes_selecionados = andaimes_disponiveis[:quantidade_andaimes]

        # 3. Criar a nova locação
        locacao = Locacao(
            cliente_id=cliente.id,
            data_registro=datetime.now(), # Alterado para datetime.now() conforme aviso de deprecation
            data_inicio_locacao=data_inicio_locacao,
            dias_locacao=dias_locacao,
            valor_total=valor_total,
            status_pagamento=status_pagamento,
            anotacoes=anotacoes
        )
        db.session.add(locacao)
        db.session.flush() # flush para ter acesso ao locacao.id antes do commit final

        # 4. Associar andaimes à locação e atualizar status
        andaime_ids_para_atualizar = []
        andaimes_locados_codigos = []
        for andaime in andaimes_selecionados:
            locacao_andaime = LocacaoAndaime(locacao_id=locacao.id, andaime_id=andaime.id)
            db.session.add(locacao_andaime)
            andaime_ids_para_atualizar.append(andaime.id)
            andaimes_locados_codigos.append(andaime.codigo)

        # Atualiza o status dos andaimes em batch
        update_andaimes_status_batch(andaime_ids_para_atualizar, 'alugado')

        db.session.commit()

        return {
            "message": "Locação registrada com sucesso!",
            "locacao_id": locacao.id,
            "cliente_id": cliente.id,
            "andaimes_locados": andaimes_locados_codigos
        }

    except ValueError as ve:
        db.session.rollback()
        raise ve
    except Exception as e:
        db.session.rollback()
        # Logar o erro 'e' para depuração
        raise Exception(f"Erro inesperado ao registrar locação: {str(e)}")

def devolve_andaimes(codigos_andaimes):
    """
    Processa a devolução de uma lista de andaimes por seus códigos.
    Retorna um dicionário com andaimes devolvidos com sucesso e erros.
    """
    if not isinstance(codigos_andaimes, list) or not codigos_andaimes:
        raise ValueError("Lista de códigos de andaimes é obrigatória.")

    devolvidos_com_sucesso = []
    erros = []

    for codigo in codigos_andaimes:
        andaime = Andaime.query.filter_by(codigo=codigo).first()
        if not andaime:
            erros.append(f"Andaime com código '{codigo}' não encontrado.")
            continue
        if andaime.status == 'disponivel':
            erros.append(f"Andaime com código '{codigo}' já está disponível.")
            continue

        try:
            andaime.status = 'disponivel'
            db.session.add(andaime) # Adiciona à sessão para que a mudança seja monitorada
            devolvidos_com_sucesso.append(codigo)
        except Exception as e:
            erros.append(f"Erro ao atualizar status do andaime '{codigo}': {str(e)}")

    if devolvidos_com_sucesso:
        db.session.commit() # Commit as mudanças de todos os andaimes que puderam ser atualizados
    else:
        db.session.rollback() # Se não houve nenhum andaime a ser devolvido com sucesso, rollback.

    return {
        "message": "Devolução processada.",
        "andaimes_devolvidos_com_sucesso": devolvidos_com_sucesso,
        "erros": erros
    }
