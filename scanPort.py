from serial.tools import list_ports

def scanPort():
    available_ports = list_ports.comports()
    return [port.device for port in available_ports]