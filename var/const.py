
VERSION = "1"
NOMBRE = "Calderas"

plc_targets = {
    'CALDERA_1_prueba_6': {
        'ip': '172.17.31.87',
    },
    'CALDERA_2_prueba_6': {
        'ip': '172.17.31.86',
    }
}

plc_ip = {name: cfg['ip'] for name, cfg in plc_targets.items()}

plc_tags = {
    # ---- AR (Input Registers - lecturas "Real") ----
    # 'AR[0]': 'intensidad_de_llama_honeywell',
    # 'AR[1]': 'velocidad_del_ventilador_de_aire_de_combustion',
    # 'AR[2]': 'kw_de_motor',
    'AR[3]': 'efficiency',
    'AR[4]': 'firing_rate',
    # 'AR[5]': 'nivel_de_o2',
    'AR[6]': 'steam_pressure_sp',
    'AR[7]': 'water_level',
    'AR[8]': 'steam_pressure',
    # 'AR[9]': 'ar_9',
    'AR[10]': 'stack_temperature',
    # 'AR[11]': 'temp_aire_de_combustion',
    'AR[12]': 'water_temp',
    # 'AR[13]': 'temp_agua_de_alimentacion_temp_salida_agua',
    # 'AR[14]': 'temp_chimenea_despues_econom_retorno_hw',
    # 'AR[15]': 'flujo_de_combustible',
    # 'AR[16]': 'presion_de_entrada_de_gas',
    # 'AR[17]': 'presion_del_aire_de_atomizacion',
    # 'AR[18]': 'presion_del_aire_de_combustion',
    # 'AR[19]': 'presion_de_la_chimenea',
    # 'AR[20]': 'carga_de_caldera',
    # 'AR[22]': 'setpoint_o2',
    # 'AR[30]': 'eficiencia_de_la_caldera',
    # 'AR[31]': 'velocidad_del_ventilador',
    # 'AR[32]': 'potencia_del_motor',

    # # ---- AD (Input Registers - lecturas "Doble entero") ----
    'AD[0]': 'total_de_horas_de_arranque_del_quemador',
    'AD[1]': 'numero_de_arranques_del_quemador',

    # ---- AB[0] ----
    'AB[0].0': 'falla_de_unidad',
    # 'AB[0].1': 'error_comunicacion_modbus',
    'AB[0].2': 'bajo_nivel_de_agua',
    'AB[0].3': 'alarma_control_del_quemador',
    'AB[0].4': 'limites_de_caldera_abiertos',
    # 'AB[0].5': 'alarma_temp_alta_chimenea',
    # 'AB[0].6': 'apagado_por_temp_alta_chimenea',
    # 'AB[0].7': 'enclavamiento_externo',
    # 'AB[0].8': 'falla_modulo_entradas_salidas',
    # 'AB[0].9': 'falla_sensor_vapor',
    # 'AB[0].10': 'alarma_actuador_neumatico_fuera_posicion',
    # 'AB[0].11': 'alarma_actuador_gas_fuera_posicion',
    # 'AB[0].12': 'falla_controlador_relacion_aire_combustible',
    # 'AB[0].13': 'ningun_combustible_seleccionado',
    # 'AB[0].14': 'bateria_plc_baja',
    # 'AB[0].15': 'falla_rele_limite_no_reciclado',

    # ---- AB[1] ----
    # 'AB[1].0': 'falla_rele_limite_reciclado',
    # 'AB[1].1': 'falla_senal_modulacion_remota',
    # 'AB[1].2': 'falla_sensor_presion_cabezal',
    # 'AB[1].3': 'falla_canal_temperatura_0_5',
    # 'AB[1].4': 'alarma_o2_bajo',
    'AB[1].5': 'alarma_limite_alto',
    # 'AB[1].6': 'alwco',
    # 'AB[1].7': 'presion_gas_baja_o_temp_aceite_baja',
    # 'AB[1].8': 'presion_aceite_alta_o_temp_aceite_alta',
    # 'AB[1].9': 'presion_aceite_baja',
    # 'AB[1].10': 'presion_aceite_alta',
    # 'AB[1].11': 'interruptor_cajon_aceite_no_hecho',
    # 'AB[1].12': 'presion_aire_atomizacion_baja',
    # 'AB[1].13': 'presion_aire_combustion_baja',
    # 'AB[1].14': 'alta_presion_compuerta_chimenea',
    # 'AB[1].15': 'alarma_auxiliar_2',

    # ---- AB[2] ----
    'AB[2].0': 'soplador_encendido',
    # 'AB[2].1': 'entrada_purga',
    # 'AB[2].2': 'liberado_para_modular',
    # 'AB[2].3': 'interruptor_fuego_bajo',
    # 'AB[2].4': 'interruptor_fuego_alto',
    # 'AB[2].5': 'listo_para_arranque_limites_cerrados',
    # 'AB[2].6': 'enclavamiento_arranque_externo',
    # 'AB[2].7': 'alfco',
    'AB[2].8': 'piloto_encendido',
    'AB[2].9': 'valvula_principal_combustible_abierta',
    # 'AB[2].10': 'combustible_1_seleccionado',
    # 'AB[2].11': 'combustible_2_seleccionado',
    # 'AB[2].12': 'pulsacion_hacia_bms',
    # 'AB[2].13': 'apagado_lwco',
    # 'AB[2].14': 'habilitacion_remota',
    # 'AB[2].15': 'interruptor_quemador',

    # ---- AB[3] ----
    # 'AB[3].0': 'rele_limite_reciclado',
    # 'AB[3].1': 'arranque_dispositivo_externo',
    # 'AB[3].2': 'rele_limite_no_reciclado',
    # 'AB[3].3': 'variador_en_fuego_bajo',
    # 'AB[3].4': 'arranque_caldera_esclava',
    # 'AB[3].5': 'salida_demanda_carga',
    # 'AB[3].6': 'salida_alarma_general',
    'AB[3].7': 'caldera_lista',
    # 'AB[3].8': 'demanda_carga_caldera',
    # 'AB[3].9': 'velocidad_combustion_remota_retardo',
    # 'AB[3].10': 'velocidad_combustion_manual',
    'AB[3].11': 'modo_automatico',
    # 'AB[3].12': 'espera_en_caliente',
    # 'AB[3].13': 'calentamiento',
    # 'AB[3].14': 'combustible_3_seleccionado',
    # 'AB[3].15': 'alarma_auxiliar_3',

    # ---- AB[4] ----
    # 'AB[4].0': 'modo_vapor',
    # 'AB[4].1': 'nivel_maestro_presente',
    # 'AB[4].2': 'variador_velocidad_presente',
    # 'AB[4].3': 'economizador_presente',
    # 'AB[4].4': 'sensor_temp_aire_combustion_presente',
    # 'AB[4].5': 'sensor_fw_economizador_presente',
    # 'AB[4].6': 'analizador_o2_presente',
    # 'AB[4].7': 'sensor_temp_agua_presente',
    # 'AB[4].8': 'reinicio_exterior_habilitado',
    # 'AB[4].9': 'posicionamiento_paralelo_habilitado',
    # 'AB[4].10': 'modo_maestro_adelanto_retardo',
    # 'AB[4].11': 'modo_esclavo_adelanto_retardo',
    # 'AB[4].12': 'panel_maestro_seleccionado',
    # 'AB[4].13': 'espera_en_caliente_por_seleccion',
    # 'AB[4].14': 'setpoint_doble_seleccionado',
    # 'AB[4].15': 'ranura_8_canal_0_ai',

    # ---- AB[5] ----
    # 'AB[5].0': 'ranura_8_canal_1_ai',
    # 'AB[5].1': 'ranura_8_canal_2_ai',
    # 'AB[5].2': 'ranura_8_canal_3_ai',
    # 'AB[5].3': 'control_fireye',
    # 'AB[5].4': 'alarma_agua_alta',
    # 'AB[5].5': 'alarma_actuador_aceite_fuera_posicion',
    # 'AB[5].6': 'alarma_actuador_fgr_fuera_posicion',
    # 'AB[5].7': 'alarma_falla_feedback_actuador_neumatico_baja',
    # 'AB[5].8': 'alarma_falla_feedback_actuador_neumatico_alta',
    # 'AB[5].9': 'alarma_feedback_actuador_gas_baja',
    # 'AB[5].10': 'alarma_feedback_actuador_gas_alta',
    # 'AB[5].11': 'alarma_feedback_actuador_aceite_baja',
    # 'AB[5].12': 'alarma_feedback_actuador_aceite_alta',
    # 'AB[5].13': 'alarma_feedback_actuador_fgr_baja',
    # 'AB[5].14': 'alarma_feedback_actuador_fgr_alta',
    # 'AB[5].15': 'alarma_desviacion_vsd',

    'AB[6].10': 'alarma_presion_vapor_baja'

}

plc_write_tags = {
    'AWB[0].0': 'pulsacion_bms',
    'AWB[0].1': 'arranque_rem_bms',

    'AWR[0]': 'caldera_sp',
    'AWR[1]': 'firing_rate',
    # 'AWR[2]': 'op_rem_sp_de_adelanto_retardo_para_dos',
}

mqtt_config = {
    "broker": "172.17.31.11",
    "port": 1883,
    "username": 'telegraf',
    "password": 'telegraf',
}

mqtt_write_topics = {
    name: f"{name}"
    for name in plc_targets.keys()
}

url_influx = 'http://172.17.31.11:8086'
api_token_influx = '8v5ffFjMYmQrZEwWInZj_OjOUTO6gXNf_6DB6yMV1Yq2fJK1Z043V6TOdgS4wHrE6PjwyV7KJY--Mi14s8hAdA=='
org_influx = 'maxia'
bucket_influx = 'sensores_prueba_3'

# Valores por defecto reportados por el controlador cuando no tiene datos reales.
# Se expresan en unidades finales (ej. 65.35k -> 65350.0).
controller_default_values = {
    65531.0, 
    429500000.0,
    32760.0,
}
# Tolerancia absoluta para comparar contra los valores anteriores.
controller_default_tolerance = 5.0
