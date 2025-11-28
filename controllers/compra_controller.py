from typing import List, Optional
from models.registro import Registro
from database import db
from datetime import date


class CompraController:
    """Controller (POO) que encapsula operações sobre a entidade Compra (Registro)."""

    @staticmethod
    def list_compras(filter_status: Optional[str] = None) -> List[Registro]:
        q = Registro.query
        # support both 'comprados' and 'carrinho' as synonyms for items added to cart
        if filter_status in ('comprados', 'carrinho'):
            q = q.filter_by(comprado=True)
        elif filter_status == 'pendentes':
            q = q.filter_by(comprado=False)
        return q.order_by(Registro.comprado.asc(), Registro.created_at.desc()).all()

    @staticmethod
    def add_compra(descricao: str, valor: Optional[float] = None, categoria: Optional[str] = None,
                   data_field: Optional[date] = None, user_id: Optional[int] = None) -> Registro:
        reg = Registro(descricao=descricao, valor=valor, categoria=categoria, data=data_field, user_id=user_id)
        db.session.add(reg)
        db.session.commit()
        return reg

    @staticmethod
    def remove_compra(compra_id: int) -> bool:
        reg = Registro.query.get(compra_id)
        if not reg:
            return False
        db.session.delete(reg)
        db.session.commit()
        return True

    @staticmethod
    def toggle_comprado(compra_id: int) -> Optional[Registro]:
        reg = Registro.query.get(compra_id)
        if not reg:
            return None
        reg.comprado = not bool(reg.comprado)
        db.session.commit()
        return reg

    @staticmethod
    def update_compra(compra_id: int, descricao: Optional[str] = None, valor: Optional[float] = None,
                      categoria: Optional[str] = None, data_field: Optional[date] = None) -> Optional[Registro]:
        reg = Registro.query.get(compra_id)
        if not reg:
            return None
        if descricao is not None:
            reg.descricao = descricao
        if valor is not None:
            reg.valor = valor
        if categoria is not None:
            reg.categoria = categoria
        if data_field is not None:
            reg.data = data_field
        db.session.commit()
        return reg
