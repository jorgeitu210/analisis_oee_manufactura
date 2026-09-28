import pandas as pd
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="portafolio_oee"
)

df = pd.read_sql("SELECT * FROM produccion", conn)
df_paros = pd.read_sql("SELECT * FROM paros", conn)
conn.close()

df['Tiempo_Operativo_min'] = df['Tiempo_Planeado_min'] - df['Downtime_Total_min']
df['Disponibilidad'] = df['Tiempo_Operativo_min'] / df['Tiempo_Planeado_min']
df['Rendimiento'] = (df['Ciclo_ideal_seg'] * df['Piezas_Producidas']) / (df['Tiempo_Operativo_min'] * 60)
df['Rendimiento'] = df['Rendimiento'].clip(upper=1)
df['Calidad'] = df['Piezas_Buenas'] / df['Piezas_Producidas']
df['OEE'] = df['Disponibilidad'] * df['Rendimiento'] * df['Calidad']

print("OEE promedio general:", round(df['OEE'].mean()*100,1),"%")
print("\nOEE promedio por maquina:")
print((df.groupby('Maquina')['OEE'].mean()*100).round(1))

df.to_csv('producccion_oee.csv', index=False)
df_paros.to_csv('paros_export.csv', index=False)
print("\nExportado: produccion_oee.csv, paros_export.csv")
