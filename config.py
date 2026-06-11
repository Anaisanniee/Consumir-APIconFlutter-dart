import os

class Config:
    DEBUG = True
    PORT = 5000
    
    # Esta es la línea clave que le falta a tu Flask:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/sistema_medico_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False