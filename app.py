import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, IntegerField, FloatField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from werkzeug.utils import secure_filename
from PIL import Image

# ========== CONFIGURAÇÃO ==========
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Inicializar banco de dados
db = SQLAlchemy(app)

# Criar pasta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ========== MODELO ==========
def calcular_idade(data_nascimento):
    hoje = date.today()
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(200), nullable=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nome_pais = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(20), nullable=False)  # CULTURAL ou PROFISSIONALIZANTE
    endereco = db.Column(db.String(200), nullable=False)
    escola = db.Column(db.String(100), nullable=False)
    trabalho_ficha_adulto = db.Column(db.Boolean, default=False)
    nome_trabalho_profissao = db.Column(db.String(100), nullable=True)
    bolsa_familia = db.Column(db.Boolean, default=False)
    irmaos = db.Column(db.Integer, default=0)
    renda_familiar = db.Column(db.Float, nullable=False)
    pessoas_residencia = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.data_nascimento:
            self.idade = calcular_idade(self.data_nascimento)

    def atualizar_idade(self):
        if self.data_nascimento:
            self.idade = calcular_idade(self.data_nascimento)

# ========== FORMULÁRIO ==========
class AlunoForm(FlaskForm):
    foto = FileField('Foto do Aluno', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas!')
    ], render_kw={"accept": "image/*"})

    nome_completo = StringField('Nome Completo', validators=[
        DataRequired(message='Nome completo é obrigatório'),
        Length(min=3, max=100)
    ], render_kw={"placeholder": "Digite o nome completo"})

    data_nascimento = DateField('Data de Nascimento', validators=[
        DataRequired(message='Data de nascimento é obrigatória')
    ], format='%Y-%m-%d', render_kw={"type": "date"})

    nome_pais = StringField('Nome dos Pais', validators=[
        DataRequired(message='Nome dos pais é obrigatório'),
        Length(min=3, max=100)
    ], render_kw={"placeholder": "Nome dos pais ou responsáveis"})

    curso = StringField('Curso', validators=[
        DataRequired(message='Curso é obrigatório'),
        Length(min=2, max=100)
    ], render_kw={"placeholder": "Curso do aluno"})

    setor = SelectField('Setor', choices=[
        ('CULTURAL', 'Cultural'),
        ('PROFISSIONALIZANTE', 'Profissionalizante')
    ], validators=[DataRequired(message='Setor é obrigatório')])

    endereco = StringField('Endereço', validators=[
        DataRequired(message='Endereço é obrigatório'),
        Length(min=5, max=200)
    ], render_kw={"placeholder": "Endereço completo"})

    escola = StringField('Escola', validators=[
        DataRequired(message='Escola é obrigatória'),
        Length(min=2, max=100)
    ], render_kw={"placeholder": "Nome da escola"})

    trabalho_ficha_adulto = BooleanField('Trabalho (Ficha de Adulto)')

    nome_trabalho_profissao = StringField('Nome do Trabalho/Profissão', validators=[
        Optional(),
        Length(max=100)
    ], render_kw={"placeholder": "Profissão ou local de trabalho"})

    bolsa_familia = BooleanField('Bolsa Família')

    irmaos = IntegerField('Irmãos', validators=[
        DataRequired(message='Número de irmãos é obrigatório'),
        NumberRange(min=0, max=50)
    ], default=0, render_kw={"placeholder": "Número de irmãos"})

    renda_familiar = FloatField('Renda Familiar (R$)', validators=[
        DataRequired(message='Renda familiar é obrigatória'),
        NumberRange(min=0, max=1000000)
    ], render_kw={"placeholder": "Renda familiar", "step": "0.01"})

    pessoas_residencia = IntegerField('Pessoas na Residência', validators=[
        DataRequired(message='Número de pessoas é obrigatório'),
        NumberRange(min=1, max=50)
    ], render_kw={"placeholder": "Quantas pessoas moram na casa"})

    observacao = TextAreaField('Observação', validators=[
        Optional(),
        Length(max=500)
    ], render_kw={"placeholder": "Observações importantes", "rows": 4})

# ========== FUNÇÕES AUXILIARES ==========
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def salvar_foto(foto_file):
    if foto_file and allowed_file(foto_file.filename):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(foto_file.filename)
        nome_arquivo = f"{timestamp}_{filename}"
        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)

        foto_file.save(caminho_completo)

        try:
            img = Image.open(caminho_completo)
            if img.size[0] > 800 or img.size[1] > 800:
                img.thumbnail((800, 800))
                img.save(caminho_completo)
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")

        return nome_arquivo
    return None

