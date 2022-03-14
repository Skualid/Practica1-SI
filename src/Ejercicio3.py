import sqlite3
import pandas as pd

def apartado_1(pd):
   print("tienen un total de muestras de: ", pd["email_phishing"].sum())

def apartado_2(pd):
   # Contar valores missing
   contador = 0
   for fila in pd["email_phishing"]:
      if str(fila) == 'None' or str(fila) == '-1' or str(fila) == '':
         contador += 1

   print("En la columna email_phishing hay", contador, "missing")

def apartado_3(pd):
   print("tienen un valor de mediana de: ", pd["email_phishing"].median())

def apartado_4(pd):
   print("tienen un valor de media de: ", pd["email_phishing"].mean())

def apartado_5(pd):
   print("tienen un valor de varianza de: ", pd["email_phishing"].var())

def apartado_6(pd):
   print("tienen un valor mínimo de: ", pd["email_phishing"].min(), " y máximo de: ", pd["email_phishing"].max())

def resultados(pd, user, cantidad):
   print("-------------------------------------------\n" + user, "con", cantidad, "de 200 emails\n")
   print(user, "con", cantidad, "de 200 email", end=' ')
   apartado_1(pd)
   print(user, "con", cantidad, "de 200 email", end=' ')
   apartado_2(pd)
   print(user, "con", cantidad, "de 200 email", end=' ')
   apartado_3(pd)
   print(user, "con", cantidad, "de 200 email", end=' ')
   apartado_4(pd)
   print(user, "con", cantidad, "de 200 email", end=' ')
   apartado_5(pd)
   print(user, "con", cantidad, "de 200 email", end=' ')
   apartado_6(pd)

def main():
   cursorObj = con.cursor()

   cursorObj.execute('SELECT  * FROM usuarios where email_total <  200 and permisos = 0')
   rows = cursorObj.fetchall()
   pd1 = pd.DataFrame(rows)
   pd1.rename(columns={0: "nombre", 1: "telefono", 2: "contraseña", 3: "provincia", 4: "permisos", 5: "email_total", 6: "email_phishing", 7: "email_clicados"}, inplace=True)

   resultados(pd1, "Usuarios", "menos")


   cursorObj.execute('SELECT  * FROM usuarios where email_total <  200 and permisos = 1')
   rows = cursorObj.fetchall()
   pd2 = pd.DataFrame(rows)
   pd2.rename(columns={0: "nombre", 1: "telefono", 2: "contraseña", 3: "provincia", 4: "permisos", 5: "email_total", 6: "email_phishing", 7: "email_clicados"}, inplace=True)

   resultados(pd2, "Administradores", "menos")


   cursorObj.execute('SELECT  * FROM usuarios where email_total >=  200 and permisos = 0')
   rows = cursorObj.fetchall()
   pd3 = pd.DataFrame(rows)
   pd3.rename(columns={0: "nombre", 1: "telefono", 2: "contraseña", 3: "provincia", 4: "permisos", 5: "email_total", 6: "email_phishing", 7: "email_clicados"}, inplace=True)

   resultados(pd3, "Usuarios", "igual o más")

   cursorObj.execute('SELECT  * FROM usuarios where email_total >=  200 and permisos = 1')
   rows = cursorObj.fetchall()
   pd4 = pd.DataFrame(rows)
   pd4.rename(columns={0: "nombre", 1: "telefono", 2: "contraseña", 3: "provincia", 4: "permisos", 5: "email_total", 6: "email_phishing", 7: "email_clicados"}, inplace=True)

   resultados(pd4, "Administradores", "igual o más")


con = sqlite3.connect('example.db')
main()
con.close()

