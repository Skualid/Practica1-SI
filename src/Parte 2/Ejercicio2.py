from flask import Flask
from flask import render_template
from flask import request
import sqlite3
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import json
import plotly.graph_objects as go
from urllib.request import urlopen


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
    pd1['ratio'] = pd1['ratio'].fillna(0)
    # Se ordena el Dataframe en función de la columna ratio
    pd1 = pd1.sort_values('ratio', ascending=False)

    return pd1


def websVuln():
    con = sqlite3.connect('example.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT url, cookies, aviso, proteccion_de_datos FROM legal')
    legal = cursorObj.fetchall()
    con.close()

    pd2 = pd.DataFrame(legal)
    pd2.rename(columns={0: "url", 1: "cookies", 2: "aviso", 3: "proteccion_de_datos"}, inplace=True)

    # Se añade una nueva columna que será el número total de políticas que cumple la web
    pd2['total_politicas'] = pd2['cookies'] + pd2['aviso'] + pd2['proteccion_de_datos']

    # Se ordena el Dataframe en función de la columna total_politicas
    pd2 = pd2.sort_values('total_politicas', ascending=True)

    return pd2


def mean_conex():
    con = sqlite3.connect('example.db')
    cursorObj = con.cursor()

    # Sacamos todos los usuarios
    cursorObj.execute(
        'SELECT i.nombre, COUNT(i.ip), u.contraseña FROM usuarios u  CROSS JOIN ip i on u.nombre = i.nombre GROUP BY(i.nombre)')
    all_user = cursorObj.fetchall()
    pd4 = pd.DataFrame(all_user)
    pd4.rename(columns={0: "usuarios", 1: "conexiones_totales", 2: "contraseña"}, inplace=True)

    listaVuln = []

    # Eliminamos los usuarios con pass pwned
    for user in range(len(pd4)):
        bool = False
        with open('passwords_pwned.txt', 'r') as f:
            for password in f:
                password = password.strip('\n')
                if pd4.iloc[user, 2] == password:
                    bool = True

        if bool:
            listaVuln.append("si")
        else:
            listaVuln.append("no")

    pd4['esVulnerable'] = listaVuln

    return pd4


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


@app.route('/ajax.html')
def ajax():
    import requests

    x = requests.get('https://cve.circl.lu/api/last')
    cves = x.json()

    matrix = []
    for i in range(10):
        matrix.append([cves[i]["last-modified"], cves[i]["id"], cves[i]["summary"]])
        print(matrix[i])

    return render_template('ajax.html', prueba=matrix)


@app.route('/pass', methods=['POST'])
def get_pass():
    password = request.form['password']
    return pwned(password)


@app.route('/pwned.html')
def pwned(password=None):
    import hashlib
    import requests
    import re
    if password is not None:
        password = password.encode("utf-8")
        hash = hashlib.sha1(password)
        prefix_hash = hash.hexdigest()[:5]

        request_get = requests.get('https://api.pwnedpasswords.com/range/' + prefix_hash)
        request_get = request_get.text

        sufix_hash = hash.hexdigest()[5:].upper()

        cadena = sufix_hash + ":([0-9]+)\\b"
        results = re.findall(cadena, request_get)

        resultado = 0
        if results:
            resultado = results[0]

        return render_template('pwned.html', resultado=resultado)
    else:
        return render_template('pwned.html', resultado=-1)


@app.route('/signup.html')
def register():
    name = request.args.get('user')
    return render_template('signup.html', name=name, graphJSON=None)


@app.route('/param', methods=['POST'])
def param():
    filtro = request.form['numero']
    return plotly(filtro)


@app.route('/filtrar', methods=['POST'])
def filtrar():
    filtro = request.form['filtrar']

    if filtro == 'mas' or filtro == 'menos':
        return plotly(filtro)
    elif filtro == 'reset':
        return plotlyNoArgs()
    else:
        return render_template('error.html')


@app.route('/plotly.html/<filtro>')
def plotly(filtro):
    pd1 = usersVuln()

    if filtro == 'mas' or filtro == 'menos':
        if filtro == 'mas':
            pd1 = pd1.drop(pd1.index[pd1['ratio'] < 50], axis=0)
        else:
            pd1 = pd1.drop(pd1.index[pd1['ratio'] >= 50], axis=0)
    else:
        if filtro <= '0' or len(filtro) == 0:
            return render_template('error.html')
        pd1 = pd1.head(int(filtro))

    return plotlyNoArgs(pd1)


