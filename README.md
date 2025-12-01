# Mejora de procesos mediante un modelo híbrido SQL + NoSQL para monitoreo de sensores

Maestría en Cómputo Aplicado  
Materia: Modelado de Datos

## Descripción general

Este proyecto muestra cómo combinar una base de datos relacional (MySQL) con una base de datos NoSQL orientada a documentos (MongoDB) para mejorar el rendimiento, la escalabilidad y la flexibilidad en el monitoreo de sensores distribuidos.

- **MySQL** se utiliza para:
  - Catálogo de sensores
  - Ubicaciones
  - Umbrales
  - Registro de alertas

- **MongoDB** se utiliza para:
  - Almacenamiento masivo de lecturas de sensores (series de tiempo)
  - Manejo de datos semiestructurados (metadatos, firmware, señal, etc.)

## Estructura del proyecto

```text
.
├── sql/
│   ├── create_tables.sql     # Definición de tablas en MySQL
│   ├── inserts.sql           # Datos de ejemplo (sensores, ubicaciones, umbrales)
│   └── consultas.sql         # Consultas de ejemplo para el reporte
├── nosql/
│   └── indices_mongodb.js    # Creación de índices en MongoDB
├── microservicio/
│   └── ingest_sensores.py    # Script de simulación e ingesta de lecturas
└── requirements.txt          # Dependencias de Python