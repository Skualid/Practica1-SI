import sqlite3
import pandas as pd

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


def years_web():
    con = sqlite3.connect('example.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT url, cookies, aviso, proteccion_de_datos, creacion FROM legal')
    legal = cursorObj.fetchall()
    pd5 = pd.DataFrame(legal)
    pd5.rename(columns={0: "url", 1: "cookies", 2: "aviso", 3: "proteccion_de_datos", 4: "creacion"}, inplace=True)

    # Se añade una nueva columna que será el número total de políticas que cumple la web

    import numpy as np
    pd5['3_politicas'] = np.where(pd5['cookies'] + pd5['aviso'] + pd5['proteccion_de_datos'] == 3, 1, np.nan)
    pd5['1_2_politicas'] = np.where(pd5['cookies'] + pd5['aviso'] + pd5['proteccion_de_datos'] == 3, np.nan, 1)

    # Eliminamos las columnas que ya no nos sirven
    pd5 = pd5.drop(columns={'cookies', 'aviso', 'proteccion_de_datos'})

    tres_pol = pd5.groupby(['creacion', '3_politicas']).size().reset_index(name='counts')
    uno_dos_pol = pd5.groupby(['creacion', '1_2_politicas']).size().reset_index(name='counts')

    politicas = pd.merge(tres_pol, uno_dos_pol, on='creacion', how='outer')
    politicas = politicas.sort_values(by=['creacion'])

    return politicas