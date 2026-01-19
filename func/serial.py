import serial

def init_serial_port(port):
    try:
        return serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=10
        )
    except Exception as e:
        print(f"Error al abrir el puerto {port}: {e}")
        return None
