from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from estudo.models import Contatos, User, Post, PostComentarios
from estudo import db, bcrypt, app
import os
from werkzeug.utils import secure_filename


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validade_email(self, email):
        if User.query.filter(email=email.data).first():
            return ValidationError("Usuário já cadastrado com esse e-mail...")
        
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )

        db.session.add(user)
        db.session.commit()
        return user
    
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        #Recuperar o usuário do e-mail
        user = User.query.filter_by(email=self.email.data).first()

        #Verificar se a senha está correta
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception("Senha incorreta!!!!")
        else:
            raise Exception("Usuário não encontrado!!!!")


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

class PostForm(FlaskForm):
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    img_post = FileField('Imagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        img_post = self.img_post.data
        nome_seguro = secure_filename(img_post.filename)
        post = Post(
            mensagem = self.mensagem.data,
            user_id = user_id,
            img_post = nome_seguro
        )

        caminho = os.path.join(
            #Pasta do projeto
            os.path.abspath(os.path.dirname(__file__)),
            #Definir a pasta configurada
            app.config['UPLOAD_FILES'],
            #Pasta onde estão os posts
            'post',
            nome_seguro
        )

        img_post.save(caminho)
        db.session.add(post)
        db.session.commit()

class PostComentariosForm(FlaskForm):
    comentario = TextAreaField('Comentário', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id, post_id):
        comentarios = PostComentarios(
            comentario = self.comentario.data,
            user_id = user_id,
            post_id = post_id
        )

        db.session.add(comentarios)
        db.session.commit()