import sqlite3
import pandas as pd

def apartado_1(pd):
   print("tienen un total de muestras de: ", pd[6].sum())

def apartado_2(pd):
   print("tienen un total de valores missing de:", end=' ')
   try:
      print(pd[6].value_counts().loc[0])
   except:
      print(0)

def apartado_3(pd):
   print("tienen un valor de mediana de: ", pd[6].median())

def apartado_4(pd):
   print("tienen un valor de media de: ", pd[6].mean())

def apartado_5(pd):
   print("tienen un valor de varianza de: ", pd[6].var())

def apartado_6(pd):
   print("tienen un valor mínimo de: ", pd[6].min(), " y máximo de: ", pd[6].max())

def resultados(pd, user, cantidad):
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

   resultados(pd1, "Usuarios", "menos")


   cursorObj.execute('SELECT  * FROM usuarios where email_total <  200 and permisos = 1')
   rows = cursorObj.fetchall()
   pd2 = pd.DataFrame(rows)

   resultados(pd1, "Administradores", "menos")


   cursorObj.execute('SELECT  * FROM usuarios where email_total >=  200 and permisos = 0')
   rows = cursorObj.fetchall()
   pd3 = pd.DataFrame(rows)

   resultados(pd1, "Usuarios", "igual o más")

   cursorObj.execute('SELECT  * FROM usuarios where email_total >=  200 and permisos = 1')
   rows = cursorObj.fetchall()
   pd4 = pd.DataFrame(rows)

   resultados(pd1, "Administradores", "igual o más")



con = sqlite3.connect('example.db')
main()
con.close()

