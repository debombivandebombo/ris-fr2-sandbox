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
    from linux_x86_64 import *

com = None #define or not the com port number which ris is connected to

input("Press Enter to INSTANTIATE the RIS...")
ris = HW_RIS(com=com)

#turn on meatsurface
input("Press Enter to turn ON the RIS...")
ris.on()
print(f"{ris.pixels = }")

# RIS pixels all to zeros
input("Press Enter to APPLY ALL ZEROS CONFIGURATION...")
configuration = [0] * 3200
ris.set_specified_states(configuration)

# Control RIS pixels independently by list[boolean]
input("Press Enter to APPLY RANDOM CONFIGURATION...")
configuration = [np.random.randint(2) for i in range(3200)] # numpy has already been imported in package
ris.set_specified_states(configuration)
print(f"random config applied")

# Turn off the RIS
input("Press Enter to turn OFF the RIS...")
ris.off()
