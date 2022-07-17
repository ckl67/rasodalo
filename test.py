import os
os.environ['PYUSB_DEBUG'] = 'debug'
import usb.core
print(list(usb.core.find(find_all=True)))

