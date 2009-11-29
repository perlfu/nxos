import usb
import time

USB_BULK_OUT_EP = 0x1
USB_BULK_IN_EP = 0x82

def get_device(vendor_id, product_id, version=0, timeout=None):
    """Return the first device matching the given vendor/product ID."""
    while True:
        dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        if dev is not None:
            return UsbBrick(dev)
        if timeout is None or timeout <= 0:
            return None
        sleep_time = min(1.0, timeout)
        time.sleep(sleep_time)
        timeout -= sleep_time

class UsbBrick(object):
    def __init__(self, dev):
        self._dev = dev

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def open(self, interface, configuration=1):
        self._iface = interface
        self._config = configuration
        self._dev.set_configuration(configuration=self._config)

    def close(self):
        del self._dev

    def read(self, size, timeout = 100):
        """Read the given amount of data from the device and return it."""
        # For some reason, bulkRead returns a tuple of longs. This is
        # dumb, so we convert it back to a string before returning,
        # kthx.
        try:
            data = self._dev.read(USB_BULK_IN_EP, size, self._iface, timeout)
        except usb.USBError:
            return None
        return ''.join(chr(x) for x in data)

    def write(self, data, timeout = 100):
        """Write the given amount of data to the device."""
        return self._dev.write(USB_BULK_OUT_EP, data, self._iface, timeout)
