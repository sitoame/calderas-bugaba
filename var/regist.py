import numpy as np

_DSE = np.array([
    # =========================
    # MOTOR (Page 4 – offsets 0..6)
    # =========================
    (41025, 'float', 'oil_pressure',       0.0, 1.0),        # kPa (16-bit)   p4 o0
    (41026, 'float', 'coolant_temp',       0.0, 1.0),        # °C (16-bit,s)  p4 o1
    (41027, 'float', 'oil_temp',           0.0, 1.0),        # °C (16-bit,s)  p4 o2
    (41028, 'float', 'fuel_level',         0.0, 1.0),        # %  (16-bit)    p4 o3
    (41029, 'float', 'alt_charge_volt',    0.0, 0.1),        # V  (16-bit)    p4 o4
    (41030, 'float', 'engine_batt_volt',   0.0, 0.1),        # V  (16-bit)    p4 o5
    (41031, 'float', 'engine_speed',       0.0, 1.0),        # RPM (16-bit)   p4 o6

    # =========================
    # GENERADOR (Page 4 – offsets 7..33)
    # =========================
    (41032, 'float', 'gen_freq',           0.0, 0.1),        # Hz (16-bit)    p4 o7
    (41033, 'float', 'gen_v_l1n',          0.0, 0.1),        # V  (32-bit)    p4 o8-9
    (41035, 'float', 'gen_v_l2n',          0.0, 0.1),        # V  (32-bit)    p4 o10-11
    (41037, 'float', 'gen_v_l3n',          0.0, 0.1),        # V  (32-bit)    p4 o12-13
    (41039, 'float', 'gen_v_l1l2',         0.0, 0.1),        # V  (32-bit)    p4 o14-15
    (41041, 'float', 'gen_v_l2l3',         0.0, 0.1),        # V  (32-bit)    p4 o16-17
    (41043, 'float', 'gen_v_l3l1',         0.0, 0.1),        # V  (32-bit)    p4 o18-19
    (41045, 'float', 'gen_i_l1',           0.0, 0.1),        # A  (32-bit)    p4 o20-21
    (41047, 'float', 'gen_i_l2',           0.0, 0.1),        # A  (32-bit)    p4 o22-23
    (41049, 'float', 'gen_i_l3',           0.0, 0.1),        # A  (32-bit)    p4 o24-25
    (41051, 'float', 'gen_i_earth',        0.0, 0.1),        # A  (32-bit)    p4 o26-27
    (41053, 'float', 'gen_w_l1',           0.0, 1.0),        # W  (32-bit,s)  p4 o28-29
    (41055, 'float', 'gen_w_l2',           0.0, 1.0),        # W  (32-bit,s)  p4 o30-31
    (41057, 'float', 'gen_w_l3',           0.0, 1.0),        # W  (32-bit,s)  p4 o32-33
    (41059, 'float', 'gen_current_angle',  0.0, 1.0),        # °  (16-bit,s)  p4 o34

    # =========================
    # RED / MAINS (Page 4 – offsets 35..65)
    # =========================
    (41060, 'float', 'mains_freq',         0.0, 0.1),        # Hz (16-bit)    p4 o35
    (41061, 'float', 'mains_v_l1n',        0.0, 0.1),        # V  (32-bit)    p4 o36-37
    (41063, 'float', 'mains_v_l2n',        0.0, 0.1),        # V  (32-bit)    p4 o38-39
    (41065, 'float', 'mains_v_l3n',        0.0, 0.1),        # V  (32-bit)    p4 o40-41
    (41067, 'float', 'mains_v_l1l2',       0.0, 0.1),        # V  (32-bit)    p4 o42-43
    (41069, 'float', 'mains_v_l2l3',       0.0, 0.1),        # V  (32-bit)    p4 o44-45
    (41071, 'float', 'mains_v_l3l1',       0.0, 0.1),        # V  (32-bit)    p4 o46-47
    (41073, 'float', 'mains_voltage_angle',0.0, 1.0),        # °  (16-bit,s)  p4 o48
    (41074, 'int',   'gen_phase_rotation', 0.0, 1.0),        # 0..3 (16-bit)  p4 o49
    (41075, 'int',   'mains_phase_rotation',0.0, 1.0),       # 0..3 (16-bit)  p4 o50
    (41076, 'float', 'mains_current_angle',0.0, 1.0),        # °  (16-bit,s)  p4 o51
    (41077, 'float', 'mains_i_l1',         0.0, 0.1),        # A  (32-bit)    p4 o52-53
    (41079, 'float', 'mains_i_l2',         0.0, 0.1),        # A  (32-bit)    p4 o54-55
    (41081, 'float', 'mains_i_l3',         0.0, 0.1),        # A  (32-bit)    p4 o56-57
    (41083, 'float', 'mains_i_earth',      0.0, 0.1),        # A  (32-bit)    p4 o58-59
    (41085, 'float', 'mains_w_l1',         0.0, 1.0),        # W  (32-bit,s)  p4 o60-61
    (41087, 'float', 'mains_w_l2',         0.0, 1.0),        # W  (32-bit,s)  p4 o62-63
    (41089, 'float', 'mains_w_l3',         0.0, 1.0),        # W  (32-bit,s)  p4 o64-65

    # =========================
    # ACUMULADOS / BMS (Page 7 – Accumulated Instrumentation)
    # =========================
    # Base Page 7 = 40001 + 7*256 = 41793  :contentReference[oaicite:0]{index=0}
    # Offsets 6–7 Engine run time (Seconds, 32-bit) :contentReference[oaicite:1]{index=1}
    (41799, 'float', 'engine_run_hours',   0.0, 1.0/3600.0),  # Engine run time (s) -> h, p7 o6-7
    # Offsets 8–9 Generator positive kWh  (0.1 kWh, 32-bit) :contentReference[oaicite:2]{index=2}
    (41801, 'float', 'gen_kwh_pos',        0.0, 0.1),         # Generator positive kWh, p7 o8-9
    # Offsets 16–17 Number of starts :contentReference[oaicite:3]{index=3}
    (41809, 'float', 'engine_starts',      0.0, 1.0),         # Número de arranques, p7 o16-17
    # Offsets 18–19 Mains positive kWh :contentReference[oaicite:4]{index=4}
    (41811, 'float', 'mains_kwh_pos',      0.0, 0.1),         # Mains positive kWh, p7 o18-19
    # Offsets 26–27 Bus positive kWh :contentReference[oaicite:5]{index=5}
    (41819, 'float', 'bus_kwh_pos',        0.0, 0.1),         # Bus positive kWh, p7 o26-27
    # Offsets 34–35 Fuel used (Litres) :contentReference[oaicite:6]{index=6}
    (41827, 'float', 'fuel_used_l',        0.0, 1.0),         # Combustible consumido, L, p7 o34-35

    # =========================
    # REMOTE CONTROL OUTPUTS (Page 193 – se pueden leer como estado)
    # =========================
    (89409, 'bool',  'remote_out1',        0.0, 1.0),         # p193 o0 (0/1)
    (89410, 'bool',  'remote_out2',        0.0, 1.0),
    (89411, 'bool',  'remote_out3',        0.0, 1.0),
    (89412, 'bool',  'remote_out4',        0.0, 1.0),
    (89413, 'bool',  'remote_out5',        0.0, 1.0),

    # =========================
    # ECU – TROUBLE CODES (Page 142 – conteo / lámparas)
    # =========================
    (76353, 'int',   'ecu_tc_count',       0.0, 1.0),         # p142 o0
    (76354, 'int',   'ecu_tc_lamps',       0.0, 1.0),         # p142 o1 (bitfield)
], dtype=[
    ('address',  np.int32),
    ('type',     (np.str_, 10)),
    ('data',     (np.str_, 40)),
    ('value',    np.float64),
    ('decimal',  np.float64)
])
