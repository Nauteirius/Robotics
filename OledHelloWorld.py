from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

# Inicjalizacja wyświetlacza
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 40), "Hello World", fill="white")