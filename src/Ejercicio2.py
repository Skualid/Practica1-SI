import sqlite3
import pandas as pd
import numpy as np
import json


def sql_create_table(con):
    cursorObj = con.cursor()

    # Esta forma de crear tablas además de ser poco robusta, es vulnerable a inyección SQL.
    '''cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS usuarios (nombre text, telefono int, contraseña text, provincia text, permisos int, email_total int, email_phishing int, email_clicados int, PRIMARY KEY(nombre))")
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS fecha (nombre text, fecha text, PRIMARY KEY(nombre, fecha) , FOREIGN KEY(nombre) REFERENCES usuarios(nombre))")
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS ip (nombre text, ip text, PRIMARY KEY(nombre, ip) , FOREIGN KEY(nombre) REFERENCES usuarios(nombre))")'''


    #Utilizamos SQL parametrizado
    sql_user = '''CREATE TABLE IF NOT EXISTS usuarios (nombre text, telefono int, contraseña text, provincia text, permisos int, email_total int, email_phishing int, email_clicados int, PRIMARY KEY(nombre))'''
    sql_fecha = '''CREATE TABLE IF NOT EXISTS fecha (nombre text, fecha text, PRIMARY KEY(nombre, fecha) , FOREIGN KEY(nombre) REFERENCES usuarios(nombre))'''
    sql_ip = '''CREATE TABLE IF NOT EXISTS ip (nombre text, ip text, PRIMARY KEY(nombre, ip) , FOREIGN KEY(nombre) REFERENCES usuarios(nombre))'''
    sql_legal = '''CREATE TABLE IF NOT EXISTS legal (url text, cookies int, aviso int, proteccion_de_datos int, creacion int, PRIMARY KEY(url))'''

    cursorObj.execute(sql_user)
    cursorObj.execute(sql_fecha)
    cursorObj.execute(sql_ip)
    cursorObj.execute(sql_legal)

    con.commit()

def sql_insert_json_user(con):
    cursorObj = con.cursor()

    with open('../Statement/Logs/users.json', 'r') as f:
        data = json.load(f)

    for usuario in range(len(data['usuarios'])):
        for nombre in data['usuarios'][usuario].keys():

            telefono = data['usuarios'][usuario][nombre]['telefono']
            if telefono == 'None':
                telefono = 0

            contraseña = data['usuarios'][usuario][nombre]['contrasena']
            provincia = data['usuarios'][usuario][nombre]['provincia']
            permisos = int(data['usuarios'][usuario][nombre]['permisos'])

            email_total = data['usuarios'][usuario][nombre]['emails']['total']
            email_phishing = data['usuarios'][usuario][nombre]['emails']['phishing']
            email_clicados = data['usuarios'][usuario][nombre]['emails']['cliclados']

            datos_user_i =  [nombre, telefono, contraseña, provincia, permisos, email_total, email_phishing, email_clicados]

            #Esta forma de hacer INSERT además de ser poco robusta, es vulnerable a inyección SQL.
            #cursorObj.execute(
            #    "INSERT INTO usuarios VALUES (nombre, telefono, contraseña, provincia, permisos, email_total, email_phishing, email_clicados) ")

            #Utilizamos SQL parametrizado
            sql = ''' INSERT INTO usuarios (nombre, telefono, contraseña, provincia, permisos, email_total, email_phishing, email_clicados) VALUES(?,?,?,?,?,?,?,?) '''

            cursorObj.execute(sql, datos_user_i)
            con.commit()


            for fecha in range(len(data['usuarios'][usuario][nombre]['fechas'])):
                sql = ''' INSERT INTO fecha (nombre, fecha) VALUES(?,?) '''

                fechas = data['usuarios'][usuario][nombre]['fechas'][fecha]

                datos_fecha_i = [nombre, fechas]
                cursorObj.execute(sql, datos_fecha_i)
                con.commit()

            for ip in range(len(data['usuarios'][usuario][nombre]['ips'])):
                sql = ''' INSERT INTO ip (nombre, ip) VALUES(?,?) '''

                ips = data['usuarios'][usuario][nombre]['ips'][ip]

                datos_ip_i = [nombre, ips]
                cursorObj.execute(sql, datos_ip_i)
                con.commit()


def sql_insert_json_legal(con):
    cursorObj = con.cursor()

    with open('../Statement/Logs/legal.json', 'r') as f:
        data = json.load(f)

    for legal in range(len(data['legal'])):
        for url in data['legal'][legal].keys():

            cookies = data['legal'][legal][url]['cookies']
            aviso = data['legal'][legal][url]['cookies']
            proteccion_de_datos = data['legal'][legal][url]['cookies']
            creacion = data['legal'][legal][url]['cookies']

            datos_legal_i =  [url, cookies, aviso, proteccion_de_datos, creacion]

            #Utilizamos SQL parametrizado
            sql = ''' INSERT INTO legal (url, cookies, aviso, proteccion_de_datos, creacion) VALUES(?,?,?,?,?) '''

            cursorObj.execute(sql, datos_legal_i)
            con.commit()

def apartado_1(con):
   cursorObj = con.cursor()
   cursorObj.execute('SELECT distinct * FROM usuarios')
   rows = cursorObj.fetchall()


   pd1 = pd.DataFrame(rows)
   print(pd1)
   print("El númeor de muestras es: ", pd1[1].count())


def apartado_2(con):
   cursorObj = con.cursor()
   cursorObj.execute('SELECT nombre,  COUNT(fecha)  FROM fecha GROUP BY nombre')
   rows = cursorObj.fetchall()


   pd1 = pd.DataFrame(rows)
   print(pd1)
   print("El valor de la media es: ", pd1[1].mean())
   print("El valor de la desviación estándar es: ", pd1[1].std())

def apartado_3(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT nombre,  COUNT(ip)  FROM ip GROUP BY nombre')
    rows = cursorObj.fetchall()

    pd1 = pd.DataFrame(rows)
    print(pd1)
    print("El valor de la media es: ", pd1[1].mean())
    print("El valor de la desviación estándar es: ", pd1[1].std())

def apartado_4(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT nombre, email_total  FROM usuarios')
    rows = cursorObj.fetchall()

    pd1 = pd.DataFrame(rows)
    print(pd1)
    print("El valor de la media es: ", pd1[1].mean())
    print("El valor de la desviación estándar es: ", pd1[1].std())

def apartado_5(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT nombre,  COUNT(fecha)  FROM fecha GROUP BY nombre')
    rows = cursorObj.fetchall()

    pd1 = pd.DataFrame(rows)
    print(pd1)
    print("El valor maximo es: ", pd1[1].max())
    print("El valor mínimo es: ", pd1[1].min())

def apartado_6(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT nombre, email_total  FROM usuarios')
    rows = cursorObj.fetchall()

    pd1 = pd.DataFrame(rows)
    print(pd1)
    print("El valor maximo es: ", pd1[1].max())
    print("El valor mínimo es: ", pd1[1].min())

con = sqlite3.connect('example.db')

#sql_create_table(con)
#sql_insert_json_user(con)
#sql_insert_json_legal(con)
apartado_1(con)
#apartado_2(con)
#apartado_3(con)
#apartado_4(con)
#apartado_5(con)
#apartado_6(con)
con.close()
