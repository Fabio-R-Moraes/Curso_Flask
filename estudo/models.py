from estudo import db
from datetime import datetime

class Contatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    assunto = db.Column(db.String, nullable=True)
    Mensagem = db.Column(db.String, nullable=True)
    respondido = db.Column(db.Integer, default=0)