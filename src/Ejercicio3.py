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

def main():
   cursorObj = con.cursor()

   cursorObj.execute('SELECT  * FROM usuarios where email_total <  200 and permisos = 0')
   rows = cursorObj.fetchall()
   pd1 = pd.DataFrame(rows)
   #print("Usuarios con menos de 200 email", end=' ')
   #apartado_1(pd1)
   #print("Usuarios con menos de 200 email", end=' ')
   #apartado_2(pd1)
   #print("Usuarios con menos de 200 email", end=' ')
   #apartado_3(pd1)
   #print("Usuarios con menos de 200 email", end=' ')
   #apartado_4(pd1)
   #print("Usuarios con menos de 200 email", end=' ')
   #apartado_5(pd1)
   #print("Usuarios con menos de 200 email", end=' ')
   #apartado_6(pd1)

   cursorObj.execute('SELECT  * FROM usuarios where email_total <  200 and permisos = 1')
   rows = cursorObj.fetchall()
   pd2 = pd.DataFrame(rows)
   #print("Administradores con menos de 200 email", end=' ')
   #apartado_1(pd2)
   #print("Administradores con menos de 200 email", end=' ')
   #apartado_3(pd2)
   #print("Administradores con menos de 200 email", end=' ')
   #apartado_4(pd2)
   #print("Administradores con menos de 200 email", end=' ')
   #apartado_5(pd2)
   #print("Administradores con menos de 200 email", end=' ')
   #apartado_6(pd2)

   cursorObj.execute('SELECT  * FROM usuarios where email_total >=  200 and permisos = 0')
   rows = cursorObj.fetchall()
   pd3 = pd.DataFrame(rows)
   #print("Usuarios con igual o más de 200 email", end=' ')
   #apartado_1(pd3)
   #print("Usuarios con igual o más de 200 email", end=' ')
   #apartado_2(pd3)
   #print("Usuarios con igual o más de 200 email", end=' ')
   #apartado_3(pd3)
   #print("Usuarios con igual o más de 200 email", end=' ')
   #apartado_4(pd3)
   #print("Usuarios con igual o más de 200 email", end=' ')
   #apartado_5(pd3)
   #print("Usuarios con igual o más de 200 email", end=' ')
   #apartado_6(pd3)

   cursorObj.execute('SELECT  * FROM usuarios where email_total >=  200 and permisos = 1')
   rows = cursorObj.fetchall()
   pd4 = pd.DataFrame(rows)
   #print("Administradores con igual o más de 200 email", end=' ')
   #apartado_1(pd4)
   #print("Administradores con igual o más de 200 email", end=' ')
   #apartado_2(pd4)
   #print("Administradores con igual o más de 200 email", end=' ')
   #apartado_3(pd4)
   #print("Administradores con igual o más de 200 email", end=' ')
   #apartado_4(pd4)
   #print("Administradores con igual o más de 200 email", end=' ')
   #apartado_5(pd4)
   #print("Administradores con igual o más de 200 email", end=' ')
   #apartado_6(pd4)


con = sqlite3.connect('example.db')
main()
con.close()

