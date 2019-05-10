# encoding: utf-8

import tkinter as tk
import ImageControl as ICtl
from PIL import ImageTk as ITk


class AppUI:

    def __init__(self):
        self.initWindow()
        self.initMenus()
        self.icontrol = ICtl.ImageControl()
        self.root.mainloop()


    def initWindow(self):
        window = tk.Tk()
        window.title("Projeto de Imagens")
        w = 700
        h = 550
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.root = window


    def initMenus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu = menubar)
        menubar.add_command(label="Buscar Imagem", command = lambda: self.loadImage())
        menubar.add_command(label="Recarregar Imagem", command = lambda: self.loadImage(False))

        subMenuStats = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Estatísticas", menu=subMenuStats)
        subMenuStats.add_command(label="Histograma Quadrante 1", command = lambda: self.icontrol.showHistogram([self.icontrol.squares['q1']]))
        subMenuStats.add_command(label="Quadrante 2", command = lambda: self.icontrol.showStats([self.icontrol.squares['q2']]))
        subMenuStats.add_command(label="Quadrante 3", command = lambda: self.icontrol.showStats([self.icontrol.squares['q3']]))
        subMenuStats.add_command(label="Quadrante 4", command = lambda: self.icontrol.showStats([self.icontrol.squares['q4']]))
        subMenuStats.add_command(label="Quadrante 1 e 2", command = lambda: self.icontrol.showStats([self.icontrol.squares['q1'], self.icontrol.squares['q2']]))
        subMenuStats.add_command(label="Calcular Pixels metade superior",
                                command = lambda: self.icontrol.countPixels([self.icontrol.squares['q1'], self.icontrol.squares['q2']], 100))
        subMenuStats.add_command(label="Calcular Pixels metade inferior",
                                command = lambda: self.icontrol.countPixels([self.icontrol.squares['q1'], self.icontrol.squares['q2']], 150))

        subMenuTransf = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Alterar Pixels", menu=subMenuTransf)
        subMenuTransf.add_command(label="Quadrante 2", command = lambda: self.icontrol.reloadImage([self.icontrol.squares['q2']], 'a'))
        subMenuTransf.add_command(label="Quadrante 4", command = lambda: self.icontrol.reloadImage([self.icontrol.squares['q4']], 'b'))
        subMenuTransf.add_command(label="Quadrante 3", command = lambda: self.icontrol.reloadImage([self.icontrol.squares['q3']], 'c'))
        subMenuTransf.add_command(label="Quadrante 2", command = lambda: self.icontrol.reloadImage([self.icontrol.squares['q2']], 'd'))
        subMenuTransf.add_command(label="Quadrante 2 e 3", command = lambda: self.icontrol.reloadImage([self.icontrol.squares['q2'], self.icontrol.squares['q3']], 'e'))

        menubar.add_command(label="Rotacionar", command = lambda: self.inputAngle())

        menubar.add_command(label="Espelhar", command = lambda: self.mirrorImage())

        menubar.add_command(label="Inverter", command = lambda: self.invertImage())

        menubar.add_command(label="Redimencionar", command = lambda: self.inputEscales())


    def loadImage(self, searchMode = True):
        if searchMode:
            self.icontrol.searchImage()
        else:
            self.lblImage.destroy()

        img = ITk.PhotoImage(self.icontrol.image)
        self.lblImage = tk.Label(self.root, image = img)
        self.lblImage.image = img
        self.lblImage.pack()

    
    def inputAngle(self):
        window = tk.Toplevel(self.root)

        label = tk.Label(window, text = "Insira o valor do ângulo: (90, 180, 270)")
        label.pack()

        entry = tk.Entry(window)
        entry.focus_set()
        entry.pack()

        self.lblImage.destroy()

        button = tk.Button(window, text = 'OK', command = lambda: self.icontrol.rotateImage(int(entry.get())))
        button.pack()


    def mirrorImage(self):
        self.lblImage.destroy()
        self.icontrol.mirrorImage()


    def invertImage(self):
        self.icontrol.invertImage()
        self.lblImage.destroy()

        


    def inputEscales(self):
        window = tk.Toplevel(self.root)

        label = tk.Label(window, text = "Insida o valor das escalas X e Y")
        label.pack()

        entryX = tk.Entry(window)
        entryX.focus_set()
        entryX.pack()

        entryY = tk.Entry(window)
        entryY.pack()

        self.lblImage.destroy()

        button = tk.Button(window, text = 'OK', command = lambda: self.icontrol.resizeImage(float(entryX.get()), float(entryY.get())))
        button.pack()