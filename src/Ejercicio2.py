import sqlite3
import pandas as pd
import numpy as np
import json

def sql_update(con):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE usuarios SET nombre = "Sergio" where dni = "X"')
    con.commit()

def sql_fetch(con):
   cursorObj = con.cursor()
   cursorObj.execute('SELECT * FROM usuarios')
   #SELECT dni, nombre FROM usuarios WHERE altura > 1.0
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)

def sql_delete(con):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE FROM usuarios where dni = "X"')
    con.commit()

def sql_delete_table(con):
    cursorObj = con.cursor()
    cursorObj.execute('drop table if exists usuarios')
    con.commit()

def sql_create_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS usuarios (nombre text, telefono int, contraseña text, provincia text, permisos int, email_total int, email_phishing int, email_clicados int, PRIMARY KEY(nombre))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS fecha (nombre text, fecha text, PRIMARY KEY(nombre, fecha) , FOREIGN KEY(nombre) REFERENCES usuarios(nombre))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS ip (nombre text, ip text, PRIMARY KEY(nombre, ip) , FOREIGN KEY(nombre) REFERENCES usuarios(nombre))")

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


            cursorObj.execute("INSERT INTO usuarios VALUES (nombre, telefono, contraseña, provincia, permisos, email_total, email_phishing, email_clicados) ")
            con.commit()

    con.commit()



con = sqlite3.connect('example.db')
sql_create_table(con)
#sql_fetch(con)
#sql_update(con)
#sql_fetch(con)
#sql_delete(con)
#sql_fetch(con)
#sql_delete_table(con)
con.close()

