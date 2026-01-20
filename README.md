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
