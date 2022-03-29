from flask import Flask
from flask import render_template
from flask import request
import sqlite3
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import json
import plotly.graph_objects as go


def main(con):
    cursorObj = con.cursor()
    ####     Apartado 1    ####

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

    pd1.rename(columns={0: "nombre", 1: "email_totales", 2: "email_phishing", 3: "email_clicados"}, inplace=True)

    # Se añade una nueva columna que será el ratio de email clicados en función de los emails de phishing
    pd1['ratio'] = (pd1['email_clicados'] * 100) / pd1['email_phishing']

    # Se ordena el Dataframe en función de la columna ratio
    pd1 = pd1.sort_values('ratio', ascending=False)

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return '<p>Hello, World!</p>'

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name, graphJSON=None)

    @app.route('/login')
    def login():
        name = request.args.get('user')
        return render_template('hello.html', name=name, graphJSON=None)

    @app.route('/plotly', methods=['GET'])
    def plotly():

        filtro = request.form['numero']
        print(filtro)

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
        return render_template('hello.html', graphJSON=graphJSON)

    if __name__ == '__main__':
        app.run(debug=True)


con = sqlite3.connect('example.db')
main(con)
con.close()