@app.route('/plotly.html')
def plotlyNoArgs(pd2=None):
    if pd2 is not None:
        pd1 = pd2
    else:
        pd1 = usersVuln()

    from plotly.subplots import make_subplots

    ejex = pd1["nombre"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['email_totales'],
        name='Emails totales',
        marker_color='royalblue'
    ))
    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['email_phishing'],
        name='Emails phishing',
        marker_color='darkorange'
    ))

    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['email_clicados'],
        name='Emails clicados',
        marker_color='lightgray'
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=ejex,
        y=pd1["ratio"],
        name='Porcentaje clics Phising',
        marker_color='gold'
    ), secondary_y=True, )

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45, legend=dict(bgcolor='rgba(0,75,154,0.4)'),
                      paper_bgcolor="rgb(0,0,0,0)", margin=dict(l=40, r=40, b=40, t=40), legend_font_color="white")

    # fig.update_layout(paper_bgcolor="rgb(0,0,0,0)")
    fig.update_xaxes(color='white', automargin=True)
    fig.update_yaxes(color='white', automargin=True)

    fig.update_layout({
        'plot_bgcolor': 'rgba(30,25,30,0.4)',
    })

    import plotly

    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('plotly.html', graphJSON=graphJSON)


@app.route('/parametro', methods=['POST'])
def parametro():
    filtro = request.form['numero']
    return plotly_web(filtro)


@app.route('/plotly_webs.html/<filtro>')
def plotly_web(filtro):
    pd1 = websVuln()
    if filtro <= '0' or len(filtro) == 0:
        return render_template('error.html')

    pd1 = pd1.head(int(filtro))
    return plotly_webNoArgs(pd1)


@app.route('/plotly_webs.html')
def plotly_webNoArgs(pd2=None):
    if pd2 is not None:
        pd1 = pd2
    else:
        pd1 = websVuln()

    from plotly.subplots import make_subplots

    ejex = pd1["url"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['cookies'].replace(to_replace=[0, 1], value=[1, 0]),
        name='cookies',
        text=pd1['cookies'].replace(to_replace=[0, 1], value=[1, 0]),
        textposition='auto',
        marker_color='royalblue'
    ))
    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['aviso'].replace(to_replace=[0, 1], value=[1, 0]),
        name='Aviso',
        text=pd1['aviso'].replace(to_replace=[0, 1], value=[1, 0]),
        textposition='auto',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['proteccion_de_datos'].replace(to_replace=[0, 1], value=[1, 0]),
        name='Protección de datos',
        text=pd1['proteccion_de_datos'].replace(to_replace=[0, 1], value=[1, 0]),
        textposition='auto',
        marker_color='lightgray'
    ), secondary_y=False)

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45, legend=dict(bgcolor='rgba(0,75,154,0.4)'),
                      paper_bgcolor="rgb(0,0,0,0)", margin=dict(l=40, r=40, b=40, t=40), legend_font_color="white")

    # fig.update_layout(paper_bgcolor="rgb(0,0,0,0)")
    fig.update_xaxes(color='white', automargin=True)
    fig.update_yaxes(color='white', automargin=True, showticklabels=False)

    fig.update_layout({
        'plot_bgcolor': 'rgba(30,25,30,0.4)',
    })

    import plotly

    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('plotly_webs.html', graphJSON=graphJSON)

@app.route('/userVuln', methods=['POST'])
def userVuln():
    filtro = request.form['user']

    if filtro == 'si' or filtro == 'no':
        pd1 = mean_conex()
        if filtro == 'si':
            pd1 = pd1.drop(pd1.index[pd1['esVulnerable'] == 'no'], axis=0)
        else:
            pd1 = pd1.drop(pd1.index[pd1['esVulnerable'] == 'si'], axis=0)

        return plotly_conex(pd1)
    elif filtro == 'reset':
        return plotly_conex()

    else:
        return render_template('error.html')

@app.route('/plotly_conex.html')
def plotly_conex(pd4=None):
    if pd4 is not None:
        pd1 = pd4
    else:
        pd1 = mean_conex()

    from plotly.subplots import make_subplots

    ejex = pd1["usuarios"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=ejex,
        y=pd1['conexiones_totales'],
        name='Conexiones',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Scatter(
        x=ejex,
        y=pd1["conexiones_totales"],
        name='Conexiones totales',
        marker_color='gold'
    ), secondary_y=True, )


    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45, legend=dict(bgcolor='rgba(0,75,154,0.4)'),
                      paper_bgcolor="rgb(0,0,0,0)", margin=dict(l=40, r=40, b=40, t=40), legend_font_color="white")

    # fig.update_layout(paper_bgcolor="rgb(0,0,0,0)")
    fig.update_xaxes(color='white', automargin=True)
    fig.update_yaxes(color='white', automargin=True)

    fig.update_layout({
        'plot_bgcolor': 'rgba(30,25,30,0.4)',
    })

    import plotly

    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('plotly_conex.html', graphJSON=graphJSON)





if __name__ == '__main__':
    app.run(debug=True)
