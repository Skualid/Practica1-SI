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

    cursorObj.execute(sql_user)
    cursorObj.execute(sql_fecha)
    cursorObj.execute(sql_ip)

    con.commit()

def sql_insert_json(con):
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

            #cursorObj.execute(sql, datos_user_i)
            con.commit()

            #print(len(data['usuarios'][usuario][nombre]['fechas']))

            for fechas in range(len(data['usuarios'][usuario][nombre]['fechas'])):
                for fecha in data['usuarios'][usuario][nombre]['fechas'][fechas]:
                    print(fecha, end=" ")




con = sqlite3.connect('example.db')

sql_create_table(con)
sql_insert_json(con)

con.close()
