from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.compra_controller import CompraController
from models.user import User
from datetime import datetime

compras_bp = Blueprint('compras', __name__)


def require_login_redirect():
    flash('Faça login para acessar essa página.', 'error')
    return redirect(url_for('compras.login'))


@compras_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('compras/login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash('Usuário e senha são obrigatórios', 'error')
        return redirect(url_for('compras.login'))

    user = User.query.filter((User.username == username) | (User.email == username)).first()
    if not user or not user.check_password(password):
        flash('Credenciais inválidas', 'error')
        return redirect(url_for('compras.login'))

    session['user_id'] = user.id
    session['username'] = user.username
    flash('Logado com sucesso', 'success')
    return redirect(url_for('compras.index'))



@compras_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('compras/register.html')

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not username or not email or not password:
        flash('Todos os campos são obrigatórios', 'error')
        return redirect(url_for('compras.register'))

    # check existing
    if User.query.filter((User.username == username) | (User.email == email)).first():
        flash('Usuário ou e-mail já cadastrado', 'error')
        return redirect(url_for('compras.register'))

    # create user
    from database import db
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username
    flash('Conta criada e logado', 'success')
    return redirect(url_for('compras.index'))


@compras_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logout realizado', 'success')
    return redirect(url_for('compras.login'))


@compras_bp.route('/')
def index():
    # require login to view/manage compras
    user_id = session.get('user_id')
    if not user_id:
        return require_login_redirect()

    status = request.args.get('status')  # all | carrinho | pendentes
    compras = CompraController.list_compras(filter_status=status)
    # filter to only user's compras
    compras = [c for c in compras if c.user_id is not None and int(c.user_id) == int(user_id)]
    return render_template('compras/index.html', compras=compras, status=status or 'Todos')


@compras_bp.route('/adicionar', methods=['POST'])
def adicionar():
    user_id = session.get('user_id')
    if not user_id:
        return require_login_redirect()

    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    categoria = request.form.get('categoria')
    data_field = request.form.get('data')

    if not descricao:
        flash('Descrição é obrigatória', 'error')
        return redirect(url_for('compras.index'))

    valor_parsed = None
    try:
        if valor:
            valor_parsed = float(valor)
    except ValueError:
        flash('Valor inválido', 'error')
        return redirect(url_for('compras.index'))

    data_parsed = None
    if data_field:
        try:
            data_parsed = datetime.fromisoformat(data_field).date()
        except Exception:
            flash('Formato de data inválido. Use YYYY-MM-DD', 'error')
            return redirect(url_for('compras.index'))

    CompraController.add_compra(descricao=descricao, valor=valor_parsed, categoria=categoria, data_field=data_parsed, user_id=user_id)
    flash('Item adicionado', 'success')
    return redirect(url_for('compras.index'))


@compras_bp.route('/remover/<int:compra_id>', methods=['POST', 'GET'])
def remover(compra_id: int):
    user_id = session.get('user_id')
    if not user_id:
        return require_login_redirect()

    # ensure the compra belongs to current user
    from models.registro import Registro
    reg = Registro.query.get(compra_id)
    if not reg or reg.user_id != int(user_id):
        flash('Compra não encontrada ou sem permissão', 'error')
        return redirect(url_for('compras.index'))

    ok = CompraController.remove_compra(compra_id)
    if not ok:
        flash('Compra não encontrada', 'error')
    else:
        flash('Compra removida', 'success')
    return redirect(url_for('compras.index'))


@compras_bp.route('/concluir/<int:compra_id>', methods=['POST', 'GET'])
def concluir(compra_id: int):
    user_id = session.get('user_id')
    if not user_id:
        return require_login_redirect()

    from models.registro import Registro
    reg = Registro.query.get(compra_id)
    if not reg or reg.user_id != int(user_id):
        flash('Compra não encontrada ou sem permissão', 'error')
        return redirect(url_for('compras.index'))

    reg = CompraController.toggle_comprado(compra_id)
    if not reg:
        flash('Compra não encontrada', 'error')
    else:
        # show a friendly message when toggling cart status
        if reg.comprado:
            flash('Adicionado ao carrinho', 'success')
        else:
            flash('Removido do carrinho', 'success')
    return redirect(url_for('compras.index'))


@compras_bp.route('/editar/<int:compra_id>', methods=['GET', 'POST'])
def editar(compra_id: int):
    user_id = session.get('user_id')
    if not user_id:
        return require_login_redirect()

    from models.registro import Registro
    reg = Registro.query.get(compra_id)
    if not reg or reg.user_id != int(user_id):
        flash('Compra não encontrada ou sem permissão', 'error')
        return redirect(url_for('compras.index'))

    if request.method == 'GET':
        return render_template('compras/edit.html', compra=reg)

    # POST -> perform update
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    categoria = request.form.get('categoria')
    data_field = request.form.get('data')

    if not descricao:
        flash('Descrição é obrigatória', 'error')
        return redirect(url_for('compras.editar', compra_id=compra_id))

    valor_parsed = None
    try:
        if valor:
            valor_parsed = float(valor)
    except ValueError:
        flash('Valor inválido', 'error')
        return redirect(url_for('compras.editar', compra_id=compra_id))

    data_parsed = None
    if data_field:
        try:
            data_parsed = datetime.fromisoformat(data_field).date()
        except Exception:
            flash('Formato de data inválido. Use YYYY-MM-DD', 'error')
            return redirect(url_for('compras.editar', compra_id=compra_id))

    CompraController.update_compra(compra_id=compra_id, descricao=descricao, valor=valor_parsed, categoria=categoria, data_field=data_parsed)
    flash('Compra atualizada', 'success')
    return redirect(url_for('compras.index'))
