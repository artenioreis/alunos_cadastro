import os
import uuid
import webbrowser
from datetime import datetime
from threading import Timer
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from waitress import serve  # Servidor de produção

# Importações internas do seu projeto
from models import db, Aluno, Usuario
from forms import AlunoForm, LoginForm, RegistroUsuarioForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
db.init_app(app)

# Inicialização do Banco e Modo WAL (Essencial para funcionamento estável em rede)
with app.app_context():
    db.create_all()
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text("PRAGMA journal_mode=WAL;"))
    except Exception as e:
        print(f"Aviso ao ativar modo WAL: {e}")
    
    # Cria o usuário inicial admin:1234 se o sistema estiver vazio
    if not Usuario.query.filter_by(username='admin').first():
        db.session.add(Usuario(username='admin', password=generate_password_hash('1234')))
        db.session.commit()
        print("Usuário administrador inicial criado (admin:1234)")

# --- Tratamento de Erros e Sessão ---

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('O ficheiro é demasiado grande! O limite máximo para anexos é de 64MB.', 'danger')
    return redirect(request.referrer or url_for('index'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def salvar_arquivo(file):
    if file and hasattr(file, 'filename') and file.filename != '':
        uid = str(uuid.uuid4())[:8]
        nome = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uid}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nome))
        return nome
    return None

# --- Rotas Principais ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session.permanent = True
            session['logged_in'] = True
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Usuário ou senha incorretos', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    termo = request.args.get('q', '')
    query = Aluno.query
    if termo:
        alunos = query.filter(Aluno.nome_completo.ilike(f'%{termo}%')).order_by(Aluno.nome_completo).all()
    else:
        alunos = query.order_by(Aluno.nome_completo).all()
    
    # Cálculo exato para os 8 cards do Dashboard
    stats = {
        'ativos': Aluno.query.filter_by(desistencia='NÃO').count(),
        'desistentes': Aluno.query.filter_by(desistencia='SIM').count(),
        'cultural': Aluno.query.filter_by(setor='CULTURAL', desistencia='NÃO').count(),
        'profissionalizante': Aluno.query.filter_by(setor='PROFISSIONALIZANTE', desistencia='NÃO').count(),
        'bolsa_familia': Aluno.query.filter_by(bolsa_familia=True, desistencia='NÃO').count(),
        'criancas': Aluno.query.filter(Aluno.idade < 12, Aluno.desistencia == 'NÃO').count(),
        'adolescentes': Aluno.query.filter(Aluno.idade >= 12, Aluno.idade < 18, Aluno.desistencia == 'NÃO').count(),
        'adultos': Aluno.query.filter(Aluno.idade >= 18, Aluno.desistencia == 'NÃO').count(),
        'total_alunos': len(alunos),
        'termo_busca': termo
    }
    return render_template('index.html', alunos=alunos, **stats)

@app.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    form = AlunoForm()
    if form.validate_on_submit():
        try:
            novo = Aluno()
            form.populate_obj(novo)
            novo.foto = salvar_arquivo(form.foto.data)
            novo.documento = salvar_arquivo(form.documento.data)
            novo.atualizar_idade()
            db.session.add(novo)
            db.session.commit()
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar: {str(e)}", "danger")
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erro no campo {getattr(form, field).label.text}: {error}", "warning")
    return render_template('cadastrar.html', form=form)

@app.route('/visualizar/<int:id>')
@login_required
def visualizar(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('visualizar.html', aluno=aluno)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    aluno = Aluno.query.get_or_404(id)
    form = AlunoForm(obj=aluno)
    if form.validate_on_submit():
        try:
            foto_anterior = aluno.foto
            doc_anterior = aluno.documento
            form.populate_obj(aluno)
            
            # Corrige a troca de fotos: salva apenas o nome (string) no banco
            if form.foto.data and hasattr(form.foto.data, 'filename') and form.foto.data.filename != '':
                aluno.foto = salvar_arquivo(form.foto.data)
            else:
                aluno.foto = foto_anterior
                
            if form.documento.data and hasattr(form.documento.data, 'filename') and form.documento.data.filename != '':
                aluno.documento = salvar_arquivo(form.documento.data)
            else:
                aluno.documento = doc_anterior
                
            aluno.atualizar_idade()
            db.session.commit()
            flash('Cadastro atualizado!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao editar: {str(e)}", "danger")
    return render_template('editar.html', form=form, aluno=aluno)

@app.route('/imprimir/<int:id>')
@login_required
def imprimir(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('ficha_impressao.html', aluno=aluno)

@app.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Registro excluído!', 'info')
    return redirect(url_for('index'))

# --- Gestão de Sistema e Usuários ---

@app.route('/relatorio')
@login_required
def relatorio():
    alunos = Aluno.query.order_by(Aluno.nome_completo).all()
    return render_template('relatorio.html', alunos=alunos)

@app.route('/backup_db')
@login_required
def backup_db():
    return send_from_directory(app.config['BASE_DIR'], 'database.db', as_attachment=True)

@app.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/registrar_usuario', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        hash_pw = generate_password_hash(form.password.data)
        db.session.add(Usuario(username=form.username.data, password=hash_pw))
        db.session.commit()
        flash('Novo usuário cadastrado!', 'success')
        return redirect(url_for('listar_usuarios'))
    return render_template('registrar_usuario.html', form=form)

@app.route('/excluir_usuario/<int:id>', methods=['POST'])
@login_required
def excluir_usuario(id):
    if id == session.get('user_id'):
        flash('Não é possível excluir o próprio usuário!', 'danger')
        return redirect(url_for('listar_usuarios'))
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('listar_usuarios'))

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Processadores Úteis ---

@app.context_processor
def utility_processor():
    def format_currency(value): return f"R$ {value:,.2f}".replace('.', ',') if value else "R$ 0,00"
    def format_date(value): return value.strftime('%d/%m/%Y') if value else ""
    def format_boolean(value): return "SIM" if value else "NÃO"
    return dict(format_currency=format_currency, format_date=format_date, format_boolean=format_boolean)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# --- Execução com Waitress (Produção) ---

if __name__ == '__main__':
    Timer(2, open_browser).start()
    # serve() substitui o app.run() para suportar rede e múltiplos usuários
    serve(app, host='0.0.0.0', port=5000, threads=8)