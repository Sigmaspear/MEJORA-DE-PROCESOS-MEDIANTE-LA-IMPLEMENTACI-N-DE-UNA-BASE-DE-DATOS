// Seleccionar base de datos
use sensores_db_nosql;

// Colección principal de lecturas
const collection = db.sensor_readings;

// Índice compuesto sensor_id + timestamp (muy útil para series de tiempo)
collection.createIndex(
  { sensor_id: 1, timestamp: -1 },
  { name: "idx_sensor_timestamp" }
);

// Índice geoespacial 2dsphere en location
collection.createIndex(
  { location: "2dsphere" },
  { name: "idx_location_2dsphere" }
);

// Índice TTL: conservar datos 1 año (en segundos)
collection.createIndex(
  { timestamp: 1 },
  {
    name: "idx_timestamp_ttl",
    expireAfterSeconds: 31536000  // 1 año
  }
);