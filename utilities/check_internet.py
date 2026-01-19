import socket
def isInternetAvailable():
    try:
        # Intentar conectarse a un servidor DNS de confianza (en este caso, Google DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except socket.timeout:
        return False
    except OSError:
        return False