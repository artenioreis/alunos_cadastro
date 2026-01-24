import os

class Config:
    SECRET_KEY = 'sua-chave-secreta-aqui-123456789'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Suporte para múltiplos notebooks na rede (timeout de 30s)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"timeout": 30}
    }
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    # Limite definido para 64MB
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)