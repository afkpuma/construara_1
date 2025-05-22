# construara_1/services/andaime_service.py
from models import Andaime
from extensions import db
from sqlalchemy.exc import IntegrityError

def get_all_andaimes_disponiveis():
    """Retorna todos os andaimes com status 'disponivel'."""
    andaimes = Andaime.query.filter_by(status='disponivel').all()
    return [andaime.to_dict() for andaime in andaimes]

def add_andaimes_em_massa(tipo, quantidade, status='disponivel'):
    """
    Adiciona múltiplos andaimes do mesmo tipo ao inventário.
    Gera códigos únicos baseados no tipo.
    """
    if not tipo or not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError("Tipo e quantidade são obrigatórios e quantidade deve ser um número inteiro positivo.")

    added_codes = []
    try:
        # Pega o último número para o tipo, para garantir unicidade
        last_andaime_of_type = Andaime.query.filter(Andaime.descricao == tipo) \
                                           .order_by(Andaime.id.desc()) \
                                           .first()
        if last_andaime_of_type:
            # Extrai o número do último código, ex: "NORMAL-0010" -> 10
            try:
                last_number_str = last_andaime_of_type.codigo.split('-')[-1]
                last_number = int(last_number_str)
            except (ValueError, IndexError):
                last_number = 0 # Se o formato for inesperado, começa do zero
        else:
            last_number = 0

        for i in range(quantidade):
            new_number = last_number + 1 + i
            # Formata o tipo para o código (ex: "Andaime Normal" -> "NORMAL")
            prefix = ''.join(word[0].upper() for word in tipo.split() if word.isalpha())
            if not prefix: # Fallback para tipos sem letras
                prefix = "AND"
            codigo = f"{prefix}-{new_number:04d}" # Ex: ANDN-0001, ANDM-0001, AND-0001

            andaime = Andaime(codigo=codigo, descricao=tipo, status=status)
            db.session.add(andaime)
            added_codes.append(codigo)
        db.session.commit()
        return {"message": f"{quantidade} Andaime(s) do tipo '{tipo}' adicionados com sucesso!", "andaimes": added_codes}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Erro de unicidade ao gerar código de andaime. Tente novamente.")
    except Exception as e:
        db.session.rollback()
        raise e

def update_andaime_status(codigo, new_status):
    """Atualiza o status de um andaime específico."""
    andaime = Andaime.query.filter_by(codigo=codigo).first()
    if andaime:
        andaime.status = new_status
        db.session.commit()
        return True
    return False

def get_andaimes_by_type_and_status(tipo, status='disponivel'):
    """Retorna andaimes de um tipo e status específicos."""
    return Andaime.query.filter_by(descricao=tipo, status=status).all()

def update_andaimes_status_batch(andaime_ids, new_status):
    """Atualiza o status de uma lista de andaimes por ID."""
    try:
        updated_count = Andaime.query.filter(Andaime.id.in_(andaime_ids)).update(
            {"status": new_status}, synchronize_session='fetch'
        )
        db.session.commit()
        return updated_count
    except Exception as e:
        db.session.rollback()
        raise e
