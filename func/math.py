import math as py_math

from var import const

FIELDS_32 = {
    # Generador
    'gen_v_l1n','gen_v_l2n','gen_v_l3n','gen_v_l1l2','gen_v_l2l3','gen_v_l3l1',
    'gen_i_l1','gen_i_l2','gen_i_l3','gen_i_earth',
    'gen_w_l1','gen_w_l2','gen_w_l3',
    # Red
    'mains_v_l1n','mains_v_l2n','mains_v_l3n','mains_v_l1l2','mains_v_l2l3','mains_v_l3l1',
    'mains_i_l1','mains_i_l2','mains_i_l3','mains_i_earth',
    'mains_w_l1','mains_w_l2','mains_w_l3',
    # Acumulados / BMS
    'engine_run_hours','gen_kwh_pos','engine_starts','mains_kwh_pos',
    'bus_kwh_pos','fuel_used_l',
}

FIELDS_32_SIGNED = {'gen_w_l1','gen_w_l2','gen_w_l3','mains_w_l1','mains_w_l2','mains_w_l3'}

FIELDS_16_SIGNED = {
    'coolant_temp','oil_temp',
    'gen_current_angle','mains_current_angle','mains_voltage_angle'
}

_SCALED_DEFAULT_VALUES = set(getattr(const, 'controller_default_values', set()))
_SCALED_DEFAULT_TOLERANCE = float(getattr(const, 'controller_default_tolerance', 0.5))

def normalize_addr_0based(addr_abs: int) -> int:
    """Convierte dirección 4xxxx a 0‑based. Si ya es 0‑based, la deja igual."""
    return addr_abs - 40001 if addr_abs >= 40001 else addr_abs

def u32_from_regs(hi: int, lo: int) -> int:
    """Combina dos registros (HI, LO) en un entero sin signo de 32 bits."""
    return ((hi & 0xFFFF) << 16) | (lo & 0xFFFF)

def s32_from_regs(hi: int, lo: int) -> int:
    """Combina HI/LO a entero con signo de 32 bits (two's complement)."""
    u = u32_from_regs(hi, lo)
    return u - 0x100000000 if (u & 0x80000000) else u

def s16(val: int) -> int:
    """Convierte un entero de 16 bits a con signo."""
    return val - 0x10000 if (val & 0x8000) else val

def apply_scale(value: float, scale: float) -> float:
    """Aplica factor de escala (decimal)."""
    return float(value) * float(scale)


def _is_scaled_default(value: float) -> bool:
    if not _SCALED_DEFAULT_VALUES:
        return False
    for sentinel in _SCALED_DEFAULT_VALUES:
        if py_math.isclose(value, float(sentinel), rel_tol=0.0, abs_tol=_SCALED_DEFAULT_TOLERANCE):
            return True
    return False

def extract_value(name: str, dtype: str, decimal: float, regs: dict, addr0: int):
    """
    Extrae y escala un valor desde 'regs' (dict: addr0 -> reg16).
    Devuelve una tupla (valor, es_default) donde es_default indica si el
    controlador está reportando uno de sus valores por defecto (0xFFFF, etc.).
    - dtype: 'float'|'int'|'bool'
    - decimal: factor de escala final
    """
    # 32-bit
    if name in FIELDS_32:
        hi = regs.get(addr0)
        lo = regs.get(addr0 + 1)
        if hi is None or lo is None:
            return None, False

        is_signed = name in FIELDS_32_SIGNED
        if (hi == 0xFFFF and lo == 0xFFFF) or (is_signed and hi == 0x7FFF and lo == 0xFFFF):
            return None, True

        raw = s32_from_regs(hi, lo) if is_signed else u32_from_regs(hi, lo)
        scaled = apply_scale(raw, decimal)
        if _is_scaled_default(scaled):
            return None, True
        return scaled, False

    # 16-bit
    v = regs.get(addr0)
    if v is None:
        return None, False

    if dtype == 'bool':
        if v in (0xFFFF, 0x7FFF):
            return None, True
        return (1.0 if v != 0 else 0.0), False

    is_signed = name in FIELDS_16_SIGNED
    if v == 0xFFFF or (is_signed and v == 0x7FFF):
        return None, True

    if is_signed:
        v = s16(v)

    scaled = apply_scale(v, decimal)
    if _is_scaled_default(scaled):
        return None, True
    return scaled, False
