
VERSION = "1"
NOMBRE = "Generadores_principales"

mbus_targets = {
    'CALDERA_1': {
        'ip': '172.17.31.86',
        'port': 502,
        'slave_id': 1,
    },
    'CALDERA_2': {
        'ip': '172.17.31.87',
        'port': 502,
        'slave_id': 1,
    },
}

mbus_gwy_port = 502
mbus_gwy_slv_id = 1
mbus_gwy_ip = {name: cfg['ip'] for name, cfg in mbus_targets.items()}

url_influx = 'http://172.17.31.11:8086'
api_token_influx = '8v5ffFjMYmQrZEwWInZj_OjOUTO6gXNf_6DB6yMV1Yq2fJK1Z043V6TOdgS4wHrE6PjwyV7KJY--Mi14s8hAdA=='
org_influx = 'maxia'
bucket_influx = 'sensores_calderas'

# Valores por defecto reportados por el controlador cuando no tiene datos reales.
# Se expresan en unidades finales (ej. 65.35k -> 65350.0).
controller_default_values = {
    65531.0, 
    429500000.0,
    32760.0,
}
# Tolerancia absoluta para comparar contra los valores anteriores.
controller_default_tolerance = 5.0
