USE sensores_db;

-- Ubicaciones de ejemplo
INSERT INTO ubicaciones (nombre, latitud, longitud, descripcion) VALUES
('Planta Norte', 20.673600, -103.344000, 'Zona norte de la planta'),
('Planta Sur',   20.650000, -103.350000, 'Zona sur de la planta'),
('Centro',       20.670000, -103.330000, 'Centro de monitoreo');

-- Sensores de ejemplo
INSERT INTO sensores (codigo, tipo, id_ubicacion, fecha_instalacion, estado) VALUES
('AQS-001', 'calidad_aire', 1, '2024-01-15', 'activo'),
('AQS-002', 'calidad_aire', 1, '2024-02-10', 'activo'),
('TMP-010', 'temperatura',  2, '2024-03-05', 'activo'),
('HMD-020', 'humedad',      3, '2024-04-01', 'activo');

-- Umbrales de ejemplo
INSERT INTO umbrales (id_sensor, parametro, valor_min, valor_max) VALUES
(1, 'temperature', 18.0, 30.0),
(1, 'humidity',    30.0, 70.0),
(1, 'pm2_5',       0.0,  25.0),

(2, 'temperature', 18.0, 30.0),
(2, 'humidity',    30.0, 70.0),
(2, 'pm2_5',       0.0,  25.0),

(3, 'temperature', 16.0, 28.0),

(4, 'humidity',    40.0, 80.0);