# ========== ROTAS ==========
@app.route('/')
def index():
    alunos = Aluno.query.order_by(Aluno.nome_completo).all()
    total_alunos = len(alunos)

    cultural = Aluno.query.filter_by(setor='CULTURAL').count()
    profissionalizante = Aluno.query.filter_by(setor='PROFISSIONALIZANTE').count()
    bolsa_familia = Aluno.query.filter_by(bolsa_familia=True).count()

    return render_template('index.html', 
                         alunos=alunos, 
                         total_alunos=total_alunos,
                         cultural=cultural,
                         profissionalizante=profissionalizante,
                         bolsa_familia=bolsa_familia)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = AlunoForm()

    if form.validate_on_submit():
        try:
            foto_nome = salvar_foto(form.foto.data) if form.foto.data else None

            novo_aluno = Aluno(
                foto=foto_nome,
                nome_completo=form.nome_completo.data,
                data_nascimento=form.data_nascimento.data,
                nome_pais=form.nome_pais.data,
                curso=form.curso.data,
                setor=form.setor.data,
                endereco=form.endereco.data,
                escola=form.escola.data,
                trabalho_ficha_adulto=form.trabalho_ficha_adulto.data,
                nome_trabalho_profissao=form.nome_trabalho_profissao.data if form.trabalho_ficha_adulto.data else None,
                bolsa_familia=form.bolsa_familia.data,
                irmaos=form.irmaos.data,
                renda_familiar=form.renda_familiar.data,
                pessoas_residencia=form.pessoas_residencia.data,
                observacao=form.observacao.data
            )

            db.session.add(novo_aluno)
            db.session.commit()

            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar aluno: {str(e)}', 'danger')

    return render_template('cadastrar.html', form=form)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    aluno = Aluno.query.get_or_404(id)
    form = AlunoForm(obj=aluno)

    if request.method == 'GET':
        form.data_nascimento.data = aluno.data_nascimento
        form.trabalho_ficha_adulto.data = aluno.trabalho_ficha_adulto
        form.bolsa_familia.data = aluno.bolsa_familia
        form.nome_trabalho_profissao.data = aluno.nome_trabalho_profissao

    if form.validate_on_submit():
        try:
            if form.foto.data:
                if aluno.foto:
                    foto_antiga = os.path.join(app.config['UPLOAD_FOLDER'], aluno.foto)
                    if os.path.exists(foto_antiga):
                        os.remove(foto_antiga)
                aluno.foto = salvar_foto(form.foto.data)

            aluno.nome_completo = form.nome_completo.data
            aluno.data_nascimento = form.data_nascimento.data
            aluno.nome_pais = form.nome_pais.data
            aluno.curso = form.curso.data
            aluno.setor = form.setor.data
            aluno.endereco = form.endereco.data
            aluno.escola = form.escola.data
            aluno.trabalho_ficha_adulto = form.trabalho_ficha_adulto.data
            aluno.nome_trabalho_profissao = form.nome_trabalho_profissao.data if form.trabalho_ficha_adulto.data else None
            aluno.bolsa_familia = form.bolsa_familia.data
            aluno.irmaos = form.irmaos.data
            aluno.renda_familiar = form.renda_familiar.data
            aluno.pessoas_residencia = form.pessoas_residencia.data
            aluno.observacao = form.observacao.data
            aluno.atualizar_idade()

            db.session.commit()
            flash('Aluno atualizado com sucesso!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar aluno: {str(e)}', 'danger')

    return render_template('editar.html', form=form, aluno=aluno)

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    aluno = Aluno.query.get_or_404(id)

    try:
        if aluno.foto:
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], aluno.foto)
            if os.path.exists(foto_path):
                os.remove(foto_path)

        db.session.delete(aluno)
        db.session.commit()
        flash('Aluno excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir aluno: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/visualizar/<int:id>')
def visualizar(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('visualizar.html', aluno=aluno)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def utility_processor():
    def format_currency(value):
        return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    def format_date(value):
        if value:
            return value.strftime('%d/%m/%Y')
        return ''

    return dict(format_currency=format_currency, format_date=format_date)

# Criar banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
