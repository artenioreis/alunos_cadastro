from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, IntegerField, FloatField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date

class AlunoForm(FlaskForm):
    foto = FileField('Foto do Aluno', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas!')
    ], render_kw={"accept": "image/*", "class": "form-control"})

    nome_completo = StringField('Nome Completo', validators=[
        DataRequired(message='Nome completo é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ], render_kw={"placeholder": "Digite o nome completo do aluno", "class": "form-control"})

    data_nascimento = DateField('Data de Nascimento', validators=[
        DataRequired(message='Data de nascimento é obrigatória')
    ], format='%Y-%m-%d', render_kw={"type": "date", "class": "form-control"})

    nome_pais = StringField('Nome dos Pais/Responsáveis', validators=[
        DataRequired(message='Nome dos pais é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ], render_kw={"placeholder": "Digite o nome dos pais ou responsáveis", "class": "form-control"})

    curso = StringField('Curso', validators=[
        DataRequired(message='Curso é obrigatório'),
        Length(min=2, max=100, message='Curso deve ter entre 2 e 100 caracteres')
    ], render_kw={"placeholder": "Digite o curso do aluno", "class": "form-control"})

    setor = SelectField('Setor', choices=[
        ('CULTURAL', 'Cultural'),
        ('PROFISSIONALIZANTE', 'Profissionalizante')
    ], validators=[DataRequired(message='Setor é obrigatório')], render_kw={"class": "form-select"})

    endereco = StringField('Endereço', validators=[
        DataRequired(message='Endereço é obrigatório'),
        Length(min=5, max=200, message='Endereço deve ter entre 5 e 200 caracteres')
    ], render_kw={"placeholder": "Digite o endereço completo", "class": "form-control"})

    escola = StringField('Escola', validators=[
        DataRequired(message='Escola é obrigatória'),
        Length(min=2, max=100, message='Escola deve ter entre 2 e 100 caracteres')
    ], render_kw={"placeholder": "Digite o nome da escola", "class": "form-control"})

    trabalho_ficha_adulto = BooleanField('Trabalho (Ficha de Adulto)', render_kw={"class": "form-check-input"})

    nome_trabalho_profissao = StringField('Nome do Trabalho/Profissão', validators=[
        Optional(),
        Length(max=100, message='Profissão deve ter até 100 caracteres')
    ], render_kw={"placeholder": "Digite a profissão ou local de trabalho", "class": "form-control"})

    bolsa_familia = BooleanField('Bolsa Família', render_kw={"class": "form-check-input"})

    irmaos = IntegerField('Irmãos', validators=[
        DataRequired(message='Número de irmãos é obrigatório'),
        NumberRange(min=0, max=50, message='Número de irmãos deve ser entre 0 e 50')
    ], default=0, render_kw={"placeholder": "Número de irmãos", "class": "form-control"})

    renda_familiar = FloatField('Renda Familiar (R$)', validators=[
        DataRequired(message='Renda familiar é obrigatória'),
        NumberRange(min=0, max=1000000, message='Renda deve ser entre 0 e 1.000.000')
    ], render_kw={"placeholder": "Digite a renda familiar", "step": "0.01", "class": "form-control"})

    pessoas_residencia = IntegerField('Pessoas na Residência', validators=[
        DataRequired(message='Número de pessoas é obrigatório'),
        NumberRange(min=1, max=50, message='Número de pessoas deve ser entre 1 e 50')
    ], render_kw={"placeholder": "Quantas pessoas moram na casa", "class": "form-control"})

    observacao = TextAreaField('Observação', validators=[
        Optional(),
        Length(max=500, message='Observação deve ter até 500 caracteres')
    ], render_kw={"placeholder": "Digite observações importantes", "rows": 4, "class": "form-control"})
