import time
from datetime import datetime

class PCF8591:
    def __init__(self, bus):
        self.i2cbus = bus

    def read(self):
        # i2cbus = SMBus(1)  # Create a new I2C bus
        i2caddress = 0x48  # Address of PCF8591 device
        self.i2cbus.write_byte(i2caddress, 0x00)
        self.i2cbus.read_byte(i2caddress)
        lux = self.i2cbus.read_byte(i2caddress)

        self.i2cbus.write_byte(i2caddress, 0x01)
        self.i2cbus.read_byte(i2caddress)
        tempture = self.i2cbus.read_byte(i2caddress)

        self.i2cbus.write_byte(i2caddress, 0x02)
        self.i2cbus.read_byte(i2caddress)
        value = self.i2cbus.read_byte(i2caddress)

        self.i2cbus.write_byte(i2caddress, 0x03)
        self.i2cbus.read_byte(i2caddress)
        ain3 = self.i2cbus.read_byte(i2caddress)

        return { "illumination": lux, "temperature": tempture, "time": datetime.utcnow() }