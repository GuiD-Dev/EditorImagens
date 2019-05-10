# encoding: utf-8

import tkinter as tk
from tkinter import messagebox as mbx
from PIL import Image as Img
import matplotlib.pyplot as plt
import collections as c
import math


class ImageControl:

    def searchImage(self):
        img = tk.filedialog.askopenfilename()
        self.image = Img.open(img).convert("L")
        self.divideSquares()


    def divideSquares(self):
        img = self.image
        width, height = img.size
        q1 = img.crop((0, 0, width//2, height//2))
        q2 = img.crop((width//2, 0, width, height//2))
        q3 = img.crop((0, height//2, width//2, height))
        q4 = img.crop((width//2, height//2, width, height))
        self.squares = {
                        'q1':(q1, (0, 0, width//2, height//2)),
                        'q2':(q2, (width//2, 0, width, height//2)),
                        'q3':(q3, (0, height//2, width//2, height)),
                        'q4':(q4, (width//2, height//2, width, height))
                       }


    def showHistogram(self, squares):
        e = self.calcStats(squares)

        plt.bar(list(e['his'].keys()), e['his'].values(), color='g')
        plt.ylabel('Frequência')
        plt.show()


    def showStats(self, squares):
        e = self.calcStats(squares)

        mbx.showinfo("Estatísticas",
                            "Média: %.2f" % e['med'] + "\n" +
                            "Moda: %.2f" % e['mod'] + "\n" +
                            "Mediana: %.2f" % e['mdn'] + "\n" +
                            "Variância: %.2f" % e['var']
                    )


    def calcStats(self, squares):
        pixels = self.getPixels(squares)

        media = sum(pixels) / len(pixels)

        ocorrencias = c.Counter(pixels)
        moda = ocorrencias.most_common(1)[0][0]

        pixels.sort()
        if len(pixels) % 2 == 0:
            mediana = (pixels[len(pixels)//2-1] + pixels[len(pixels)//2]) / 2
        else:
            mediana = pixels[len(pixels)//2]

        variancia = 0
        histograma = c.defaultdict(int)

        for p in pixels:
            variancia += (p - media) ** 2
            histograma[p] += 1

        variancia = variancia / len(pixels)

        for h in range(0,255):
            histograma[h] += 0
        
        return {'med':media, 'mod':moda, 'mdn':mediana, 'var':variancia, 'his':histograma}


    def countPixels(self, squares, halfValue):
        pixels = self.getPixels(squares)
        sup = 0
        inf = 0

        for p in pixels:
            if p > halfValue:
                sup += 1
            elif p < halfValue:
                inf += 1

        mbx.showinfo("Quantidade de Pixels", "Superiores a %d: %d" % (halfValue, sup) + "\n" +
                                             "Inferiores a %d: %d" % (halfValue, inf))


    def getPixels(self, squares):
        pixels = []

        for sq in squares:
            width, height = sq[0].size
            matrix = sq[0].load()

            for x in range(width):
                for y in range(height):
                    pixels.append(matrix[x,y])

        return pixels



    def reloadImage(self, squares, option):
        img = self.image.copy()
        width, height = img.size
        matrix = img.load()

        e = self.calcStats(squares)

        i = 0
        for sq in squares:
            i += 1
            for x in (x for x in range(sq[1][0], sq[1][2]) if x < sq[1][2]):
                for y in (y for y in range(sq[1][1], sq[1][3]) if y < sq[1][3]):

                    if option == 'a' and matrix[x,y] >= e['med']:
                        matrix[x,y] = 255
                    elif option == 'b' and matrix[x,y] >= e['mod']:
                        matrix[x,y] = 200
                    elif option == 'c' and matrix[x,y] >= e['mdn']:
                        matrix[x,y] = 220
                    elif option == 'd' and matrix[x,y] < e['med']:
                        matrix[x,y] = 100
                    elif option == 'e' and i == 1 and matrix[x,y] > e['med']:
                        matrix[x,y] = 0
                    elif option == 'e' and i == 2 and matrix[x,y] < e['mdn']:
                        matrix[x,y] = 255

        img.show()



    def invertImage(self):
        width, height = self.image.size

        img = self.image.copy()
        matrix = img.load()

        invImg = self.image.copy()
        invMatrix = invImg.load()

        for x in (x for x in range(width) if x < width):
            for y in (y for y in range(height) if y < height):
                invMatrix[x, y] = matrix[width - 1 - x, height - 1 - y]

        # invImg.show()
        self.image = invImg


    def mirrorImage(self):
        width, height = self.image.size

        img = self.image.copy()
        matrix = img.load()

        invertImg = self.image.copy()
        invertMatrix = invertImg.load()

        for x in (x for x in range(width) if x < width):
            for y in (y for y in range(height) if y < height):
                invertMatrix[x, y] = matrix[width - 1 - x, y]

        # invertImg.show()
        self.image = invertImg


    def rotateImage(self, angle):
        width, height = self.image.size
        matrix = self.image.load()

        rotImg = Img.new('L', self.image.size)
        rotMatrix = rotImg.load()

        deslocX = height - 1
        deslocY = width - 1

        rad = math.radians(angle)
        mat = { 'sin':math.sin(rad), 'cos':math.cos(rad) }

        if angle == 90:
            deslocX = 0
            deslocY = height - 1
        elif angle == 180:
            deslocX = height - 1
            deslocY = width - 1
        elif angle == 270:
            deslocX = width - 1
            deslocY = 0
        # else:
        #     mbx.showwarning("Atenção", "Valor do ângulo fora da faixa de valores válidos.")
        #     return

        # matrixTranf = [
        #     [ mat['cos'], -mat['sin'], 0 ],
        #     [ mat['sin'], mat['cos'], 0 ],
        #     [ deslocX, deslocY, 1 ]
        # ]

        z = 1
        for x in (x for x in range(width) if x < width):
            for y in (y for y in range(height) if y < height):
                    
                xNew = round((x * mat['cos']) + (y * mat['sin']) + width//2)
                yNew = round((x * -mat['sin']) + (y * mat['cos']) + height//2)
                # print(xNew, yNew)
                if xNew < width and yNew < height and xNew > -1 and yNew > -1:
                    rotMatrix[xNew, yNew] = matrix[x,y]

        # rotImg.show()
        self.image = rotImg


    def resizeImage(self, scalaX, scalaY):
        matrix = self.image.load()

        width = int(scalaX * self.image.size[0])
        height = int(scalaY * self.image.size[1])

        resImg = Img.new('L', (width, height))
        resMatrix = resImg.load()

        for xDest in (xDest for xDest in range(width) if xDest < width):
            x = xDest / scalaX

            for yDest in (yDest for yDest in range(height) if yDest < height):
                y = yDest / scalaY
                
                resMatrix[xDest, yDest] = matrix[x,y]

        # resImg.show()
        self.image = resImg


    # def fillBackground(self):

    #     for x in (x for x in range(width) if x < width):
    #         for y in (y for y in range(height) if y < height):