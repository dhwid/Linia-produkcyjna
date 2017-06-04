#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from gui import Ui_Widget, LoginDialog
from PyQt5 import QtCore
import PyQt5.QtMultimedia as M
import math
import random



class Zadania(QWidget, Ui_Widget):


    def __init__(self, parent=None):
        super(Zadania, self).__init__(parent)
        self.setupUi(self)

        self.counter = 0
        self.t1 = 0
        self.actualTemp1 = 0
        self.t2 = 0
        self.actualTemp2 = 0

        url = QtCore.QUrl.fromLocalFile("alarm.mp3")
        content = M.QMediaContent(url)
        self.player = M.QMediaPlayer()
        self.player.setMedia(content)

        self.obrotySilnika1 = 0
        self.obrotySilnika2 = 0
        self.temp1 = 0
        self.temp2 = 0

        self.obrotyCoolera1 = 1
        self.obrotyCoolera2 = 1
        self.jestBlad1 = False
        self.jestBlad2 = False
        self.loguj()

        #Sygnaly
        self.suwak.valueChanged.connect(self.wartoscSilnik1)
        self.suwak1.valueChanged.connect(self.wartoscCooler1)
        self.kasujBledy1.clicked.connect(self.kasowanieBledow1)
        self.suwak2.valueChanged.connect(self.wartoscSilnik2)
        self.suwak3.valueChanged.connect(self.wartoscCooler2)
        self.kasujBledy2.clicked.connect(self.kasowanieBledow2)

        #Timer
        self.timer = QtCore.QBasicTimer()
        self.speed = 100
        self.timer.start(self.speed, self)

    def wartoscSilnik1(self, wartosc):
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotySilnika1 = wartosc/4
        self.lcd.display(wartosc)

    def wartoscCooler1(self, wartosc):
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotyCoolera1 = (wartosc/50) +1
        self.lcd1.display(wartosc)

    def wartoscSilnik2(self, wartosc):
        self.counter = 0
        self.actualTemp2 = self.temp2
        self.t2 = 0
        self.obrotySilnika2 = wartosc/4
        self.lcd2.display(wartosc)

    def wartoscCooler2(self, wartosc):
        self.counter = 0
        self.actualTemp2 = self.temp2
        self.t2 = 0
        self.obrotyCoolera2 = (wartosc/50) +1
        self.lcd3.display(wartosc)

    def obliczTemperature(self,temp,actualTemp,t,obrotySilnika,obrotyCoolera):

        if (t<3.5):
            t+=0.05
        else:
            t = 3

        obroty = obrotySilnika/obrotyCoolera/1.5

        if (temp > obroty):
            temp = (obroty * math.e ** ((-t ** 2) / 2) + obroty)
            if(temp > actualTemp):
                temp = actualTemp
                temp -= random.randint(5,30)/10
        else:
            temp = (-obroty * math.e ** ((-t ** 2) / 2) + obroty)
            if(temp < actualTemp):
                temp = actualTemp
                temp += random.randint(5,30)/10

        return temp,t


    def loguj(self):
        login, haslo, ok = LoginDialog.getLoginHaslo(self)
        if not ok:
            self.loguj()

        if not login or not haslo:
            QMessageBox.warning(self, 'Błąd',
                                'Pusty login lub hasło!', QMessageBox.Ok)
            self.loguj()

        # QMessageBox.information(self,
        #     'Dane logowania', 'Podano: ' + login + ' ' + haslo, QMessageBox.Ok)

        if (login == 'ask' and haslo == 'ask'):
            return
        else:
            self.loguj()

    def timerEvent(self, event):
        self.temp1, self.t1 = self.obliczTemperature(self.temp1,self.actualTemp1,self.t1,self.obrotySilnika1,self.obrotyCoolera1)
        temp = ("%.2f" % self.temp1)
        self.temperatura1.setText(temp)
        self.generujBledy1()

        self.temp2, self.t2 = self.obliczTemperature(self.temp2,self.actualTemp2,self.t2,self.obrotySilnika2,self.obrotyCoolera2)
        temp = ("%.2f" % self.temp2)
        self.temperatura2.setText(temp)
        self.generujBledy2()

    def generujBledy1(self):

        self.counter += 1

        if self.temp1 > 90 and not self.jestBlad1:
            self.bledy1.setText("SILNIK JEST PRZEGRZANY !!!")
            self.jestBlad1 = True


        if (random.randint(1,100) == 2 and not self.jestBlad1):
            rand = random.randint(1, 4)
            self.jestBlad1 = True
            if(rand == 1):
                self.bledy1.setText("NIE DZIALA JEDEN Z CYLINDROW")
            elif(rand == 2):
                self.bledy1.setText("MALO OLEJU")
            elif(rand == 3):
                self.bledy1.setText("ZA DUZO SPALIN")
            elif(rand == 4):
                self.bledy1.setText("NIEZNANY BLAD")

        if (self.counter) > 150:
            self.player.play()
            self.brakAktywnosci()

    def generujBledy2(self):

        self.counter += 1

        if self.temp2 > 90 and not self.jestBlad2:
            self.bledy2.setText("SILNIK JEST PRZEGRZANY !!!")
            self.jestBlad2 = True


        if (random.randint(1,100) == 2 and not self.jestBlad2):
            rand = random.randint(1, 4)
            self.jestBlad2 = True
            if(rand == 1):
                self.bledy2.setText("NIE DZIALA JEDEN Z CYLINDROW")
            elif(rand == 2):
                self.bledy2.setText("MALO OLEJU")
            elif(rand == 3):
                self.bledy2.setText("ZA DUZO SPALIN")
            elif(rand == 4):
                self.bledy2.setText("NIEZNANY BLAD")

        if (self.counter) > 150:
            self.player.play()
            self.brakAktywnosci()

    def kasowanieBledow1(self):
        self.counter = 0
        self.jestBlad1 = False
        self.bledy1.setText("")

    def kasowanieBledow2(self):
        self.counter = 0
        self.jestBlad2 = False
        self.bledy2.setText("")

    def brakAktywnosci(self):
        haslo, ok = QInputDialog.getText(self, 'Brak akywnosci', 'Podaj haslo')
        if ok and haslo == 'ask':
            self.player.stop()
            self.counter = 0
        else:

            QMessageBox.warning(
            self, 'Błąd', 'Brak hasla lub bledne haslo!', QMessageBox.Ok)
            return


    def koniec(self):
        self.close()

    def keyPressEvent(self, e):
        self.key = e.key()
        if (self.key==QtCore.Qt.Key_P):
            self.player.stop()
            self.counter = 0
            print("wcisnales P")



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = Zadania()
    okno.show()
    okno.move(350, 200)
    sys.exit(app.exec_())