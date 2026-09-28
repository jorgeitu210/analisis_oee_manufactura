import pandas as pd
import pymysql

df_produccion = pd.read_csv("produccion.csv")
df_paros = pd.read_csv("paros.csv")

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "portafolio_oee"
)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS paros")
cursor.execute("DROP TABLE IF EXISTS produccion")

cursor.execute("""
CREATE TABLE produccion (
    Registro_ID INT PRIMARY KEY,
    Fecha DATE,
    Turno VARCHAR(20),
    Maquina VARCHAR(10),
    Tiempo_Planeado_min INT,
    Downtime_Total_min INT,
    Piezas_Producidas INT,
    Piezas_Buenas INT,
    Piezas_Defectuosas INT,
    Ciclo_ideal_seg DOUBLE
    )
    """)

cursor.execute("""
CREATE TABLE paros(
    Paro_ID INT AUTO_INCREMENT PRIMARY KEY,
    Registro_ID INT,
    Fecha DATE,
    Turno VARCHAR(20),
    Maquina VARCHAR(10),
    Causa_Paro VARCHAR(50),
    Duracion_min INT,
    FOREIGN KEY (Registro_ID) REFERENCES produccion(Registro_ID)
    )
    """)

cols_p = ",".join([f"`{c}`" for c in df_produccion.columns])
placeholders_p = ",".join(["%s"]*len(df_produccion.columns))
cursor.executemany(f"INSERT INTO produccion ({cols_p}) VALUES ({placeholders_p})",
                   [tuple(row) for row in df_produccion.to_numpy()])

cols_pa = ",".join([f"`{c}`" for c in df_paros.columns])
placeholders_pa = ",".join(["%s"]*len(df_paros.columns))
cursor.executemany(f"INSERT INTO paros ({cols_pa}) VALUES ({placeholders_pa})",
                   [tuple(row) for row in df_paros.to_numpy()])

conn.commit()
print("Filas insertadas en producción:", len(df_produccion))
print("Filas insertadas en paros:", len(df_paros))

cursor.close()
conn.close()