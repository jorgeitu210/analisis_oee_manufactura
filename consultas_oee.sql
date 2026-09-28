SELECT Maquina, SUM(Downtime_Total_min) AS downtime_total,
	ROUND(AVG(Downtime_Total_min),1) AS downtime_promedio
FROM produccion
GROUP BY Maquina
ORDER BY downtime_total DESC;

SELECT Maquina,
	SUM(Piezas_Producidas) AS total_piezas,
    ROUND(SUM(Piezas_Defectuosas)/SUM(Piezas_Producidas)*100,2) AS tasa_defecto_pct
FROM produccion
GROUP BY Maquina;

SELECT Causa_Paro, COUNT(*) AS num_eventos, SUM(Duracion_min) AS minutos_totales
FROM paros
GROUP BY Causa_Paro
ORDER BY minutos_totales DESC;