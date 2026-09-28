import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

maquinas = ['M1', 'M2', 'M3', 'M4']
turnos = ['Mañana', 'Tarde', 'Noche']
fecha_inicio = datetime(2025,1,1)
dias = 90
tiempo_turno_min = 480
ciclo_ideal_base_seg = 12

causas_paro = {
    'Falla mecánica':       {'prob': 0.35, 'duracion_media':45},
    'Cambio de herramienta':        {'prob': 0.25, 'duracion_media':20},
    'Falta de material':        {'prob': 0.15, 'duracion_media':30},
    'Ajuste de calidad':        {'prob': 0.10, 'duracion_media': 15},
    'Falta de operador':        {'prob': 0.08, 'duracion_media': 25},
    'Mantenimiento no programado':      {'prob': 0.07, 'duracion_media': 60},
}

produccion = []
paros = []
registro_id = 1

for dia in range(dias):
    fecha = fecha_inicio + timedelta(days=dia)
    for turno in turnos:
        for maquina in maquinas:
            num_paros = np.random.poisson(1.5)
            downtime_total = 0
            eventos = []

            for _ in range(num_paros):
                causa = np.random.choice(list(causas_paro.keys()),
                              p=[c['prob'] for c in causas_paro.values()])
                duracion = max(5, int(np.random.exponential(causas_paro[causa]['duracion_media'])))
                eventos.append((causa,duracion))
                downtime_total += duracion

            downtime_total = min(downtime_total, tiempo_turno_min - 60)
            tiempo_operativo = tiempo_turno_min - downtime_total

            ciclo_maquina = ciclo_ideal_base_seg * (1 + maquinas.index(maquina)*0.05)
            eficiencia_real = np.random.uniform(0.75, 0.98)
            piezas_producidas = int((tiempo_operativo*60 / ciclo_maquina) * eficiencia_real)
            tasa_defecto = np.random.uniform(0.01, 0.06)
            piezas_defectuosas = int(piezas_producidas*tasa_defecto)
            piezas_buenas = piezas_producidas - piezas_defectuosas

            produccion.append({
                'Registro_ID': registro_id,
                'Fecha': fecha.strftime('%Y-%m-%d'),
                'Turno': turno,
                'Maquina': maquina,
                'Tiempo_Planeado_min': tiempo_turno_min,
                'Downtime_Total_min': downtime_total,
                'Piezas_Producidas': piezas_producidas,
                'Piezas_Buenas': piezas_buenas,
                'Piezas_Defectuosas': piezas_defectuosas,
                'Ciclo_Ideal_seg': round(ciclo_maquina,2)
            })

            for causa, duracion in eventos:
                paros.append({
                    'Registro_ID': registro_id,
                    'Fecha': fecha.strftime('%Y-%m-%d'),
                    'Turno': turno,
                    'Maquina': maquina,
                    'Causa_Paro': causa,
                    'Duracion_min': duracion
                })

            registro_id += 1

df_prodcuccion = pd.DataFrame(produccion)
df_paros    = pd.DataFrame(paros)

df_prodcuccion.to_csv('produccion.csv', index=False, encoding='utf-8-sig')
df_paros.to_csv('paros.csv', index=False, encoding='utf-8-sig')

print ("Registros de producción:", len(df_prodcuccion))
print("Eventos de paro:", len(df_paros))
print(df_prodcuccion.head())
print(df_paros.head())
