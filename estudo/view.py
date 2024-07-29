from estudo import app, db
from flask import render_template, url_for, request, redirect
from estudo.models import Contatos
from estudo.forms import ContatoForm

@app.route('/')
def homepage():
    usuario = 'Fabio'
    context = {
        'idade':40,
        'cidade':'Curitiba',
    }
    return render_template("index.html", usuario=usuario, context=context)


#Formato INSEGURO, pode ser utilizado mas NÃO é recomendado
@app.route('/contato_old/', methods=['GET','POST'])
def contato_old():
    context = {}
    if request.method == 'GET':
        palavra = request.args.get('pesquisa')
        print(f'Método GET: O termo procurado foi "{palavra}"')
        context.update({'palavra': palavra})

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        contato = Contatos(
            nome=nome,
            email=email,
            assunto=assunto,
            Mensagem=mensagem
        )

        db.session.add(contato)
        db.session.commit()

    return render_template("contatos_old.html", context=context)

@app.route('/contato/', methods=['GET','POST'])
def contato():
    form = ContatoForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template("contatos.html", form=form)