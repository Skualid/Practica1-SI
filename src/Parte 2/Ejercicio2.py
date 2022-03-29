from flask import Flask
from flask import render_template
from flask import request
import sqlite3
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import json
import plotly.graph_objects as go

def usersVuln():
    con = sqlite3.connect('example.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT contraseña FROM usuarios')
    user = cursorObj.fetchall()
    pd1 = pd.DataFrame(user)
    pd1.rename(columns={0: "contraseña"}, inplace=True)

    with open('password.txt', 'w') as f:
        f.write(pd1.to_string(index=False, header=False))

    pd1 = pd.DataFrame()
    with open('passwords_pwned.txt', 'r') as f:
        for password in f:
            password = password.strip('\n')
            cursorObj.execute(
                'SELECT nombre, email_total, email_phishing, email_clicados FROM usuarios WHERE contraseña=?',
                [password])
            user = cursorObj.fetchall()
            pd1 = pd1.append(user, ignore_index=True)

    con.close()

    pd1.rename(columns={0: "nombre", 1: "email_totales", 2: "email_phishing", 3: "email_clicados"}, inplace=True)

    # Se añade una nueva columna que será el ratio de email clicados en función de los emails de phishing
    pd1['ratio'] = (pd1['email_clicados'] * 100) / pd1['email_phishing']

    # Se ordena el Dataframe en función de la columna ratio
    pd1 = pd1.sort_values('ratio', ascending=False)

    return pd1


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/signin.html')
def login():
    name = request.args.get('user')
    return render_template('signin.html', name=name, graphJSON=None)

@app.route('/signup.html')
def register():
    name = request.args.get('user')
    return render_template('signup.html', name=name, graphJSON=None)

@app.route('/param', methods=['POST'])
def param():
    filtro = request.form['numero']
    return plotly(filtro)

@app.route('/plotly.html/<filtro>')
def plotly(filtro):

    pd1 = usersVuln()
    pd1 = pd1.head(int(filtro))
    if int(filtro) <= 0:
        return render_template('error.html')
    else:
        return plotlyNoArgs(pd1)

@app.route('/plotly.html')
def plotlyNoArgs(pd2=None):
    if pd2 is not None:
        pd1 = pd2
    else:
        pd1 = usersVuln()

    x = pd1["nombre"]

    ejex = pd1["nombre"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['email_totales'],
        name='Emails totales',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['email_phishing'],
        name='Emails phishing',
        marker_color='lightsalmon'
    ))

    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['email_clicados'],
        name='Emails clicados',
        marker_color='blue'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    import plotly

    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('plotly.html', graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)