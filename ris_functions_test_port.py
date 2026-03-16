import os
import sys
import platform
import numpy as np

if os.name == 'nt':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'windows_x86_64'))
    from windows_x86_64 import RIS as HW_RIS
elif os.name == 'posix':
    if platform.machine() == 'aarch64':
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'linux_aarch64'))
        from linux_aarch64 import RIS as HW_RIS
    else:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'linux_x86_64'))
        from linux_x86_64 import RIS as HW_RIS

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
