from flask import Blueprint, request, jsonify
from database import db
from models.registro import Registro
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

registros_bp = Blueprint('registros', __name__, url_prefix='/registros')


@registros_bp.route('/', methods=['GET'])
@jwt_required()
def list_registros():
    user_id = get_jwt_identity()
    registros = Registro.query.filter_by(user_id=user_id).all()
    return jsonify([r.to_dict() for r in registros])


@registros_bp.route('/', methods=['POST'])
@jwt_required()
def create_registro():
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    descricao = data.get('descricao')
    valor = data.get('valor')
    categoria = data.get('categoria')
    data_field = data.get('data')
    tipo = data.get('tipo')

    if not descricao:
        return jsonify({'error': 'descricao is required'}), 400

    # parse date if provided
    data_parsed = None
    if data_field:
        try:
            data_parsed = datetime.fromisoformat(data_field).date()
        except Exception:
            return jsonify({'error': 'invalid date format, use ISO YYYY-MM-DD'}), 400

    reg = Registro(user_id=user_id, descricao=descricao, valor=valor, categoria=categoria, data=data_parsed, tipo=tipo)
    db.session.add(reg)
    db.session.commit()
    return jsonify(reg.to_dict()), 201


@registros_bp.route('/<int:reg_id>', methods=['GET'])
@jwt_required()
def get_registro(reg_id):
    user_id = get_jwt_identity()
    reg = Registro.query.get_or_404(reg_id)
    if reg.user_id != int(user_id):
        return jsonify({'error': 'forbidden'}), 403
    return jsonify(reg.to_dict())


@registros_bp.route('/<int:reg_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_registro(reg_id):
    user_id = get_jwt_identity()
    reg = Registro.query.get_or_404(reg_id)
    if reg.user_id != int(user_id):
        return jsonify({'error': 'forbidden'}), 403

    data = request.get_json() or {}
    descricao = data.get('descricao')
    valor = data.get('valor')
    categoria = data.get('categoria')
    data_field = data.get('data')
    tipo = data.get('tipo')

    if descricao is not None:
        reg.descricao = descricao
    if valor is not None:
        reg.valor = valor
    if categoria is not None:
        reg.categoria = categoria
    if tipo is not None:
        reg.tipo = tipo
    if data_field is not None:
        try:
            reg.data = datetime.fromisoformat(data_field).date()
        except Exception:
            return jsonify({'error': 'invalid date format, use ISO YYYY-MM-DD'}), 400

    db.session.commit()
    return jsonify(reg.to_dict())


@registros_bp.route('/<int:reg_id>', methods=['DELETE'])
@jwt_required()
def delete_registro(reg_id):
    user_id = get_jwt_identity()
    reg = Registro.query.get_or_404(reg_id)
    if reg.user_id != int(user_id):
        return jsonify({'error': 'forbidden'}), 403
    db.session.delete(reg)
    db.session.commit()
    return jsonify({'deleted': True}), 200
