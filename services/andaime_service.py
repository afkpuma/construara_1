# construara_1/services/andaime_service.py
from models import Andaime
from extensions import db
from sqlalchemy.exc import IntegrityError
import uuid # NOVO: Importa o módulo uuid

def get_all_andaimes_disponiveis():
    """Retorna todos os andaimes com status 'disponivel'."""
    andaimes = Andaime.query.filter_by(status='disponivel').all()
    return [andaime.to_dict() for andaime in andaimes]

def add_andaimes_em_massa(tipo, quantidade, status='disponivel'):
    """
    Adiciona múltiplos andaimes do mesmo tipo ao inventário.
    Gera códigos únicos usando UUIDs.
    """
    if not tipo or not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError("Tipo e quantidade são obrigatórios e quantidade deve ser um número inteiro positivo.")

    added_codes = []
    try:
        # Formata o tipo para o prefixo do código (ex: "Andaime Normal" -> "NORMAL")
        # Usamos uma lógica mais robusta para o prefixo
        prefix = ''.join(word[0].upper() for word in tipo.split() if word.isalpha())
        if not prefix:
            prefix = "AND" # Fallback se o tipo não gerar um prefixo alfabético

        for i in range(quantidade):
            # ALTERADO: Geração de código usando UUID
            # Isso garante unicidade e remove a complexidade de sequências
            codigo = f"{prefix}-{uuid.uuid4()}"

            # Uma verificação extra, embora UUIDs sejam virtualmente únicos
            if Andaime.query.filter_by(codigo=codigo).first():
                # Em caso extremamente raro de colisão de UUID (ou se o prefixo for igual)
                # Tenta gerar um novo UUID
                codigo = f"{prefix}-{uuid.uuid4()}"
                if Andaime.query.filter_by(codigo=codigo).first():
                    raise ValueError(f"Falha ao gerar um código único para o andaime do tipo '{tipo}'.")

            andaime = Andaime(codigo=codigo, descricao=tipo, status=status)
            db.session.add(andaime)
            added_codes.append(codigo)
        db.session.commit()
        return {"message": f"{quantidade} Andaime(s) do tipo '{tipo}' adicionados com sucesso!", "andaimes": added_codes}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Erro de unicidade ao adicionar andaime. Um código gerado pode já existir.")
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
