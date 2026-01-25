from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, IntegerField, FloatField, TextAreaField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, EqualTo, InputRequired

class AlunoForm(FlaskForm):
    foto = FileField('Foto do Aluno', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens!')], render_kw={"class": "form-control"})
    documento = FileField('Anexar Documento', validators=[FileAllowed(['pdf', 'jpg', 'png'], 'PDF ou Imagem!')], render_kw={"class": "form-control"})
    nome_completo = StringField('Nome Completo', validators=[DataRequired(message="O nome é obrigatório")], render_kw={"class": "form-control"})
    cpf = StringField('CPF', validators=[Optional()], render_kw={"class": "form-control"})
    rg_certidao = StringField('RG ou Certidão', validators=[Optional()], render_kw={"class": "form-control"})
    telefone = StringField('Telefone', validators=[Optional()], render_kw={"class": "form-control"})
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"type": "date", "class": "form-control"})
    data_cadastro = DateField('Data da Inscrição', validators=[Optional()], format='%Y-%m-%d', render_kw={"type": "date", "class": "form-control"})
    nome_pais = StringField('Nome dos Pais/Responsáveis', validators=[DataRequired()], render_kw={"class": "form-control"})
    curso = StringField('Curso', validators=[DataRequired()], render_kw={"class": "form-control"})
    setor = SelectField('Setor', choices=[('CULTURAL', 'Cultural'), ('PROFISSIONALIZANTE', 'Profissionalizante')], render_kw={"class": "form-select"})
    endereco = StringField('Endereço', validators=[DataRequired()], render_kw={"class": "form-control"})
    escola = StringField('Escola', validators=[DataRequired()], render_kw={"class": "form-control"})
    trabalho_ficha_adulto = BooleanField('Trabalho (Adulto)', render_kw={"class": "form-check-input"})
    nome_trabalho_profissao = StringField('Profissão', render_kw={"class": "form-control"})
    bolsa_familia = BooleanField('Bolsa Família', render_kw={"class": "form-check-input"})
    irmaos = IntegerField('Irmãos', validators=[InputRequired()], default=0, render_kw={"class": "form-control"})
    renda_familiar = FloatField('Renda Familiar', validators=[InputRequired()], render_kw={"class": "form-control"})
    pessoas_residencia = IntegerField('Pessoas na Residência', validators=[InputRequired()], render_kw={"class": "form-control"})
    desistencia = SelectField('Desistência', choices=[('NÃO', 'Não'), ('SIM', 'Sim')], render_kw={"class": "form-select"})
    observacao = TextAreaField('Observação', render_kw={"class": "form-control", "rows": 3})

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Senha', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Entrar')

class RegistroUsuarioForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"class": "form-control"})
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=4)], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='Senhas não coincidem')], render_kw={"class": "form-control"})
    submit = SubmitField('Cadastrar')