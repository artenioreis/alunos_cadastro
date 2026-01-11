from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, IntegerField, FloatField, TextAreaField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, EqualTo

class AlunoForm(FlaskForm):
    foto = FileField('Foto do Aluno', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas!')
    ], render_kw={"accept": "image/*", "class": "form-control"})

    documento = FileField('Anexar Documento (PDF ou Imagem)', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Apenas PDF e imagens são permitidos!')
    ], render_kw={"class": "form-control"})

    nome_completo = StringField('Nome Completo', validators=[
        DataRequired(message='Nome completo é obrigatório'),
        Length(min=3, max=100)
    ], render_kw={"class": "form-control"})

    cpf = StringField('CPF', validators=[Optional()], render_kw={"class": "form-control", "placeholder": "000.000.000-00"})
    rg_certidao = StringField('RG ou Certidão', validators=[Optional()], render_kw={"class": "form-control", "placeholder": "RG ou Número da Certidão"})
    telefone = StringField('Telefone', validators=[Optional()], render_kw={"class": "form-control", "placeholder": "(00) 00000-0000"})
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"type": "date", "class": "form-control"})
    data_cadastro = DateField('Data da Inscrição', validators=[Optional()], format='%Y-%m-%d', render_kw={"type": "date", "class": "form-control"})
    nome_pais = StringField('Nome dos Pais/Responsáveis', validators=[DataRequired()], render_kw={"class": "form-control"})
    curso = StringField('Curso', validators=[DataRequired()], render_kw={"class": "form-control"})
    setor = SelectField('Setor', choices=[('CULTURAL', 'Cultural'), ('PROFISSIONALIZANTE', 'Profissionalizante')], validators=[DataRequired()], render_kw={"class": "form-select"})
    endereco = StringField('Endereço', validators=[DataRequired()], render_kw={"class": "form-control"})
    escola = StringField('Escola', validators=[DataRequired()], render_kw={"class": "form-control"})
    trabalho_ficha_adulto = BooleanField('Trabalho (Ficha de Adulto)', render_kw={"class": "form-check-input"})
    nome_trabalho_profissao = StringField('Nome do Trabalho/Profissão', validators=[Optional()], render_kw={"class": "form-control"})
    bolsa_familia = BooleanField('Bolsa Família', render_kw={"class": "form-check-input"})
    irmaos = IntegerField('Irmãos', validators=[DataRequired(), NumberRange(min=0)], default=0, render_kw={"class": "form-control"})
    renda_familiar = FloatField('Renda Familiar', validators=[DataRequired()], render_kw={"class": "form-control"})
    pessoas_residencia = IntegerField('Pessoas na Residência', validators=[DataRequired()], render_kw={"class": "form-control"})
    desistencia = SelectField('Desistência', choices=[('NÃO', 'Não'), ('SIM', 'Sim')], validators=[DataRequired()], render_kw={"class": "form-select"})
    observacao = TextAreaField('Observação', validators=[Optional()], render_kw={"class": "form-control", "rows": 3})

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Senha', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Entrar', render_kw={"class": "btn w-100 py-2 text-white", "style": "background-color: #a689bd;"})

class RegistroUsuarioForm(FlaskForm):
    username = StringField('Novo Usuário', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"class": "form-control"})
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=4)], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem coincidir')], render_kw={"class": "form-control"})
    submit = SubmitField('Cadastrar Usuário', render_kw={"class": "btn btn-primary"})