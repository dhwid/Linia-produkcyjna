# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLCDNumber, QSplitter
from PyQt5.QtWidgets import QRadioButton, QGroupBox


class Ui_Widget(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        # tabelaryczny widok danych
        self.widok = QTableView()

        # etykiety
        Silnik1 = QLabel("Silnik 1", self)
        Silnik1.setAlignment(Qt.AlignCenter)
        Silnik1.setStyleSheet('font-size: 20pt; font-family: Arial')
        Silnik2 = QLabel("Silnik 2", self)
        Silnik2.setStyleSheet('font-size: 20pt; font-family: Arial')
        Silnik2.setAlignment(Qt.AlignCenter)
        Chlodzenie = QLabel("Cooler",self)
        Chlodzenie2 = QLabel("Cooler",self)
        Temperatura = QLabel("Temperatura:", self)
        Temperatura2 = QLabel("Temperatura:", self)
        self.temperatura1 = QLineEdit()
        self.bledy1 = QLineEdit()
        self.temperatura2 = QLineEdit()
        self.bledy2 = QLineEdit()

        # przyciski Push ###
        self.kasujBledy1 = QPushButton("Kasuj Bledy")
        self.kasujBledy2 = QPushButton("Kasuj Bledy")

        # Slider i LCDNumber ###
        self.suwak = QSlider(Qt.Horizontal)
        self.suwak.setMinimum(1)
        self.suwak.setMaximum(1000)
        self.lcd = QLCDNumber()
        self.lcd.setSegmentStyle(QLCDNumber.Flat)

        # Slider i LCDNumber ###
        self.suwak1 = QSlider(Qt.Horizontal)
        self.suwak1.setMinimum(1)
        self.suwak1.setMaximum(50)
        self.lcd1 = QLCDNumber()
        self.lcd1.setSegmentStyle(QLCDNumber.Flat)

        # Slider i LCDNumber ###
        self.suwak2 = QSlider(Qt.Horizontal)
        self.suwak2.setMinimum(1)
        self.suwak2.setMaximum(1000)
        self.lcd2 = QLCDNumber()
        self.lcd2.setSegmentStyle(QLCDNumber.Flat)

        # Slider i LCDNumber ###
        self.suwak3 = QSlider(Qt.Horizontal)
        self.suwak3.setMinimum(1)
        self.suwak3.setMaximum(50)
        self.lcd3 = QLCDNumber()
        self.lcd3.setSegmentStyle(QLCDNumber.Flat)



        # układ poziomy (splitter) dla slajdera i lcd
        ukladH2 = QSplitter(Qt.Horizontal, self)
        ukladH2.addWidget(self.suwak)
        ukladH2.addWidget(self.lcd)
        ukladH2.setSizes((125, 75))

        # układ poziomy (splitter) dla slajdera1 i lcd1
        ukladH3 = QSplitter(Qt.Horizontal, self)
        ukladH3.addWidget(self.suwak1)
        ukladH3.addWidget(self.lcd1)
        ukladH3.setSizes((125, 75))


        # układ poziomy (splitter) dla slajdera1 i lcd1
        ukladH4 = QSplitter(Qt.Horizontal, self)
        ukladH4.addWidget(self.suwak2)
        ukladH4.addWidget(self.lcd2)
        ukladH4.setSizes((125, 75))


        # układ poziomy (splitter) dla slajdera1 i lcd1
        ukladH5 = QSplitter(Qt.Horizontal, self)
        ukladH5.addWidget(self.suwak3)
        ukladH5.addWidget(self.lcd3)
        ukladH5.setSizes((125, 75))


        # układ przycisków Push ###
        uklad = QHBoxLayout()


        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()

        ukladT.addWidget(Silnik1, 0, 0)
        ukladT.addWidget(ukladH2,1,0)
        ukladT.addWidget(Chlodzenie,2,0)
        ukladT.addWidget(ukladH3,3,0)
        ukladT.addWidget(Temperatura, 4, 0)
        ukladT.addWidget(self.temperatura1,5,0)
        ukladT.addWidget(self.bledy1,6,0)
        ukladT.addWidget(self.kasujBledy1,7,0)


        ukladT.addWidget(Silnik2, 0, 1)
        ukladT.addWidget(ukladH4,1,1)
        ukladT.addWidget(Chlodzenie2,2,1)
        ukladT.addWidget(ukladH5,3,1)
        ukladT.addWidget(Temperatura2, 4,1)
        ukladT.addWidget(self.temperatura2,5,1)
        ukladT.addWidget(self.bledy2,6,1)
        ukladT.addWidget(self.kasujBledy2,7,1)



        # główny układ okna ###
        ukladV = QVBoxLayout(self)
        ukladV.addLayout(uklad)
        ukladV.addLayout(ukladT)

        # właściwości widżetu ###
        self.setWindowTitle("Symulator lini produkcyjnej")
        self.resize(800, 600)

class LoginDialog(QDialog):
    """ Okno dialogowe logowania """

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        # etykiety, pola edycyjne i przyciski ###
        loginLbl = QLabel('Login')
        hasloLbl = QLabel('Hasło')
        self.login = QLineEdit()
        self.haslo = QLineEdit()
        self.przyciski = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # układ główny ###
        uklad = QGridLayout(self)
        uklad.addWidget(loginLbl, 0, 0)
        uklad.addWidget(self.login, 0, 1)
        uklad.addWidget(hasloLbl, 1, 0)
        uklad.addWidget(self.haslo, 1, 1)
        uklad.addWidget(self.przyciski, 2, 0, 2, 0)

        # sygnały i sloty ###
        self.przyciski.accepted.connect(self.accept)
        self.przyciski.rejected.connect(self.reject)

        # właściwości widżetu ###
        self.setModal(True)
        self.setWindowTitle('Logowanie')

    def loginHaslo(self):
        return (self.login.text().strip(),
                self.haslo.text().strip())

    # metoda statyczna, tworzy dialog i zwraca (login, haslo, ok)
    @staticmethod
    def getLoginHaslo(parent=None):
        dialog = LoginDialog(parent)
        dialog.login.setFocus()
        ok = dialog.exec_()
        login, haslo = dialog.loginHaslo()
        return (login, haslo, ok == QDialog.Accepted)