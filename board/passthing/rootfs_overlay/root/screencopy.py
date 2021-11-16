#!/usr/bin/env python2

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306 as pgdisplay
from luma.core.render import canvas

from curses import panel
import subprocess
from PIL import Image, ImageDraw

from luma.core.sprite_system import framerate_regulator
serial = i2c(port=1, address=0x3C)
dev = pgdisplay(serial, width=128, height=32)

def fbcopy():
    global dev
    size = [min(*dev.size)] * 2
    posn = ((dev.width - size[0]) // 2, dev.height - size[1])
    
    subprocess.call('fbcat > /tmp/scrdmp.ppm', shell=True)
    im = Image.open('/tmp/scrdmp.ppm')
    dev.display(im.convert(dev.mode, dither=0))

if __name__ == "__main__":
    regulator = framerate_regulator(fps=10)
    while True:
        with regulator:
            fbcopy()

