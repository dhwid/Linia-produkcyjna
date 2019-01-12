# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLCDNumber, QSplitter
from PyQt5 import QtGui

EMPTY_STRING = "                   "


class Ui_Widget(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.setFont(QtGui.QFont("Cantarell", 12, QtGui.QFont.Light))

        # tabelaryczny widok danych
        self.widok = QTableView()

        # etykiety
        Silnik1 = QLabel("Silnik 1", self)
        Silnik1.setAlignment(Qt.AlignCenter)
        Silnik1.setStyleSheet('font-size: 15pt; font: bold "Cantarell"')

        Silnik2 = QLabel("Silnik 2", self)
        Silnik2.setStyleSheet('font-size: 15pt; font: bold "Cantarell"')
        Silnik2.setAlignment(Qt.AlignCenter)

        Obroty1 = QLabel("Obroty:", self)
        Obroty1.setStyleSheet('font: bold')
        Obroty1.setAlignment(Qt.AlignCenter)
        Obroty2 = QLabel("Obroty:", self)
        Obroty2.setStyleSheet('font: bold')
        Obroty2.setAlignment(Qt.AlignCenter)
        Chlodzenie1 = QLabel("Chłodnica:",self)
        Chlodzenie1.setStyleSheet('font: bold')
        Chlodzenie1.setAlignment(Qt.AlignCenter)
        Chlodzenie2 = QLabel("Chłodnica:",self)
        Chlodzenie2.setStyleSheet('font: bold')
        Chlodzenie2.setAlignment(Qt.AlignCenter)
        Temperatura = QLabel("Temperatura:", self)
        Temperatura.setStyleSheet('font: bold')
        Temperatura.setAlignment(Qt.AlignCenter)
        Temperatura2 = QLabel("Temperatura:", self)
        Temperatura2.setStyleSheet('font: bold')
        Temperatura2.setAlignment(Qt.AlignCenter)

        self.temperatura1 = QLabel("0.00")
        self.temperatura1.setAlignment(Qt.AlignCenter)
        self.bledy1 = QLabel(EMPTY_STRING)
        self.bledy1.setAlignment(Qt.AlignCenter)
        self.temperatura2 = QLabel("0.00")
        self.temperatura2.setAlignment(Qt.AlignCenter)
        self.bledy2 = QLabel(EMPTY_STRING)
        self.bledy2.setAlignment(Qt.AlignCenter)

        # przyciski Push ###
        self.kasujBledy1 = QPushButton("Kasuj błędy")
        self.kasujBledy2 = QPushButton("Kasuj błędy")

        # Slider i LCDNumber ###
        self.suwak = QSlider(Qt.Horizontal)
        self.suwak.setMinimum(1)
        self.suwak.setMaximum(1000)
        self.lcd = QLabel("0")
        self.lcd.setAlignment(Qt.AlignCenter)

        # Slider i LCDNumber ###
        self.suwak1 = QSlider(Qt.Horizontal)
        self.suwak1.setMinimum(1)
        self.suwak1.setMaximum(50)
        self.lcd1 = QLabel("0")
        self.lcd1.setAlignment(Qt.AlignCenter)


        # Slider i LCDNumber ###
        self.suwak2 = QSlider(Qt.Horizontal)
        self.suwak2.setMinimum(1)
        self.suwak2.setMaximum(1000)
        self.lcd2 = QLabel("0")
        self.lcd2.setAlignment(Qt.AlignCenter)


        # Slider i LCDNumber ###
        self.suwak3 = QSlider(Qt.Horizontal)
        self.suwak3.setMinimum(1)
        self.suwak3.setMaximum(50)
        self.lcd3= QLabel("0")
        self.lcd3.setAlignment(Qt.AlignCenter)


        # układ poziomy (splitter) dla slajdera i lcd
        ukladH2 = QSplitter(Qt.Vertical, self)
        ukladH2.addWidget(self.lcd)
        ukladH2.addWidget(self.suwak)

        # układ poziomy (splitter) dla slajdera1 i lcd1
        ukladH3 = QSplitter(Qt.Vertical, self)
        ukladH3.addWidget(self.lcd1)
        ukladH3.addWidget(self.suwak1)

        # układ poziomy (splitter) dla slajdera1 i lcd1
        ukladH4 = QSplitter(Qt.Vertical, self)
        ukladH4.addWidget(self.lcd2)
        ukladH4.addWidget(self.suwak2)

        # układ poziomy (splitter) dla slajdera1 i lcd1
        ukladH5 = QSplitter(Qt.Vertical, self)
        ukladH5.addWidget(self.lcd3)
        ukladH5.addWidget(self.suwak3)
        # ukladH5.setSizes((125, 75))

        # układ przycisków Push ###
        uklad = QHBoxLayout()

        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()

        ukladT.addWidget(Silnik1, 0, 0)
        ukladT.addWidget(Obroty1, 1, 0)
        ukladT.addWidget(self.lcd,2,0)
        ukladT.addWidget(self.suwak,3,0)
        ukladT.addWidget(Chlodzenie1,4,0)
        ukladT.addWidget(self.lcd1,5,0)
        ukladT.addWidget(self.suwak1,6,0)
        ukladT.addWidget(Temperatura, 7, 0)
        ukladT.addWidget(self.temperatura1,8,0)
        ukladT.addWidget(self.bledy1,9,0)
        ukladT.addWidget(self.kasujBledy1,10,0)


        ukladT.addWidget(Silnik2, 0, 1)
        ukladT.addWidget(Obroty2, 1, 1)
        ukladT.addWidget(self.lcd2,2,1)
        ukladT.addWidget(self.suwak2,3,1)
        ukladT.addWidget(Chlodzenie2,4,1)
        ukladT.addWidget(self.lcd3,5,1)
        ukladT.addWidget(self.suwak3,6,1)
        ukladT.addWidget(Temperatura2, 7, 1)
        ukladT.addWidget(self.temperatura2,8,1)
        ukladT.addWidget(self.bledy2,9,1)
        ukladT.addWidget(self.kasujBledy2,10,1)

        # główny układ okna ###
        ukladV = QVBoxLayout(self)
        ukladV.addLayout(uklad)
        ukladV.addLayout(ukladT)

