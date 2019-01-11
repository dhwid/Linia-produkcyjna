#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi import require_version
require_version( 'Gtk', '3.0' )

from gi.repository import Gtk, GObject
import math
import random


class ProductionLineViewer( Gtk.Window ):
    def __init__(self):
        super().__init__(title = "Symulator linii produkcyjnej", window_position = Gtk.WindowPosition.CENTER )

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
        GObject.timeout_add(100, self.timerEvent)


        #menuBar
        menuBar = Gtk.MenuBar()
        aboutmenu = Gtk.Menu()
        about = Gtk.MenuItem("O autorze")
        about.set_submenu(aboutmenu)
        author = Gtk.MenuItem("Dawid Hirsz")
        aboutmenu.append(author)
        menuBar.append(about)

        vbox = Gtk.VBox(False, 2)
        vbox.pack_start(menuBar, False, False, 0)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)

        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)


        self.silnik1Label = Gtk.Label(label ="<b>Silnik 1</b>", use_markup = True)
        vbox_left.pack_start(self.silnik1Label, True, True, 0)

        self.silnik1LCD = Gtk.Label("0")
        vbox_left.pack_start(self.silnik1LCD, True, True, 0)

        ad1 = Gtk.Adjustment(0, 0, 1000, 1, 1, 0)
        self.silnik1Obroty = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1, value_pos=5)

        self.silnik1Obroty.set_digits(0)
        self.silnik1Obroty.connect("value-changed", self.torqueEngineChange1)

        vbox_left.pack_start(self.silnik1Obroty, True, True, 0)

        self.cooler1Label = Gtk.Label(label ="<b>Chłodnica</b>", use_markup = True)
        vbox_left.pack_start(self.cooler1Label, True, True, 0)

        ad2 = Gtk.Adjustment(0, 0, 50, 1, 1, 0)

        self.cooler1Obroty = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad2)

        self.cooler1Obroty.set_digits(0)
        self.cooler1Obroty.connect("value-changed", self.torqueCoolerChange1)

        vbox_left.pack_start(self.cooler1Obroty, True, True, 0)

        temp1Label = Gtk.Label( label = "<b>Temperatura</b>", use_markup = True )
        vbox_left.pack_start(temp1Label, True, True, 0)

        self.temp1LCD = Gtk.Label("0")
        vbox_left.pack_start(self.temp1LCD, True, True, 0)

        self.bledy1 = Gtk.Label("BRAK BŁĘDÓW")
        vbox_left.pack_start(self.bledy1, True, True, 0)

        button = Gtk.Button( label = "Kasuj błędy")
        vbox_left.pack_start(button, True, True, 0)

        silnik2 = Gtk.Label( label = "<b>Silnik 2</b>", use_markup = True )
        vbox_right.pack_start(silnik2, True, True, 0)


        # self.grid = Gtk.Grid()
        # self.grid.attach(row1,0,0,1,1)
        # self.grid.attach(row2,2,1,1,1)

        vbox.pack_start(hbox, False, True, 0)
        self.add (vbox)
        self.set_default_size( 800, 600 )

    def torqueEngineChange1(self, event):
        self.silnik1LCD.set_text(str(self.silnik1Obroty.get_value()))
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotySilnika1 = self.silnik1Obroty.get_value() / 4

    def torqueCoolerChange1(self, event):
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotyCoolera1 = (self.cooler1Obroty.get_value() / 50) + 1

    def timerEvent(self):
        self.temp1, self.t1 = self.obliczTemperature(self.temp1, self.actualTemp1, self.t1, self.obrotySilnika1,
                                                     self.obrotyCoolera1)
        temp = ("%.2f" % self.temp1)
        self.temp1LCD.set_text(temp)
        # self.generujBledy1()

        # temp2, self.t2 = self.obliczTemperature(self.t2, self.actualTemp2, self.t2, self.suwak2.get_value(),
        #                                              self.cooler2.get_value())
        # temp2 = ("%.2f" % temp2)
        # self.temp2.setText(temp2)
        # self.generujBledy2()

        return True

    def obliczTemperature(self, temp, actualTemp, t, obrotySilnika, obrotyCoolera):

        if (t < 3.5):
            t += 0.05
        else:
            t = 3

        if obrotyCoolera != 0:
            obroty = obrotySilnika / obrotyCoolera / 1.5
        else:
            obroty = obrotySilnika / 1.5

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

w = ProductionLineViewer()
w.connect("delete-event", Gtk.main_quit)
w.show_all()
Gtk.main()