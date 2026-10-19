import platform
import numpy as np
from surpRISe.optimization import WMMSE_MM_Optimizer

# Importación dinámica del driver según tu arquitectura en ris-fr2-sandbox
arch = f"{platform.system().lower()}_{platform.machine().lower()}"
print(f"Detectada arquitectura de control: {arch}")


def phases_to_bit_states(phases_deg: np.ndarray, n_bits: int = 1) -> np.ndarray:
    """
    Convierte la matriz de fases en grados (ej. 0°, 180° para 1 bit)
    en estados enteros (0, 1, ..., 2^B - 1) requeridos por la placa física de la RIS.
    """
    step = 360.0 / (2 ** n_bits)
    states = np.round(phases_deg / step).astype(int) % (2 ** n_bits)
    return states


def apply_ris_configuration(phase_matrix_deg: np.ndarray, n_bits: int = 1):
    """
    Traduce la matriz de fases y la aplica al controlador de hardware.
    """
    state_matrix = phases_to_bit_states(phase_matrix_deg, n_bits=n_bits)
    print("Matriz de estados digitales a escribir en la RIS:")
    print(state_matrix)

    # =========================================================================
    # PUNTO DE CONEXIÓN CON TU HARDWARE EN ris-fr2-sandbox:
    # Sustituye la llamada inferior por la función exacta que usas en
    # `example_fr2.py` o `ris_hardware_server.py` para enviar el patrón:
    #
    # Ejemplo con el controlador local:
    # from linux_x86_64 import ext_metasurface_ctrl
    # ctrl = ext_metasurface_ctrl.MetasurfaceController(...)
    # ctrl.set_pattern(state_matrix)
    # =========================================================================
    return state_matrix


if __name__ == "__main__":
    # Ejemplo: RIS de 16x16 elementos (256 elementos) apuntando a 1 usuario
    Nx, Ny = 16, 16
    N = Nx * Ny

    # Canal simulado o medido hacia el usuario objetivo
    G_mock = np.ones((N, 1), dtype=complex)
    h_r_mock = np.exp(-1j * np.linspace(0, 4 * np.pi, N))

    opt = WMMSE_MM_Optimizer(num_ris_elements=N, num_tx_antennas=1, ris_bits=1)
    result = opt.optimize(G=G_mock, H_r=h_r_mock, method="scrpa")

    phases_2d = result["phases_deg"].reshape((Nx, Ny))
    apply_ris_configuration(phases_2d, n_bits=1)