#!/usr/bin/python3
from time import sleep

import board
import neopixel
import os

ignored_pixels = 15
v_pixels = 9
h_pixels = 15
Nr_Of_Pixels = 150
pixels = neopixel.NeoPixel(board.D18, Nr_Of_Pixels, auto_write=False, brightness=1)
pixels.fill((0, 0, 0))


def readbitmap(filename):
    bitmap = {}
    with open(filename, 'rb') as bmpfile:
        bitmap['ID'] = bmpfile.read(2).decode('utf-8')
        bitmap['size'] = int(bmpfile.read(4).hex().rstrip("0"), 16)
        bitmap['reserved1'] = bmpfile.read(2).decode('utf-8').strip()
        bitmap['reserved2'] = bmpfile.read(2).decode('utf-8').strip()
        bitmap['pixelarray_offset'] = int(bmpfile.read(4).hex().rstrip('0'), 16)
        bmpfile.seek(0)
        bmpfile.seek(18)
        bitmap['width'] = int(bmpfile.read(4).hex().rstrip("0"), 16)
        bitmap['padding'] = 4 - bitmap['width'] % 4
        bmpfile.seek(0)
        bmpfile.seek(bitmap['pixelarray_offset'])
        bitmap['pixelarray'] = bmpfile.read()
        count = 0
        ledaddr = ignored_pixels + 1
        bitmap['pixels'] = []
        bmpfile.seek(bitmap['pixelarray_offset'], 1)
        while count <= Nr_Of_Pixels:
            r_val = 0
            g_val = 0
            b_val = 0
            try:
                b_val = bitmap['pixelarray'][(count * 3)]
                r_val = bitmap['pixelarray'][(count * 3) + 1]
                g_val = bitmap['pixelarray'][(count * 3) + 2]
                if (count + 1) % (h_pixels + bitmap['padding']) != 0 or count == 0:
                    bitmap['pixels'].append((r_val, g_val, b_val))
                    ledaddr = ledaddr + 1
                count = count + 1
            except Exception as e:
                break
    pixelvalues = bitmap['pixels']
    pixelvalues.reverse()
    row = 1
    pix_ordered = []
    while row <= v_pixels:
        pixels_startrng = h_pixels * row
        pixels_endrng = pixels_startrng + h_pixels
        pixelvalues_startrng = len(pixelvalues) - (h_pixels * row)
        pixelvalues_endrng = pixelvalues_startrng + h_pixels
        pix_ordered[pixels_startrng:pixels_endrng] = pixelvalues[pixelvalues_startrng:pixelvalues_endrng]
        row = row + 1
    return pix_ordered


def loopimages():
    while True:
        for file in os.listdir("images"):
            pixels[ignored_pixels:] = readbitmap("images/" + str(file))
            pixels.write()
            sleep(1)


def kloppend_hart():
    while True:
        pixels[ignored_pixels:] = readbitmap(os.path.dirname(os.path.abspath(__file__)) + "/images/hartje.bmp")
        pixels.write()
        sleep(1)
        pixels[ignored_pixels:] = readbitmap(os.path.dirname(os.path.abspath(__file__)) + "/images/hartje_groot.bmp")
        pixels.write()
        sleep(0.25)
        pixels[ignored_pixels:] = readbitmap(os.path.dirname(os.path.abspath(__file__)) + "/images/hartje.bmp")
        pixels.write()
        sleep(0.25)
        pixels[ignored_pixels:] = readbitmap(os.path.dirname(os.path.abspath(__file__)) + "/images/hartje_groot.bmp")
        pixels.write()
        sleep(0.25)


if __name__ == "__main__":
    kloppend_hart()
