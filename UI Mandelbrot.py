__author__ = 'Nate St. George'

import pyforms
from   pyforms          import BaseWidget
from   pyforms.Controls import ControlSlider
from   pyforms.Controls import ControlButton
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlNumber
from   pyforms.Controls import ControlCheckBox

import time
import random

from PIL import Image

class UI(BaseWidget):
    def __init__(self):
        BaseWidget.__init__(self, "Mandelbrot Set Generator")

        self._redSlider            = ControlSlider(label="Red", min=0, max=255)
        self._blueSlider           = ControlSlider(label="Blue", min=0, max=255)
        self._greenSlider          = ControlSlider(label="Green", min=0, max=255)

        self._redSliderTwo         = ControlSlider(label="Red 2", defaultValue=255, min=0, max=255)
        self._blueSliderTwo        = ControlSlider(label="Blue 2", defaultValue=255, min=0, max=255)
        self._greenSliderTwo       = ControlSlider(label="Green 2", defaultValue=255, min=0, max=255)

        self._randomizeFirstColor  = ControlCheckBox(label='Randomize First Color?')
        self._randomizeFirstColor.value = True
        self._randomizeSecondColor = ControlCheckBox(label="Randomize Second Color?")
        self._randomizeSecondColor.value = True
        self._randomizeBrightness  = ControlCheckBox(label="Randomize Brightness?")

        self._brightnessSlider     = ControlSlider(label="Brightness", defaultValue=255, min=0, max=255)

        self._xSlider              = ControlText(label="X", defaultValue="-1.0")
        self._ySlider              = ControlText(label="Y", defaultValue="0")

        self._zoomSlider           = ControlNumber(label="Zoom", defaultValue=1, min=1, max=1000000)

        self._entropySlider        = ControlSlider(label="Entropy", defaultValue=5000, min=100, max=100000)

        self._randomPreviewButton  = ControlButton(label="Smart Randomize and Generate Preview")
        self._randomPreviewButton.value = self.randomPreviewAction

        self._previewButton        = ControlButton(label="Generate Preview (120x120)")
        self._previewButton.value = self.previewAction

        self._generateButton       = ControlButton(label="Generate (500x500)")
        self._generateButton.value = self.generateAction

        self._exportButton         = ControlButton(label="Export For Desktop (2049x1153)")
        self._exportButton.value   = self.exportAction

        self._fourKExportButton    = ControlButton(label="Export at 4K UHD (3840x2160)")
        self._fourKExportButton.value = self.fourKExportAction

        self._phoneExportButton    = ControlButton(label="Export for Phone (1080x1920)")
        self._phoneExportButton.value = self.phoneExportAction

        self._randomButton         = ControlButton(label="Randomize")
        self._randomButton.value = self.randomAction

        self._formset = [
            (('_redSlider', '_greenSlider', '_blueSlider'),"=", ('_redSliderTwo', '_greenSliderTwo', '_blueSliderTwo'), '=', '           ', '_randomizeFirstColor', '_randomizeSecondColor', '_randomizeBrightness', '|', '_brightnessSlider', "=", '_entropySlider', '_xSlider', '_ySlider', '_zoomSlider', "=", '_randomButton', '_randomPreviewButton', '_previewButton', '_generateButton', '_exportButton', '_fourKExportButton', '_phoneExportButton')
        ]

    def previewAction(self):
        global xsize
        global ysize
        global max_iteration
        max_iteration = 200
        xsize = 120
        ysize = 120

        self.makeImage()

    def generateAction(self):
        global xsize
        global ysize
        global max_iteration
        max_iteration = 500
        xsize = 500
        ysize = 500

        self.makeImage()

    def exportAction(self):
        global xsize
        global ysize
        global max_iteration
        max_iteration = 500
        xsize = 1366*2
        ysize = 1366*2
        x_center = float(self._xSlider.value)
        y_center =  float(self._ySlider.value)

        redStep = int(abs(self._redSlider.value - self._redSliderTwo.value) / 255);
        greenStep = int(abs(self._greenSlider.value - self._greenSliderTwo.value) / 255);
        blueStep = int(abs(self._blueSlider.value - self._blueSliderTwo.value) / 255);

        im = Image.new("RGB", (xsize,ysize))

        for i in xrange(xsize):                                                         # Thanks to http://rosettacode.org/wiki/Mandelbrot_set#Python
            for j in xrange(ysize):
                x,y = ( x_center + (4.0/self._zoomSlider.value)*float(i-xsize/2)/xsize,
                          y_center + (4.0/self._zoomSlider.value)*float(j-ysize/2)/ysize
                        )

                a,b = (0.0, 0.0)
                iteration = 0

                while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                    a,b = a**2 - b**2 + x, 2*a*b + y
                    iteration += 1
                if iteration == max_iteration:
                    color_value = 255
                else:
                    color_value = iteration*10 % 255
                # im.putpixel( (i,j), (color_value+self._redSlider.value-(255-self._brightnessSlider.value), color_value+self._greenSlider.value-(255-self._brightnessSlider.value), color_value+self._blueSlider.value-(255-self._brightnessSlider.value)))
                im.putpixel( (i, j), (colorFinder(self._redSlider.value, self._redSliderTwo.value, color_value), colorFinder(self._greenSlider.value, self._greenSliderTwo.value, color_value), colorFinder(self._blueSlider.value, self._blueSliderTwo.value, color_value)))
                im.resize((2049, 2049), Image.ANTIALIAS)
                im.crop(0, 448, 2049, 1600)
                im.save("/root/Documents/Fractals/fractal"+str(time.time()), "JPEG", quality=95)
                im.show(title="Generated Set")


    def fourKExportAction(self):
        global xsize
        global ysize
        global max_iteration
        max_iteration = 500
        xsize = int(3840*1.2)
        ysize = int(3840*1.2)
        x_center = float(self._xSlider.value)
        y_center =  float(self._ySlider.value)

        redStep = int(abs(self._redSlider.value - self._redSliderTwo.value) / 255);
        greenStep = int(abs(self._greenSlider.value - self._greenSliderTwo.value) / 255);
        blueStep = int(abs(self._blueSlider.value - self._blueSliderTwo.value) / 255);

        im = Image.new("RGB", (xsize,ysize))

        for i in xrange(xsize):                                                         # Thanks to http://rosettacode.org/wiki/Mandelbrot_set#Python
            for j in xrange(ysize):
                x,y = ( x_center + (4.0/self._zoomSlider.value)*float(i-xsize/2)/xsize,
                          y_center + (4.0/self._zoomSlider.value)*float(j-ysize/2)/ysize
                        )

                a,b = (0.0, 0.0)
                iteration = 0

                while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                    a,b = a**2 - b**2 + x, 2*a*b + y
                    iteration += 1
                if iteration == max_iteration:
                    color_value = 255
                else:
                    color_value = iteration*10 % 255
                # im.putpixel( (i,j), (color_value+self._redSlider.value-(255-self._brightnessSlider.value), color_value+self._greenSlider.value-(255-self._brightnessSlider.value), color_value+self._blueSlider.value-(255-self._brightnessSlider.value)))
                im.putpixel( (i, j), (colorFinder(self._redSlider.value, self._redSliderTwo.value, color_value), colorFinder(self._greenSlider.value, self._greenSliderTwo.value, color_value), colorFinder(self._blueSlider.value, self._blueSliderTwo.value, color_value)))


        im = im.resize((3840, 3840), Image.ANTIALIAS)
        im = im.crop((0, 0, 3840, 2160))
        im.save("/root/Documents/Fractals/fractal"+str(time.time()), "JPEG", quality=95)
        im.show(title="Generated Set")

    def phoneExportAction(self):
        global xsize
        global ysize
        global max_iteration
        max_iteration = 500
        xsize = int(1920*1.2)
        ysize = int(1920*1.2)
        x_center = float(self._xSlider.value)
        y_center =  float(self._ySlider.value)

        redStep = int(abs(self._redSlider.value - self._redSliderTwo.value) / 255);
        greenStep = int(abs(self._greenSlider.value - self._greenSliderTwo.value) / 255);
        blueStep = int(abs(self._blueSlider.value - self._blueSliderTwo.value) / 255);

        im = Image.new("RGB", (xsize,ysize))

        for i in xrange(xsize):                                                         # Thanks to http://rosettacode.org/wiki/Mandelbrot_set#Python
            for j in xrange(ysize):
                x,y = ( x_center + (4.0/self._zoomSlider.value)*float(i-xsize/2)/xsize,
                          y_center + (4.0/self._zoomSlider.value)*float(j-ysize/2)/ysize
                        )

                a,b = (0.0, 0.0)
                iteration = 0

                while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                    a,b = a**2 - b**2 + x, 2*a*b + y
                    iteration += 1
                if iteration == max_iteration:
                    color_value = 255
                else:
                    color_value = iteration*10 % 255
                # im.putpixel( (i,j), (color_value+self._redSlider.value-(255-self._brightnessSlider.value), color_value+self._greenSlider.value-(255-self._brightnessSlider.value), color_value+self._blueSlider.value-(255-self._brightnessSlider.value)))
                im.putpixel( (i, j), (colorFinder(self._redSlider.value, self._redSliderTwo.value, color_value), colorFinder(self._greenSlider.value, self._greenSliderTwo.value, color_value), colorFinder(self._blueSlider.value, self._blueSliderTwo.value, color_value)))

        im = im.resize((2970, 2970), Image.ANTIALIAS)
        im = im.crop((675, 0, 2295, 2970))
        im.save("/root/Documents/Fractals/fractal"+str(int(time.time()))+".jpg", "JPEG", quality=95)
        im.show(title="Generated Set")

    def randomAction(self):
        self._redSlider.value = int(float(random.random())*255)
        self._greenSlider.value = int(float(random.random())*255)
        self._blueSlider.value = int(float(random.random())*255)

        self._xSlider.value = str(float(random.random())*4)
        self._ySlider.value = str(float(random.random())*4)

        self._zoomSlider.value = int(float(random.random())*60)
        self._brightnessSlider.value = int(float(random.random())*255)

    def randomPreviewAction(self):
        done = False
        while not done:
            if self._randomizeFirstColor.value:
                self._redSlider.value = int(float(random.random())*255)
                self._greenSlider.value = int(float(random.random())*255)
                self._blueSlider.value = int(float(random.random())*255)

            if self._randomizeSecondColor.value:
                self._redSliderTwo.value = int(float(random.random())*255)
                self._greenSliderTwo.value = int(float(random.random())*255)
                self._blueSliderTwo.value = int(float(random.random())*255)

            self._xSlider.value = str(float(random.random())*4)
            self._ySlider.value = str(float(random.random())*4)

            self._zoomSlider.value = int(20+float(random.random())*self._entropySlider.value)
            if self._randomizeBrightness.value:
                self._brightnessSlider.value = int(float(random.random())*255)

            global xsize
            global ysize
            global max_iteration
            max_iteration = 200
            xsize = 128
            ysize = 128

            x_center = float(self._xSlider.value)
            y_center =  float(self._ySlider.value)

            redStep = (self._redSliderTwo.value - self._redSlider.value) / 255
            greenStep = (self._greenSliderTwo.value - self._greenSlider.value)/ 255
            blueStep = (self._blueSliderTwo.value - self._blueSlider.value) / 255

            im = Image.new("RGB", (xsize,ysize))

            colorValueArray = []
            colorCount = 0
            colorRatio = False

            for i in xrange(xsize):                                                         # Thanks to http://rosettacode.org/wiki/Mandelbrot_set#Python
                for j in xrange(ysize):
                    x,y = ( x_center + (4.0/self._zoomSlider.value)*float(i-xsize/2)/xsize,
                              y_center + (4.0/self._zoomSlider.value)*float(j-ysize/2)/ysize
                          )

                    a,b = (0.0, 0.0)
                    iteration = 0

                    while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                        a,b = a**2 - b**2 + x, 2*a*b + y
                        iteration += 1

                    if iteration == max_iteration:
                        color_value = 255
                    else:
                        color_value = iteration*10 % 255

                    if len(colorValueArray) == 0:
                        colorValueArray.append(color_value)

                    for color in colorValueArray:   # I wrote all this code, and it works. Despite these facts, I have not the slightest clue why.
                        if color_value != color:
                            colorValueArray.append(color_value)
                            break

                    # im.putpixel( (i,j), ((color_value+self._redSlider.value)-abs(self._redSliderTwo.value-self._brightnessSlider.value), (color_value+self._greenSlider.value)-abs(self._greenSliderTwo.value-self._brightnessSlider.value), (color_value+self._blueSlider.value)-abs(self._blueSliderTwo.value-self._brightnessSlider.value)))
                    # im.putpixel( (i, j), (int(self._redSlider.value+(redStep*color_value)-abs(255-self._brightnessSlider.value)), int(self._greenSlider.value+(greenStep*color_value)-abs(255-self._brightnessSlider.value)), int(self._blueSlider.value+(blueStep*color_value)-abs(255-self._brightnessSlider.value))))
                    im.putpixel( (i, j), (colorFinder(self._redSlider.value, self._redSliderTwo.value, color_value), colorFinder(self._greenSlider.value, self._greenSliderTwo.value, color_value), colorFinder(self._blueSlider.value, self._blueSliderTwo.value, color_value)))


            if not len(colorValueArray) <= 600: # THERE MUST BE A BETTER WAY TO DO THIS!
                colorChecker = 0
                colorCheckerTwo = 0
                while colorChecker <= 255:
                    while colorCheckerTwo <= 255:
                        colorAmount = colorValueArray.count(colorChecker)
                        colorAmount += colorValueArray.count(colorCheckerTwo)
                        if colorAmount > (len(colorValueArray)/2.5):    # Change the 2.5 value to adjust the parameter for what is considered interesting. For example, if you want it to ignore any image where two colors take up more than 75% of the image, change /2.5 to *.75
                            colorRatio = True
                            break
                        else:
                            colorCheckerTwo += 1
                    colorChecker += 1
                if colorRatio == False:
                    print("Done. There were "+str(len(colorValueArray))+" colors.")
                    done = True
                    im.show(title="Generated Set")

    def makeImage(self):
        global xsize
        global ysize
        global max_iteration
        x_center = float(self._xSlider.value)
        y_center =  float(self._ySlider.value)

        im = Image.new("RGB", (xsize,ysize))
        for i in xrange(xsize):                                                         # Thanks to http://rosettacode.org/wiki/Mandelbrot_set#Python
            for j in xrange(ysize):
                x,y = ( x_center + (4.0/self._zoomSlider.value)*float(i-xsize/2)/xsize,
                          y_center + (4.0/self._zoomSlider.value)*float(j-ysize/2)/ysize
                        )

                a,b = (0.0, 0.0)
                iteration = 0

                while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                    a,b = a**2 - b**2 + x, 2*a*b + y
                    iteration += 1
                if iteration == max_iteration:
                    color_value = 255
                else:
                    color_value = iteration*10 % 255

                # im.putpixel( (i,j), (color_value+self._redSlider.value-(self._redSliderTwo.value-self._brightnessSlider.value), color_value+self._greenSlider.value-(self._greenSliderTwo.value-self._brightnessSlider.value), color_value+self._blueSlider.value-(self._blueSliderTwo.value-self._brightnessSlider.value)))
                im.putpixel( (i, j), (colorFinder(self._redSlider.value, self._redSliderTwo.value, color_value)-(255-self._brightnessSlider.value), colorFinder(self._greenSlider.value, self._greenSliderTwo.value, color_value)-(255-self._brightnessSlider.value), colorFinder(self._blueSlider.value, self._blueSliderTwo.value, color_value)-(255-self._brightnessSlider.value)))

        im.show(title="Generated Set")

def colorFinder(c1, c2, stage):
    step = float(abs(float(c1)-float(c2))/255)
    c1 = 255-c1
    c2 = 255-c2

    if c1 < c2:
        return int(c1+(step*stage))
    else:
        return int(255-(c2+(step*stage)))


if __name__ == "__main__": pyforms.startApp(UI)