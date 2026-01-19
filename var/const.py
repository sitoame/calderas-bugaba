
VERSION = "1"
NOMBRE = "Generadores_principales"

plc_targets = {
    'CALDERA_1': {
        'ip': '172.17.31.86',
    },
    'CALDERA_2': {
        'ip': '172.17.31.87',
    },
}

plc_ip = {name: cfg['ip'] for name, cfg in plc_targets.items()}

plc_tags = {
    # ---- AR (Input Registers - lecturas "Real") ----
    'AR[0]': 'intensidad_de_llama_honeywell',
    'AR[1]': 'velocidad_del_ventilador_de_aire_de_combustion',
    'AR[2]': 'kw_de_motor',
    'AR[3]': 'eficiencia_de_la_caldera',
    'AR[4]': 'velocidad_de_combustion',
    'AR[5]': 'nivel_de_o2',
    'AR[6]': 'presion_de_vapor_temp_de_agua_sp',
    'AR[7]': 'nivel_del_agua',
    'AR[8]': 'presion_de_vapor_o_temp_del_agua_caliente',
    'AR[9]': 'ar_9',
    'AR[10]': 'temperatura_de_la_chimenea_antes_de',
    'AR[11]': 'temp_aire_de_combustion',
    'AR[12]': 'temp_deposito_agua_temp_exterior',
    'AR[13]': 'temp_agua_de_alimentacion_temp_salida_agua',
    'AR[14]': 'temp_chimenea_despues_econom_retorno_hw',
    'AR[15]': 'flujo_de_combustible',
    'AR[16]': 'presion_de_entrada_de_gas',
    'AR[17]': 'presion_del_aire_de_atomizacion',
    'AR[18]': 'presion_del_aire_de_combustion',
    'AR[19]': 'presion_de_la_chimenea',
    'AR[20]': 'carga_de_caldera',
    'AR[21]': 'ar_21',
    'AR[22]': 'setpoint_o2',
    'AR[23]': 'ar_23',
    'AR[24]': 'ar_24',
    'AR[25]': 'ar_25',
    'AR[26]': 'ar_26',
    'AR[27]': 'ar_27',
    'AR[28]': 'ar_28',
    'AR[29]': 'ar_29',
    'AR[30]': 'eficiencia_de_la_caldera',
    'AR[31]': 'velocidad_del_ventilador',
    'AR[32]': 'potencia_del_motor',
    'AR[33]': 'ar_33',
    'AR[34]': 'ar_34',
    'AR[35]': 'ar_35',
    'AR[36]': 'ar_36',
    'AR[37]': 'ar_37',
    'AR[38]': 'ar_38',
    'AR[39]': 'ar_39',
    'AR[40]': 'ar_40',
    'AR[41]': 'ar_41',
    'AR[42]': 'ar_42',
    'AR[43]': 'ar_43',
    'AR[44]': 'ar_44',
    'AR[45]': 'ar_45',
    'AR[46]': 'ar_46',
    'AR[47]': 'ar_47',
    'AR[48]': 'ar_48',
    'AR[49]': 'ar_49',

    # ---- AI (Input Registers - lecturas "Entero simple") ----
    'AI[0]': 'estado_control_quemador_linea_1_honeywell',
    'AI[1]': 'falla_ffgr',
    'AI[2]': 'falla_interna_del_controlador_ffgr',
    'AI[3]': 'falla_del_sensor_del_controlador_ffgr',
    'AI[4]': 'estado_secuenciador_honeywell',
    'AI[5]': 'tipo_de_caldera_1_vapor',
    'AI[6]': 'tipo_de_control_de_nivel_1_un_elemento',
    'AI[7]': 'type_of_control_lo_water_1_lwco',
    'AI[8]': 'tipo_de_valvula_principal_de_combustible_1_gas',
    'AI[9]': 'tipo_de_valvula_principal_de_combustible_2_aceite',
    'AI[10]': 'tipo_de_valvula_principal_de_combustible_3_none',
    'AI[11]': 'tipo_de_valvula_de_encendido_1_gas',
    'AI[12]': 'tipo_de_valvula_de_encendido_2_aceite',
    'AI[13]': 'tipo_de_valvula_de_encendido_3_none',
    'AI[14]': 'tipo_de_valvula_de_aislamiento_aceite_onoff',
    'AI[15]': 'tipo_de_valvula_de_retorno_aceite_onoff',
    'AI[16]': 'tipo_de_valvula_de_atomizacion_onoff',
    'AI[17]': 'tipo_de_valvula_fgr_none',
    'AI[18]': 'tipo_de_valvula_seguimiento_aceite_none',
    'AI[19]': 'tipo_de_valvula_compuerta_de_chimenea_onoff',
    'AI[20]': 'tipo_de_analizador_de_o2',
    'AI[21]': 'tipo_de_actuador_de_a_c',
    'AI[22]': 'tipo_de_actuador_de_combustible_1_gas',
    'AI[23]': 'tipo_de_actuador_de_combustible_2_aceite',
    'AI[24]': 'tipo_de_actuador_de_combustible_3_none',
    'AI[25]': 'tipo_de_actuador_de_compuerta_fgr_none',
    'AI[26]': 'tipo_de_actuador_neumatico',
    'AI[27]': 'tipo_de_actuador_farc_none',
    'AI[28]': 'tipo_de_actuador_de_compuerta_de_chimenea',
    'AI[29]': 'tipo_de_interruptor_del_quemador',
    'AI[30]': 'tipo_de_interruptor_de_combustible_1_gas',
    'AI[31]': 'tipo_de_interruptor_de_combustible_2_aceite',
    'AI[32]': 'tipo_de_interruptor_de_combustible_3_none',
    'AI[33]': 'tipo_de_interruptor_de_fuego_bajo',
    'AI[34]': 'tipo_de_interruptor_de_fuego_alto',
    'AI[35]': 'tipo_de_sensor_de_vapor',
    'AI[36]': 'tipo_de_sensor_o2',
    'AI[37]': 'tipo_de_sensor_de_entrada_de_aire_de_combustion',
    'AI[38]': 'tipo_de_sensor_de_entrada_de_economizador',
    'AI[39]': 'tipo_de_sensor_temp_o2_sensor_analizador',
    'AI[40]': 'tipo_de_sensor_de_presion_de_entrada_de_gas',
    'AI[41]': 'tipo_de_sensor_de_presion_de_aire_de_atomizacion',
    'AI[42]': 'tipo_de_sensor_de_presion_de_aire_de_combustion',
    'AI[43]': 'tipo_de_sensor_de_presion_de_chimenea',
    'AI[44]': 'tipo_de_control_de_la_caldera',
    'AI[45]': 'tipo_de_agua_caliente_1_alta',
    'AI[46]': 'tipo_de_agua_caliente_2_none',
    'AI[47]': 'tipo_de_control_de_temp_del_deposito_de_agua',
    'AI[48]': 'tipo_de_control_de_temp_del_agua_caliente',
    'AI[49]': 'tipo_de_control_de_temp_de_salida_del_agua_caliente',
    'AI[50]': 'tipo_de_control_de_temp_del_agua_de_alimentacion',
    'AI[51]': 'tipo_de_control_de_temp_del_agua_de_retorno',
    'AI[52]': 'tipo_de_control_de_adelanto_retardo',
    'AI[53]': 'tipo_de_bms',
    'AI[54]': 'tipo_de_bms_2_none',

    # ---- AD (Input Registers - lecturas "Doble entero") ----
    'AD[0]': 'total_de_horas_de_arranque_del_quemador',
    'AD[1]': 'numero_de_arranques_del_quemador',

    # ---- AWR (Holding Registers - escritura "Real") ----
    'AWR[0]': 'op_rem_caldera_sp',
    'AWR[1]': 'velocidad_de_combustion_rem',
    'AWR[2]': 'op_rem_sp_de_adelanto_retardo_para_dos',
    'AWR[3]': 'awr_3',
    'AWR[4]': 'awr_4',
    'AWR[5]': 'awr_5',
    'AWR[6]': 'awr_6',
    'AWR[7]': 'awr_7',
    'AWR[8]': 'awr_8',
    'AWR[9]': 'awr_9',
}

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
