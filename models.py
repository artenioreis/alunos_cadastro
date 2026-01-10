from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def calcular_idade(data_nascimento):
    if not data_nascimento:
        return 0
    hoje = date.today()
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(200), nullable=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nome_pais = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    escola = db.Column(db.String(100), nullable=False)
    trabalho_ficha_adulto = db.Column(db.Boolean, default=False)
    nome_trabalho_profissao = db.Column(db.String(100), nullable=True)
    bolsa_familia = db.Column(db.Boolean, default=False)
    irmaos = db.Column(db.Integer, default=0)
    renda_familiar = db.Column(db.Float, nullable=False)
    pessoas_residencia = db.Column(db.Integer, nullable=False)
    desistencia = db.Column(db.String(10), default='NÃO')
    observacao = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def atualizar_idade(self):
        if self.data_nascimento:
            self.idade = calcular_idade(self.data_nascimento)