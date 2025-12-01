import time
import random
import datetime

import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient

# ==============================
# CONFIGURACIÓN
# ==============================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "contraseña borrada por seguridad"
MYSQL_DB = "sensores_db"

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "sensores_db_nosql"
MONGO_COLLECTION = "sensor_readings"

# Intervalo de tiempo entre lecturas (segundos)
INTERVALO_SEGUNDOS = 5


# ==============================
# CONEXIONES
# ==============================

def crear_conexion_mysql():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        if conn.is_connected():
            print("✅ Conectado a MySQL")
            return conn
    except Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
    return None


def crear_conexion_mongo():
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        print("✅ Conectado a MongoDB")
        return db
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        return None


# ==============================
# FUNCIONES DE NEGOCIO
# ==============================

def obtener_sensores(conn_mysql):
    query = """
        SELECT s.id_sensor,
               s.codigo,
               u.latitud,
               u.longitud
        FROM sensores s
        JOIN ubicaciones u ON u.id_ubicacion = s.id_ubicacion
        WHERE s.estado = 'activo';
    """
    cursor = conn_mysql.cursor(dictionary=True)
    cursor.execute(query)
    sensores = cursor.fetchall()
    cursor.close()
    print(f"🔎 Sensores activos encontrados: {len(sensores)}")
    return sensores


def obtener_umbrales_por_sensor(conn_mysql, id_sensor):
    query = """
        SELECT parametro, valor_min, valor_max
        FROM umbrales
        WHERE id_sensor = %s;
    """
    cursor = conn_mysql.cursor(dictionary=True)
    cursor.execute(query, (id_sensor,))
    filas = cursor.fetchall()
    cursor.close()

    umbrales = {}
    for fila in filas:
        umbrales[fila["parametro"]] = (fila["valor_min"], fila["valor_max"])
    return umbrales


def insertar_alerta(conn_mysql, id_sensor, parametro, valor, tipo_alerta):
    query = """
        INSERT INTO alertas (id_sensor, timestamp, parametro, valor, tipo_alerta, atendida)
        VALUES (%s, %s, %s, %s, %s, 0);
    """
    ahora = datetime.datetime.now()
    cursor = conn_mysql.cursor()
    cursor.execute(query, (id_sensor, ahora, parametro, valor, tipo_alerta))
    conn_mysql.commit()
    cursor.close()
    print(f"⚠️ Alerta registrada: sensor={id_sensor}, param={parametro}, valor={valor}, tipo={tipo_alerta}")


def simular_valores():
    temperature = round(random.uniform(15.0, 35.0), 1)
    humidity = round(random.uniform(20.0, 90.0), 1)
    pm2_5 = round(random.uniform(0.0, 50.0), 1)
    return {
        "temperature": temperature,
        "humidity": humidity,
        "pm2_5": pm2_5
    }


def clasificar_alerta(valor, valor_min, valor_max):
    if valor < valor_min or valor > valor_max:
        rango = valor_max - valor_min
        if rango <= 0:
            return "critical"

        if valor < valor_min:
            distancia = valor_min - valor
        else:
            distancia = valor - valor_max

        if distancia > 0.2 * rango:
            return "critical"
        else:
            return "warning"
    return None


# ==============================
# PROCESO PRINCIPAL
# ==============================

def main():
    conn_mysql = crear_conexion_mysql()
    db_mongo = crear_conexion_mongo()

    if not conn_mysql or not db_mongo:
        print("❌ No se pudieron establecer las conexiones necesarias. Saliendo.")
        return

    collection = db_mongo[MONGO_COLLECTION]

    try:
        sensores = obtener_sensores(conn_mysql)
        if not sensores:
            print("No hay sensores activos en MySQL. Verifica los inserts.sql.")
            return

        print("Iniciando simulación de lecturas. Presiona Ctrl+C para detener.\n")

        while True:
            for sensor in sensores:
                id_sensor = sensor["id_sensor"]
                codigo = sensor["codigo"]
                lat = float(sensor["latitud"])
                lng = float(sensor["longitud"])

                values = simular_valores()
                timestamp_utc = datetime.datetime.utcnow()

                doc = {
                    "sensor_id": codigo,
                    "timestamp": timestamp_utc,
                    "location": {"lat": lat, "lng": lng},
                    "values": values,
                    "metadata": {
                        "battery": random.randint(50, 100),
                        "signal_strength": random.choice(["weak", "medium", "strong"])
                    }
                }

                collection.insert_one(doc)
                print(f"✅ Insertada lectura en MongoDB: sensor={codigo}, values={values}")

                umbrales = obtener_umbrales_por_sensor(conn_mysql, id_sensor)
                for parametro, valor in values.items():
                    if parametro in umbrales:
                        valor_min, valor_max = umbrales[parametro]
                        if valor_min is not None and valor_max is not None:
                            tipo_alerta = clasificar_alerta(valor, float(valor_min), float(valor_max))
                            if tipo_alerta is not None:
                                insertar_alerta(conn_mysql, id_sensor, parametro, valor, tipo_alerta)

            time.sleep(INTERVALO_SEGUNDOS)

    except KeyboardInterrupt:
        print("\n🛑 Simulación detenida por el usuario.")
    finally:
        if conn_mysql and conn_mysql.is_connected():
            conn_mysql.close()
            print("🔌 Conexión MySQL cerrada.")


if __name__ == "__main__":
    main()