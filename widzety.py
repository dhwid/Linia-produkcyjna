#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from gui import Ui_Widget
from PyQt5 import QtCore, QtGui
import math
import random

EMPTY_STRING = "                   "

ABOUT = "Zadaniem dyspozytora jest sterowanie prędkością obrotową silników tak aby\n " \
        "nie doprowadzić do ich przegrzania. Do swojej dyspozycji ma on dwa suwaki,\n jeden służy do zwiększania " \
        "obrotów silnika, drugi do zwiększania obrotów układu chłodzenia,\ndzięki czemu można kontrolować temperatury."

def showdialog():
    msg = QMessageBox()
    # msg.setIcon(QMessageBox.Information)

    # msg.setText("This is a message box")
    # msg.setInformativeText("This is additional information")
    msg.setWindowTitle("O programie")
    msg.setText(ABOUT)


    retval = msg.exec_()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zadania = Zadania()
        self.setCentralWidget(self.zadania)

        menubar = self.menuBar()
        menubar.setFont(QtGui.QFont("Cantarell", 14, QtGui.QFont.Light))
        fileMenu = menubar.addMenu('Pomoc')
        fileMenu.setFont(QtGui.QFont("Cantarell", 12, QtGui.QFont.Light))

        fileMenu.addAction("O programie")
        # fileMenu.triggered.connect(QMessageBox.information(self, 'Błąd',
        #                         'Pusty login lub hasło!', QMessageBox.Ok))

        fileMenu.triggered.connect(showdialog)

    # def newCall(self, QDialog):
    #     def __init__(self, parent=None):
    #         super(self).__init__(parent)
    #
    #         # etykiety, pola edycyjne i przyciski ###
    #         loginLbl = QtGui.QLabel('Login')
    #         self.setModal(True)

class Zadania(QWidget, Ui_Widget):

    def __init__(self, parent=None):
        super(Zadania, self).__init__(parent)
        self.menuBar = QtGui
        self.setupUi(self)

        self.counter = 0
        self.t1 = 0
        self.actualTemp1 = 0
        self.t2 = 0
        self.actualTemp2 = 0

        self.obrotySilnika1 = 0
        self.obrotySilnika2 = 0
        self.temp1 = 0
        self.temp2 = 0

        self.obrotyCoolera1 = 1
        self.obrotyCoolera2 = 1
        self.jestBlad1 = False
        self.jestBlad2 = False

        # Sygnaly
        self.suwak.valueChanged.connect(self.wartoscSilnik1)
        self.suwak1.valueChanged.connect(self.wartoscCooler1)
        self.kasujBledy1.clicked.connect(self.kasowanieBledow1)
        self.suwak2.valueChanged.connect(self.wartoscSilnik2)
        self.suwak3.valueChanged.connect(self.wartoscCooler2)
        self.kasujBledy2.clicked.connect(self.kasowanieBledow2)

        # Timer
        self.timer = QtCore.QBasicTimer()
        self.speed = 100
        self.timer.start(self.speed, self)

    def wartoscSilnik1(self, wartosc):
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotySilnika1 = wartosc / 4
        self.lcd.setText(str(wartosc))

    def wartoscCooler1(self, wartosc):
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotyCoolera1 = (wartosc / 50) + 1
        self.lcd1.setText(str(wartosc))

    def wartoscSilnik2(self, wartosc):
        self.counter = 0
        self.actualTemp2 = self.temp2
        self.t2 = 0
        self.obrotySilnika2 = wartosc / 4
        self.lcd2.setText(str(wartosc))

    def wartoscCooler2(self, wartosc):
        self.counter = 0
        self.actualTemp2 = self.temp2
        self.t2 = 0
        self.obrotyCoolera2 = (wartosc / 50) + 1
        self.lcd3.setText(str(wartosc))

    def obliczTemperature(self, temp, actualTemp, t, obrotySilnika, obrotyCoolera):

        if (t < 3.5):
            t += 0.05
        else:
            t = 3

        obroty = obrotySilnika / obrotyCoolera / 1.5

        if (temp > obroty):
            temp = (obroty * math.e ** ((-t ** 2) / 2) + obroty)
            if (temp > actualTemp):
                temp = actualTemp
                temp -= random.randint(5, 30) / 10
        else:
            temp = (-obroty * math.e ** ((-t ** 2) / 2) + obroty)
            if (temp < actualTemp):
                temp = actualTemp
                temp += random.randint(5, 30) / 10

        return temp, t

    def timerEvent(self, event):
        self.temp1, self.t1 = self.obliczTemperature(self.temp1, self.actualTemp1, self.t1, self.obrotySilnika1,
                                                     self.obrotyCoolera1)
        temp = ("%.2f" % self.temp1)
        self.temperatura1.setText(temp)
        self.generujBledy1()

        self.temp2, self.t2 = self.obliczTemperature(self.temp2, self.actualTemp2, self.t2, self.obrotySilnika2,
                                                     self.obrotyCoolera2)
        temp = ("%.2f" % self.temp2)
        self.temperatura2.setText(temp)
        self.generujBledy2()

    def generujBledy1(self):

        self.counter += 1

        if self.temp1 > 90 and not self.jestBlad1:
            self.bledy1.setText("SILNIK PRZEGRZANY")
            self.jestBlad1 = True

        if (random.randint(1, 100) == 2 and not self.jestBlad1 and self.actualTemp1):
            rand = random.randint(1, 4)
            self.jestBlad1 = True
            if (rand == 1):
                self.bledy1.setText("MAŁO PALIWA")
            elif (rand == 2):
                self.bledy1.setText("MAŁO OLEJU")
            elif (rand == 3):
                self.bledy1.setText("ZA DUŻO SPALIN")
            elif (rand == 4):
                self.bledy1.setText("NIEZNANY BŁĄD")

    def generujBledy2(self):

        self.counter += 1

        if self.temp2 > 90 and not self.jestBlad2:
            self.bledy2.setText("SILNIK PRZEGRZANY")
            self.jestBlad2 = True

        if (random.randint(1, 100) == 2 and not self.jestBlad2 and self.actualTemp2):
            rand = random.randint(1, 4)
            self.jestBlad2 = True
            if (rand == 1):
                self.bledy2.setText("MAŁO PALIWA")
            elif (rand == 2):
                self.bledy2.setText("MAŁO OLEJU")
            elif (rand == 3):
                self.bledy2.setText("ZA DUŻO SPALIN")
            elif (rand == 4):
                self.bledy2.setText("NIEZNANY BŁĄD")

    def kasowanieBledow1(self):
        self.counter = 0
        self.jestBlad1 = False
        self.bledy1.setText(EMPTY_STRING)

    def kasowanieBledow2(self):
        self.counter = 0
        self.jestBlad2 = False
        self.bledy2.setText(EMPTY_STRING)

    def koniec(self):
        self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = MainWindow()
    okno.show()
    okno.setWindowTitle("Symulator linii produkcyjnej")
    # okno.resize(800,800)
    okno.resize(500, 350)
    sys.exit(app.exec_())
