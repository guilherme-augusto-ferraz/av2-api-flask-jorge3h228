from flask import Blueprint, request, jsonify
from database import db
from models.registro import Registro
from models.user import User

registros_bp = Blueprint('registros', __name__, url_prefix='/registros')


@registros_bp.route('/', methods=['GET'])
def list_registros():
    registros = Registro.query.all()
    return jsonify([r.to_dict() for r in registros])


@registros_bp.route('/', methods=['POST'])
def create_registro():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    descricao = data.get('descricao')
    valor = data.get('valor')

    if not user_id or not descricao:
        return jsonify({'error': 'user_id and descricao are required'}), 400

    if not User.query.get(user_id):
        return jsonify({'error': 'user not found'}), 404

    reg = Registro(user_id=user_id, descricao=descricao, valor=valor)
    db.session.add(reg)
    db.session.commit()
    return jsonify(reg.to_dict()), 201


@registros_bp.route('/<int:reg_id>', methods=['GET'])
def get_registro(reg_id):
    reg = Registro.query.get_or_404(reg_id)
    return jsonify(reg.to_dict())
