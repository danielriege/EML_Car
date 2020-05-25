#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageEnhance
import random
import numpy as np
import matplotlib.pyplot as plt

kelvin_table = {
    5300: (255, 233, 217),
    5400: (255, 235, 220),
    5500: (255, 236, 224),
    5600: (255, 238, 227),
    5700: (255, 239, 230),
    5800: (255, 240, 233),
    5900: (255, 242, 236),
    6000: (255, 243, 239),
    6100: (255, 244, 242),
    6200: (255, 245, 245),
    6300: (255, 246, 247),
    6400: (255, 248, 251),
    6500: (255, 249, 253),
    6600: (254, 249, 255),
    6700: (252, 247, 255),
    6800: (249, 246, 255),
    6900: (247, 245, 255),
    7000: (245, 243, 255),
    7100: (243, 242, 255),
    7200: (240, 241, 255),
    7300: (239, 240, 255),
    7400: (237, 239, 255),
    7500: (235, 238, 255),
    7600: (233, 237, 255),
    7700: (231, 236, 255),
    7800: (230, 235, 255),
    7900: (228, 234, 255),
    8000: (227, 233, 255),
    8100: (225, 232, 255),
    8200: (224, 231, 255),
    8300: (222, 230, 255),
    8400: (221, 230, 255),
    8500: (220, 229, 255),
    8600: (218, 229, 255),
    8700: (217, 227, 255),
    8800: (216, 227, 255),
    8900: (215, 226, 255),
    9000: (214, 225, 255),
    9100: (212, 225, 255),
    9200: (211, 224, 255),
    9300: (210, 223, 255),
    9400: (209, 223, 255),
    9500: (208, 222, 255),
    9600: (207, 221, 255),
    9700: (207, 221, 255),
    9800: (206, 220, 255),
    9900: (205, 220, 255)}
def box(x,y,radius):
    ux = (x-radius)
    uy = (y-radius)
    lx = (x+radius)
    ly = (y+radius)
    return (ux,uy,lx,ly)
def addTemperatureToImg(img, temp):
    color = kelvin_table[temp]
    r, g, b = color
    color_matrix = (r / 255.0, 0.0, 0.0, 0.0, 0.0, g / 255.0, 0.0, 0.0, 0.0, 0.0, b / 255.0, 0.0)
    return img.convert('RGB', color_matrix)
def generateRandomImage():
    radius = random.randrange(10,25,1)
    angle = random.randrange(1000,2000,1)
    x = ((angle / 1000)-1)*640
    y = random.randrange(120,360,1)
    temperature = random.randrange(5300,9900,100)
    brightness_factor = random.randrange(40,100)/100

    img = Image.new('RGB', (640, 480), color = 'white')

    d = ImageDraw.Draw(img)

    d.ellipse(xy=box(x,y,radius), fill=(0,0,0), outline=(0,0,0))
    #image brightness enhancer
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness_factor)

    img = addTemperatureToImg(img, temperature)
    return (img, angle)
if __name__ == "__main__":
    image, angle = generateRandomImage()
    npimage = np.asarray(image)
    plt.title("%f" % (angle))
    plt.imshow(image)
    plt.show()
