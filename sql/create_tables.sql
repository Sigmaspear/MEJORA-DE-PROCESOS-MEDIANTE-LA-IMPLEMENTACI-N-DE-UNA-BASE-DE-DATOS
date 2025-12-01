-- Crear base de datos
CREATE DATABASE IF NOT EXISTS sensores_db;
USE sensores_db;

-- Tabla de ubicaciones
CREATE TABLE IF NOT EXISTS ubicaciones (
    id_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    latitud DECIMAL(9,6) NOT NULL,
    longitud DECIMAL(9,6) NOT NULL,
    descripcion VARCHAR(255)
);

-- Tabla de sensores
CREATE TABLE IF NOT EXISTS sensores (
    id_sensor INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL,
    id_ubicacion INT NOT NULL,
    fecha_instalacion DATE,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id_ubicacion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Tabla de umbrales
CREATE TABLE IF NOT EXISTS umbrales (
    id_umbral INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL,
    parametro VARCHAR(50) NOT NULL,
    valor_min DECIMAL(10,2),
    valor_max DECIMAL(10,2),
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Tabla de alertas
CREATE TABLE IF NOT EXISTS alertas (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL,
    timestamp DATETIME NOT NULL,
    parametro VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    tipo_alerta ENUM('warning', 'critical') NOT NULL,
    atendida TINYINT(1) DEFAULT 0,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);