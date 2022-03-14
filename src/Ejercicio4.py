import sqlite3

import numpy as np
import pandas as pd
from natsort import index_natsorted
import matplotlib.pyplot as plt

def main(con):
    cursorObj = con.cursor()

    cursorObj.execute('SELECT contraseña FROM usuarios')
    user = cursorObj.fetchall()
    pd1 = pd.DataFrame(user)
    pd1.rename(columns={0:"contraseña"}, inplace=True)

    with open('password.txt', 'w') as f:
        f.write(pd1.to_string(index=False, header=False))

    pd1 = pd.DataFrame()
    with open('passwords_pwned.txt', 'r') as f:
        for password in f:
            password = password.strip('\n')
            cursorObj.execute('SELECT nombre, email_total, email_phishing, email_clicados FROM usuarios WHERE contraseña=?', [password])
            user = cursorObj.fetchall()
            pd1 = pd1.append(user, ignore_index=True)

    pd1.rename(columns={0: "nombre", 1:"email_totales", 2:"email_phishing", 3:"email_clicados"}, inplace=True)

    #Se añade una nueva columna que será el ratio de email clicados en función de los emails de phishing
    pd1['ratio'] = (pd1['email_clicados'] * 100) / pd1['email_phishing']

    #Se ordena el Dataframe en función de la columna ratio
    pd1 = pd1.sort_values('ratio', ascending=False)
    print(pd1)

    #Nos quedamos sólo con las 10 primeras filas del Dataframe que serán los 10 usuarios más críticos
    pd1 = pd1.head(10)
    print(pd1)




con = sqlite3.connect('example.db')
main(con)
con.close()