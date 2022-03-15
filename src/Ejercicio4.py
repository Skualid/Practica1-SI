import sqlite3
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main(con):
    cursorObj = con.cursor()
    ####     Apartado 1    ####

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

    #Nos quedamos sólo con las 10 primeras filas del Dataframe que serán los 10 usuarios más críticos
    pd1 = pd1.head(10)
    print("--------------- APARTADO 1 ----------------\n")
    print(pd1)
    print("-------------------------------------------\n")

    ####   Apartado 2    ####

    cursorObj.execute('SELECT url, cookies, aviso, proteccion_de_datos FROM legal')
    legal = cursorObj.fetchall()
    pd2 = pd.DataFrame(legal)
    pd2.rename(columns={0: "url", 1: "cookies", 2: "aviso", 3: "proteccion_de_datos"}, inplace=True)

    # Se añade una nueva columna que será el número total de políticas que cumple la web
    pd2['total_politicas'] = pd2['cookies']  + pd2['aviso'] + pd2['proteccion_de_datos']

    # Se ordena el Dataframe en función de la columna total_politicas
    pd2 = pd2.sort_values('total_politicas', ascending=True)

    # Nos quedamos sólo con las 5 primeras filas del Dataframe que serán las 5 webs con más políticas desactualizadas
    pd2 = pd2.head(5)
    print("--------------- APARTADO 2 ----------------\n")
    print(pd2)
    print("-------------------------------------------\n")

    ####     Apartado 3    #####
    #Obtenemos los usuarios con pass pwned
    pd3 = pd.DataFrame()
    with open('passwords_pwned.txt', 'r') as f:
        for password in f:
            password = password.strip('\n')
            cursorObj.execute('SELECT i.nombre, COUNT(i.ip) FROM usuarios u  CROSS JOIN ip i on u.nombre = i.nombre WHERE u.contraseña=? GROUP BY(i.nombre)', [password])
            user = cursorObj.fetchall()
            pd3 = pd3.append(user, ignore_index=True)

    pd3.rename(columns={0: "usuarios_vulnerables", 1:"conexiones_totales"}, inplace=True)
    print("--------------- APARTADO 3 ----------------\n")
    print("La media de conexiones de usuarios con contraseña vulnerable es:", pd3['conexiones_totales'].mean())

    #Sacamos todos los usuarios
    cursorObj.execute('SELECT i.nombre, COUNT(i.ip), u.contraseña FROM usuarios u  CROSS JOIN ip i on u.nombre = i.nombre GROUP BY(i.nombre)')
    all_user = cursorObj.fetchall()
    pd4 = pd.DataFrame(all_user)
    pd4.rename(columns={0: "usuarios_no_vulnerables", 1: "conexiones_totales", 2:"contraseña"}, inplace=True)

    #Eliminamos los usuarios con pass pwned
    with open('passwords_pwned.txt', 'r') as f:
        for password in f:
            password = password.strip('\n')
            pd4 = pd4.drop(pd4.index[pd4['contraseña'] == password], axis = 0)
    

    pd4 = pd4.drop(columns='contraseña')

    print("La media de conexiones de usuarios con contraseña no vulnerable es:", pd4['conexiones_totales'].mean())
    print("-------------------------------------------\n")

    ####    Apartado 4    ####
    cursorObj.execute('SELECT url, cookies, aviso, proteccion_de_datos, creacion FROM legal')
    legal = cursorObj.fetchall()
    pd5 = pd.DataFrame(legal)
    pd5.rename(columns={0: "url", 1: "cookies", 2: "aviso", 3: "proteccion_de_datos", 4:"creacion"}, inplace=True)

    # Se añade una nueva columna que será el número total de políticas que cumple la web
    pd5['total_politicas'] = pd5['cookies'] + pd5['aviso'] + pd5['proteccion_de_datos']

    #Eliminamos las columnas que ya no nos sirven
    pd5 = pd5.drop(columns={'cookies', 'aviso', 'proteccion_de_datos'})

    años = []
    for año in pd5['creacion']:
        if año not in años:
            años.append(año)

    años = sorted(años)

    print("--------------- APARTADO 4 ----------------\n")
    for año in años:
        print(pd5.groupby(['creacion']).get_group(año))
        print()
    print("-------------------------------------------\n")

    #### Actividad 5  ####
    print("--------------- APARTADO 5 ----------------\n")
    print("El número de usuarios con contraseñas comprometidas es:", pd3['usuarios_vulnerables'].count())
    print("El número de usuarios con contraseñas no comprometidas es:", pd4['usuarios_no_vulnerables'].count())
    print("-------------------------------------------\n")


con = sqlite3.connect('example.db')
main(con)
con.close()