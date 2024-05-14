class Config:
    SECRET_KEY = 'asdasd;jas;l.dkhna1092370'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://dexter:dexter@localhost:5432/novelserver'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = Config()