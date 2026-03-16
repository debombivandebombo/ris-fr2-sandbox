import socket
import json
import os
import sys
import platform

if os.name == 'nt':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'windows_x86_64'))
    from windows_x86_64 import RIS
    if platform.machine() == 'aarch64':
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'linux_aarch64'))
        from linux_aarch64 import RIS
    else:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'linux_x86_64'))
        from linux_x86_64 import RIS

# Configuración del Socket
UDP_IP = "127.0.0.1"
UDP_PORT = 17000 # Puerto diferente al del radar

def start_server():
    # Inicializar la RIS real
    ris_hw = RIS()
    ris_hw.on()
    print(f"{ris_hw.pixels = }")
    print("RIS Server started. Listening on port 17000...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    try:
        while True:
            data, addr = sock.recvfrom(65535) # Búfer grande para los 3200 píxeles
            msg = json.loads(data.decode('utf-8'))
            
            command = msg.get("cmd")
            
            if command == "SET_CONFIG":
                # Aplicar la configuración recibida
                config_list = msg.get("data")
                ris_hw.set_specified_states(config_list)
                print("New configuration applied")
            
            elif command == "OFF":
                ris_hw.off()
                print("RIS turned OFF by remote command.")
            
            elif command == "ON":
                ris_hw.on()
                print("RIS turned ON by remote command.")

    except KeyboardInterrupt:
        ris_hw.off()
        print("Server stopped.")

if __name__ == "__main__":
    start_server()