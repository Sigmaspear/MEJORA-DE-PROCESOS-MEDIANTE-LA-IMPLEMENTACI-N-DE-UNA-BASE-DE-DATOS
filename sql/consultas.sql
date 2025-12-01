USE sensores_db;

-- 1. Sensores activos por ubicación
SELECT u.nombre AS ubicacion,
       COUNT(s.id_sensor) AS sensores_activos
FROM ubicaciones u
LEFT JOIN sensores s ON s.id_ubicacion = u.id_ubicacion AND s.estado = 'activo'
GROUP BY u.id_ubicacion, u.nombre;

-- 2. Alertas críticas en el último mes
SELECT s.codigo,
       a.parametro,
       a.valor,
       a.tipo_alerta,
       a.timestamp
FROM alertas a
JOIN sensores s ON s.id_sensor = a.id_sensor
WHERE a.tipo_alerta = 'critical'
  AND a.timestamp >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
ORDER BY a.timestamp DESC;

-- 3. Número de alertas por sensor
SELECT s.codigo,
       COUNT(a.id_alerta) AS total_alertas
FROM sensores s
LEFT JOIN alertas a ON a.id_sensor = s.id_sensor
GROUP BY s.id_sensor, s.codigo
ORDER BY total_alertas DESC;