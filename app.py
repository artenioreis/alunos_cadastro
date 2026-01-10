import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Aluno, Usuario
from forms import AlunoForm, LoginForm, RegistroUsuarioForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')

db.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def salvar_foto(foto_file):
    if foto_file and hasattr(foto_file, 'filename') and foto_file.filename != '':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(foto_file.filename)
        nome_arquivo = f"{timestamp}_{filename}"
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        foto_file.save(caminho)
        return nome_arquivo
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        flash('Usuário ou senha incorretos', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

@app.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.username).all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/registrar_usuario', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(username=form.username.data).first():
            flash('Este usuário já existe.', 'warning')
        else:
            hash_pw = generate_password_hash(form.password.data)
            novo_user = Usuario(username=form.username.data, password=hash_pw)
            db.session.add(novo_user)
            db.session.commit()
            flash(f'Usuário {novo_user.username} criado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))
    return render_template('registrar_usuario.html', form=form)

@app.route('/excluir_usuario/<int:id>', methods=['POST'])
@login_required
def excluir_usuario(id):
    if id == session.get('user_id'):
        flash('Você não pode excluir o usuário que está usando no momento.', 'danger')
        return redirect(url_for('listar_usuarios'))
    
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário removido com sucesso!', 'success')
    return redirect(url_for('listar_usuarios'))

@app.route('/')
@login_required
def index():
    termo_busca = request.args.get('q', '')
    if termo_busca:
        alunos = Aluno.query.filter(Aluno.nome_completo.ilike(f'%{termo_busca}%')).order_by(Aluno.nome_completo).all()
    else:
        alunos = Aluno.query.order_by(Aluno.nome_completo).all()
    
    cultural = Aluno.query.filter_by(setor='CULTURAL').count()
    profissional = Aluno.query.filter_by(setor='PROFISSIONALIZANTE').count()
    bolsa = Aluno.query.filter_by(bolsa_familia=True).count()
    return render_template('index.html', alunos=alunos, cultural=cultural, profissionalizante=profissional, bolsa_familia=bolsa, total_alunos=len(alunos), termo_busca=termo_busca)

@app.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    form = AlunoForm()
    if form.validate_on_submit():
        foto_nome = salvar_foto(form.foto.data)
        novo_aluno = Aluno()
        form.populate_obj(novo_aluno)
        novo_aluno.foto = foto_nome
        novo_aluno.atualizar_idade()
        db.session.add(novo_aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('cadastrar.html', form=form)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    aluno = Aluno.query.get_or_404(id)
    form = AlunoForm(obj=aluno)
    if form.validate_on_submit():
        foto_atual = aluno.foto
        if form.foto.data and hasattr(form.foto.data, 'filename') and form.foto.data.filename != '':
            nova = salvar_foto(form.foto.data)
            if nova:
                if aluno.foto:
                    path = os.path.join(app.config['UPLOAD_FOLDER'], aluno.foto)
                    if os.path.exists(path): os.remove(path)
                foto_atual = nova
        form.populate_obj(aluno)
        aluno.foto = foto_atual
        aluno.atualizar_idade()
        db.session.commit()
        flash('Atualizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('editar.html', form=form, aluno=aluno)

@app.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    aluno = Aluno.query.get_or_404(id)
    if aluno.foto:
        path = os.path.join(app.config['UPLOAD_FOLDER'], aluno.foto)
        if os.path.exists(path): os.remove(path)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/visualizar/<int:id>')
@login_required
def visualizar(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('visualizar.html', aluno=aluno)

@app.route('/imprimir/<int:id>')
@login_required
def imprimir(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('ficha_impressao.html', aluno=aluno)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def utility_processor():
    def format_currency(value): return f"R$ {value:,.2f}".replace('.', ',')
    def format_date(value): return value.strftime('%d/%m/%Y') if value else ""
    return dict(format_currency=format_currency, format_date=format_date, now=datetime.now())

with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(username='admin', password=generate_password_hash('1234'))
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)