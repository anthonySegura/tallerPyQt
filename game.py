import sys
import os
import time
import random
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from gridLayout import Ui_MainWindow

class Game():
    def __init__(self, n_filas, n_columnas, jugador_1, jugador_2):
        self.n_filas = n_filas
        self.n_columnas = n_columnas
        self.jugador_1 = jugador_1
        self.jugador_2 = jugador_2
        # Lista los archivos dentro de la carpeta cards
        self.cartas = os.listdir('cards')
        self.matrizBotones = []
        self.cartasSeleccionadas = []
        self.jugadores = [self.jugador_1, self.jugador_2]
        self.n_movimiento = 0
        # Ventaja del juego
        self.window = Ui_MainWindow()
        
    def init(self):
        self.agregarCartas()

    def agregarCartas(self):
        ancho = self.window.centralwidget.frameGeometry().width()
        alto = self.window.centralwidget.frameGeometry().height()
        for i in range(self.n_filas):
            self.matrizBotones.append([])
            for j in range(self.n_columnas):
                boton = QtWidgets.QPushButton()
                # boton.setIcon(QIcon(QPixmap('back.png')))
                # boton.setIconSize(QSize(75, 75))
                boton.setStyleSheet("QPushButton{background-image: url('back.png'); border: none; width: 100px; height: 100px;}")
                # Evento de cada boton
                boton.clicked.connect(lambda checked, arg=(i, j): self.click(*arg))
                # Se agrega el boton al layout de la ventana
                self.window.gridLayout.addWidget(boton, i, j)
                # Se agrega el boton a la matriz
                self.matrizBotones[i].append({'btn': boton, 'imagen': random.choice(self.cartas), 'emparejada': False})

    def click(self, fila, columna):
        boton = self.matrizBotones[fila][columna]
        if boton['emparejada']:
            return
        # Se muestra la imagen de la carta
        # boton['btn'].setIcon(QIcon(QPixmap('cards/{}'.format(boton['imagen']))))
        boton['btn'].setStyleSheet("QPushButton{background-image: url('{}');}".format(boton['imagen']))
        self.cartasSeleccionadas.append(boton)    

        if len(self.cartasSeleccionadas) > 2:
            if self.compararSeleccionadas():
                QMessageBox.information(self.window.centralwidget, '', 'Son iguales')
                self.cartasSeleccionadas[0]['emparejada'] = True
                self.cartasSeleccionadas[1]['emparejada'] = True
            self.ocultarCartas()         
        
    def compararSeleccionadas(self):
        return self.cartasSeleccionadas[0]['imagen'] == self.cartasSeleccionadas[1]['imagen']        

    def ocultarCartas(self):
        for i in range(self.n_filas):
            for j in range(self.n_columnas):
                if not self.matrizBotones[i][j]['emparejada']:
                    self.matrizBotones[i][j]['btn'].setIcon(QIcon(QPixmap('back.png')))
        self.cartasSeleccionadas = []        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # Instancia del juego      
    game = Game(3, 3, 'Freddy', 'Michael')
    ui = game.window
    ui.setupUi(MainWindow)
    game.init()
    MainWindow.show()
    sys.exit(app.exec_())