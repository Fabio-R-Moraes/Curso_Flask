from estudo import app, db
from flask import render_template, url_for, request, redirect
from estudo.models import Contatos, Post
from estudo.forms import ContatoForm, UserForm,LoginForm, PostForm, PostComentariosForm
from flask_login import login_user, logout_user, current_user, login_required
from collectionpy.chart.apexcharts import Chart, CND_SRC

@app.route('/', methods=['GET', 'POST'])
def homepage():
    usuario = 'Fabio'
    context = {
        'idade':40,
        'cidade':'Curitiba',
    }
    form = LoginForm()
    
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))

    return render_template("index.html", usuario=usuario, context=context, form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()

    if form.validate_on_submit():
        user = form.save()

        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    
    return render_template("cadastro.html", form=form)

@app.route('/sair')
@login_required
def logout():
    logout_user()

    return redirect(url_for('homepage'))

@app.route('/post/novo/', methods=['GET', 'POST'])
@login_required
def postNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        
        return redirect(url_for('homepage'))

    return render_template("postNovo.html", form=form)

@app.route('/post/lista')
@login_required
def postLista():
    posts = Post.query.all()
    print(current_user.posts)
    return render_template("postLista.html", posts=posts)

@app.route('/post/<int:id>/', methods=['GET','POST'])
@login_required
def postDetail(id):
    post = Post.query.get(id)
    form = PostComentariosForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        
        return redirect(url_for('postDetail', id=id))

    return render_template("post.html", post=post, form=form)

#Formato INSEGURO, pode ser utilizado mas NÃO é recomendado
@app.route('/contato_old/', methods=['GET','POST'])
@login_required
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
@login_required
def contato():
    form = ContatoForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template("contatos.html", form=form)

@app.route('/contato/lista/')
@login_required
def contatoLista():
    if(current_user.id == 1): return redirect(url_for('homepage'))

    if request.method == 'GET':
        palavra = request.args.get('pesquisa','')

    dados = Contatos.query.order_by('nome')

    if palavra != '':
        dados = dados.filter_by(nome=palavra)

    context = {'dados': dados}
    return render_template("contato_lista.html", context=context)

@app.route('/contato/<int:id>/')
@login_required
def contato_detail(id):
    obj = Contatos.query.get(id)
    return render_template("contato_detail.html", obj=obj)

@app.route('/grafico/')
def exemplo_grafico():
    x = ['A', 'B', 'C']
    y = [
        [10, 20, 30, 40, 50],
        [14, 50, 74, 5, 63]
    ]

    y_label = ['Orçado', 'Realizado']

    chart = Chart(x, y, y_label)
    chart.width = 600
    chart.foreColor = '191970'
    chart.background= '00FF00'
    chart.palette = 1
    chart.plot_type = 'line'

    return render_template("exemplo_grafico.html", chart=chart, cnd=CND_SRC)