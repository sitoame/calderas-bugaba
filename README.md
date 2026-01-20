# Calderas Bugaba

Servicio de lectura de tags desde un PLC Allen-Bradley (Logix) con `pycomm3` y envío de datos
a InfluxDB usando el escritor por lotes existente.

## Requisitos

- Python 3.10+
- Conectividad al PLC y a InfluxDB

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Editar los destinos del PLC y el diccionario de tags en `var/const.py`:

- `plc_targets`: lista de PLCs con IP.
- `plc_tags`: diccionario `{tag: nombre_de_campo}` leído con `plc.read`.
- `url_influx`, `api_token_influx`, `org_influx`, `bucket_influx`: datos de InfluxDB.

## Ejecución

```bash
python main.py
```

El proceso lector consulta los tags cada 10 segundos y publica el payload
para ingesta inmediata en InfluxDB.

## Escritura a PLC vía MQTT

El servicio también escucha comandos MQTT para escritura de tags en el PLC.
Configura el broker y los topics en `var/const.py`:

- `plc_write_tags`: tags permitidos para escritura (con alias opcional).
- `mqtt_config`: broker, puerto y credenciales.
- `mqtt_write_topics`: topic por PLC (por defecto `calderas/<plc>/write`).

Payload esperado (JSON):

```json
{
  "tag": "AWB[0].0",
  "value": true
}
```

También se puede usar `field` con el alias definido en `plc_write_tags`:

```json
{
  "field": "pulsacion_bms",
  "value": 1
}
```
