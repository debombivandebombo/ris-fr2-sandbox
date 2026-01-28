## Run the RIS Hardware Server
```bash
uv run python ris_hardware_server.py
```

## How to use the RIS Hardware Server
3 types of commands are available:
- "ON" : turn on the RIS
- "OFF" : turn off the RIS
- "SET_CONFIG" : set the RIS to a specified configuration

1. Create the class to control the RIS Hardware Server with a Python class
```python
import socket
import json
from dataclasses import dataclass

@dataclass
class RISConfig:
    state_matrix_v: np.ndarray  # Vertical polarization state matrix (i.e. 40x40)
    state_matrix_h: np.ndarray  # Horizontal polarization state matrix (i.e. 40x40)

class RISServerController:
    def __init__(self, ip="127.0.0.1", port=17000):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self._send_command("ON")

    def disconnect(self):
        self._send_command("OFF")

    def apply_config(self, config: RISConfig):
        v_flat = config.state_matrix_v[::-1, :].T.flatten().astype(int)
        h_flat = config.state_matrix_h[::-1, :].T.flatten().astype(int)

        gw_pattern = [0] * (v_flat.size + h_flat.size)
        gw_pattern[0::2] = v_flat.tolist()
        gw_pattern[1::2] = h_flat.tolist()

        # Apply the config to the RIS
        self._send_command("SET_CONFIG", gw_pattern)

    def _send_command(self, cmd, data=None):
        msg = {"cmd": cmd, "data": data}
        self.sock.sendto(json.dumps(msg).encode('utf-8'), self.addr)
```

2. Use the class to control the RIS Hardware Server
```python
# from ... import RISServerController, RISConfig

# Create the controller
controller = RISServerController()

# Connect to the RIS
controller.connect()

# Apply a configuration
config = RISConfig(
    state_matrix_v=np.random.randint(0, 2, (40, 40)),
    state_matrix_h=np.random.randint(0, 2, (40, 40))
)
controller.apply_config(config)

# Disconnect from the RIS
controller.disconnect()
```



