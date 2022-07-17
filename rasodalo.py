import usb.core

USB_idVendor = 0x10C4
USB_idProduct = 0xEA60


def connect():
    dev = usb.core.find(idVendor=0x10C4, idProduct=0xEA60)
    assert dev is not None
    print(dev)
    return dev

if __name__ == "__main__":
    import logroll
    import datetime
    import time

# connect Sound Level meter DEM202 over USB
dev = connect()