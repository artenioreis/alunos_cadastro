from datetime import datetime, date
from app import db

def calcular_idade(data_nascimento):
    """Calcula idade a partir da data de nascimento"""
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
        # Calcular idade automaticamente
        if self.data_nascimento:
            self.idade = calcular_idade(self.data_nascimento)

    def atualizar_idade(self):
        """Atualiza a idade do aluno"""
        if self.data_nascimento:
            self.idade = calcular_idade(self.data_nascimento)

    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'idade': self.idade,
            'curso': self.curso,
            'setor': self.setor,
            'escola': self.escola,
            'foto_url': f'/static/uploads/{self.foto}' if self.foto else None,
            'bolsa_familia': self.bolsa_familia,
            'renda_familiar': self.renda_familiar,
            'pessoas_residencia': self.pessoas_residencia
        }
