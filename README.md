📘 REPORTE FINAL
Mejora de Procesos con un Modelo Híbrido SQL + NoSQL para Monitoreo de Sensores

Maestría en Cómputo Aplicado
Materia: Modelado de Datos
Alumno: Oscar Flores

🧩 Introducción

Este proyecto implementa un sistema de monitoreo de sensores mediante un modelo híbrido SQL + NoSQL, donde:
MySQL administra catálogos, umbrales y alertas, MongoDB almacena lecturas masivas y semiestructuradas provenientes de sensores distribuidos.
La solución optimiza rendimiento, escalabilidad y análisis en tiempo real frente a un sistema basado solo en SQL.

🚨 Planteamiento del Problema

Una organización opera ~300 sensores en distintas ubicaciones.
El sistema previo utilizaba solo SQL para:

* Catálogos

* Lecturas históricas

* Alertas

* Metadatos variables

Lo cual generaba:

⚠️ Consultas lentas (7–12 s por sensor)

⚠️ Mala escalabilidad

⚠️ Dificultad con datos semiestructurados

⚠️ Sobrecarga del servidor SQL

🎯 Objetivo del Proyecto
Diseñar e implementar un sistema que:

Mantenga consistencia e integridad en SQL, Gestione lecturas masivas y flexibles en NoSQL, Mejore rendimiento y escalabilidad, Permita análisis en tiempo real y Automatice alertas mediante un microservicio en Python

🟦 MySQL (SQL)

Ideal para:

Estructura fija, Integridad referencial. Relaciones entre sensores y ubicaciones y Registro formal de alertas

🟩 MongoDB (NoSQL)

Adecuado para:

Datos semiestructurados, Millones de lecturas por día, Series de tiempo, Escalabilidad horizontal, Metadatos variables

🗂 Modelado de Datos
🟦 MySQL (Relacional)

Tablas principales:

* ubicaciones

* sensores

* umbrales

* alertas

Estas contienen la estructura rígida del sistema y mantienen integridad.

🟩 MongoDB (NoSQL)

Colección: sensor_readings

Ejemplo de documento JSON:
```
{
  "sensor_id": "AQS-034",
  "timestamp": "2025-10-21T12:10:34Z",
  "location": { "lat": 20.6736, "lng": -103.344 },
  "values": {
    "temperature": 26.4,
    "humidity": 68,
    "pm2_5": 14
  },
  "metadata": {
    "battery": 92,
    "signal_strength": "strong"
  }
}
```

📌 Índices:

* sensor_id + timestamp

* Índice geoespacial 2dsphere

* Índice TTL para borrar datos antiguos

🏗 Arquitectura General
```
Sensores Simulados ──► Microservicio Python ───┬──► MySQL (catálogos y alertas)
                                               └──► MongoDB (lecturas)
```

El microservicio:

Obtiene sensores desde MySQL
Simula lecturas
Inserta mediciones en MongoDB
Verifica umbrales
Genera alertas automáticamente

🛠 Implementación

📁 Archivos incluidos
```
sql/
  create_tables.sql
  inserts.sql
  consultas.sql

nosql/
  indices_mongodb.js
  modelo_mongodb.md

microservicio/
  ingest_sensores.py

requirements.txt
README.md
```

📈 Resultados

🚀 Inserciones por segundo: 900 → 10,500

⚡ Consulta 24 h por sensor: 7–12 s → 0.8–1.2 s

⚡ Consulta por región: 15 s → 2–3 s

🔧 Manejo flexible de metadatos

🔒 Alta disponibilidad con replica sets (99.98%)

🧩 Conclusión

El modelo híbrido SQL + NoSQL:

* Mejora el rendimiento general

* Escala horizontalmente para series de tiempo

* Mantiene integridad en datos estructurados

* Permite una ingesta continua con Python

* Es adecuado para sistemas industriales reales de monitoreo en tiempo real

🔮 Trabajo Futuro
* Integración con Apache Kafka

* Dashboards en tiempo real (Grafana/Streamlit)

* Machine learning sobre series de tiempo

* Más shards en MongoDB Atlas
