from estudo import app
from flask import render_template, url_for

@app.route('/')
def homepage():
    usuario = 'Fabio'
    context = {
        'idade':40,
        'cidade':'Curitiba',
    }
    return render_template("index.html", usuario=usuario, context=context)

@app.route('/nova/')
def novapage():
    return "Esta é uma nova página!!!"