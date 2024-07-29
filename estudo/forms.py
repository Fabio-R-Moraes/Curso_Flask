from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from estudo.models import Contatos
from estudo import db

class  ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        contato = Contatos(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            Mensagem = self.mensagem.data
        )

        db.session.add(contato)
        db.session.commit()