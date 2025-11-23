from datetime import datetime, date
from database import db


class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=True)
    categoria = db.Column(db.String(80), nullable=True)
    data = db.Column(db.Date, nullable=True)
    tipo = db.Column(db.String(20), nullable=True)  # 'receita' ou 'despesa'
    comprado = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'descricao': self.descricao,
            'valor': self.valor,
            'categoria': self.categoria,
            'data': self.data.isoformat() if self.data else None,
            'tipo': self.tipo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Registro {self.id} user={self.user_id}>"
