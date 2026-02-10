import os
import sys
import numpy as np

base_path = os.path.dirname(__file__)
windows_path = os.path.join(base_path, "windows_x86_64")
if windows_path not in sys.path:
    sys.path.insert(0, windows_path)

if os.name == 'nt':
    # from windows_x86_64 import *
    from windows_x86_64 import RIS as HW_RIS
elif os.name == 'posix':
    from linux_x86_64 import RIS as HW_RIS

com = None #define or not the com port number which ris is connected to

ris = HW_RIS(com=com)

#turn on meatsurface
ris.on()
print(f"{ris.pixels = }")

# RIS pixels all to zeros
# configuration = [0] * 128
# ris.set_specified_states(configuration)

# Control RIS pixels independently by list[boolean]
configuration = [np.random.randint(2) for i in range(128)] # numpy has already been imported in package
# ris.set_specified_states(configuration)
print(f"random config applied")

# # Control RIS pixels independently by list[boolean]
# configuration = [np.random.randint(2) for i in range(128)] # numpy has already been imported in package
# ris.set_specified_states(configuration)
# print(f"random config applied")

# # Control RIS pixels by columns from bottom to top (see readme.md)
# configuration = [i//16  for i in range(32)]*4 #[0,0,..,0,1,1,...,1,0,0,...,0,1,1,...,1...]
# ris.set_specified_states(configuration)
# print(f"column_by_column config applied")

# #Control RIS pixels by rows from bottom to top (see readme.md)
# configuration = [i%2 for i in range(128)] # [0,1,0,1,0,1,...]
# ris.set_specified_states(configuration)
# print(f"Line_by_line config applied")

# # Run pixel by pixel optimization to generate configuration that gives the best S21
# # A signal feedback system is required (VNA recommended)
# callback_ris_apply_config = lambda config: ris.set_specified_states(config)
# callback_measurement_get_s21 = lambda: feedback_system.get_data() # <!> USER TO PROVIDE THIS FUNCTION TO RETURN POWER IN DB
# n_pixels = ris.pixels
# n_loops = 4 # number of optimization loops (recommended 10-15 loops)
# reference_optimization(callback_ris_apply_config,
#                         callback_measurement_get_s21,
#                         n_pixels,
#                         n_loops
#                         )
# print(f"reference optimization executed and data file has been saved")



#turn off metasurface
ris.off()
