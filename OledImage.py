from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

# Inicjalizacja wyświetlacza
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# Wczytanie obrazu z pliku i przeskalowanie do wymiarów 128x64 pikseli
image = Image.open('nazwa_pliku.png').convert('1')
image = image.resize((128, 64))

# Wyświetlenie obrazu na ekranie
device.display(image)