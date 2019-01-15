#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi import require_version
require_version( 'Gtk', '3.0' )

from gi.repository import Gtk, GObject, Gio
import math
import random

EMPTY_STRING = "                   "

ABOUT = "Zadaniem dyspozytora jest sterowanie prędkością obrotową silników, tak aby\n" \
        "nie doprowadzić do ich przegrzania. Do swojej dyspozycji ma on dwa suwaki,\njeden służy do zwiększania " \
        "obrotów silnika, drugi do zwiększania obrotów układu chłodzenia,\ndzięki czemu możliwe jest " \
        "kontrolowanie temperatury silników.\nDodatkowo w czasie trwania symulacji mogą wystąpić błędy,\nktórych " \
        "kasowanie umożliwia przycisk u dołu ekranu."

class DialogExample(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "O programie", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        # self.set_default_size(150, 100)

        label = Gtk.Label(ABOUT)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

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
        about = Gtk.MenuItem("Pomoc")
        about.set_submenu(aboutmenu)
        # author = Gtk.EventBox()
        # label = Gtk.Label("Right-click to see the popup menu.")
        # author.add(label)
        author = Gtk.MenuItem("O programie")
        author.connect("button-press-event", self.on_button_clicked)
        aboutmenu.append(author)
        menuBar.append(about)

        vbox = Gtk.VBox(False, 2)
        vbox.pack_start(menuBar, False, False, 0)

        hbox = Gtk.Box(spacing=10)
        # hbox.set_homogeneous(True)

        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)


        self.silnik1Label = Gtk.Label(label ="<b><big>Silnik 1</big></b>", use_markup = True)
        vbox_left.pack_start(self.silnik1Label, True, True, 10)

        obrotyLabel = Gtk.Label(label ="<b>Obroty:</b>", use_markup = True)
        vbox_left.pack_start(obrotyLabel, True, True, 0)

        self.silnik1LCD = Gtk.Label("0")
        vbox_left.pack_start(self.silnik1LCD, True, True, 0)
        ad1 = Gtk.Adjustment(0, 0, 1000, 1, 1, 0)
        self.silnik1Obroty = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1, draw_value=False)
        self.silnik1Obroty.set_digits(0)
        self.silnik1Obroty.connect("value-changed", self.torqueEngineChange1)
        vbox_left.pack_start(self.silnik1Obroty, True, True, 0)

        self.cooler1Label = Gtk.Label(label ="<b>Chłodnica:</b>", use_markup = True)
        vbox_left.pack_start(self.cooler1Label, True, True, 0)

        self.cooler1LCD = Gtk.Label("0")
        vbox_left.pack_start(self.cooler1LCD, True, True, 0)
        ad2 = Gtk.Adjustment(0, 0, 50, 1, 1, 0)
        self.cooler1Obroty = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad2, draw_value=False)
        self.cooler1Obroty.set_digits(0)
        self.cooler1Obroty.connect("value-changed", self.torqueCoolerChange1)
        vbox_left.pack_start(self.cooler1Obroty, True, True, 0)

        temp1Label = Gtk.Label( label = "<b>Temperatura:</b>", use_markup = True )
        vbox_left.pack_start(temp1Label, True, True, 0)

        self.temp1LCD = Gtk.Label("0")
        vbox_left.pack_start(self.temp1LCD, True, True, 0)

        self.bledy1 = Gtk.Label(EMPTY_STRING)
        vbox_left.pack_start(self.bledy1, True, True, 0)

        button = Gtk.Button( label = "Kasuj błędy")
        button.connect("clicked", self.kasowanieBledow1)
        vbox_left.pack_start(button, True, True, 0)

        silnik2 = Gtk.Label( label ="<b><big>Silnik 2</big></b>", use_markup = True )
        vbox_right.pack_start(silnik2, True, True, 10)

        obroty2Label = Gtk.Label(label ="<b>Obroty:</b>", use_markup = True)
        vbox_right.pack_start(obroty2Label, True, True, 0)

        self.silnik2LCD = Gtk.Label("0")
        vbox_right.pack_start(self.silnik2LCD, True, True, 0)
        ad3 = Gtk.Adjustment(0, 0, 1000, 1, 1, 0)
        self.silnik2Obroty = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad3, draw_value=False)
        self.silnik2Obroty.set_digits(0)
        self.silnik2Obroty.connect("value-changed", self.torqueEngineChange2)
        vbox_right.pack_start(self.silnik2Obroty, True, True, 0)

        self.cooler2Label = Gtk.Label(label ="<b>Chłodnica:</b>", use_markup = True)
        vbox_right.pack_start(self.cooler2Label, True, True, 0)

        self.cooler2LCD = Gtk.Label("0")
        vbox_right.pack_start(self.cooler2LCD, True, True, 0)
        ad4 = Gtk.Adjustment(0, 0, 50, 1, 1, 0)
        self.cooler2Obroty = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad4, draw_value=False)
        self.cooler2Obroty.set_digits(0)
        self.cooler2Obroty.connect("value-changed", self.torqueCoolerChange2)
        vbox_right.pack_start(self.cooler2Obroty, True, True, 0)

        temp2Label = Gtk.Label( label = "<b>Temperatura:</b>", use_markup = True )
        vbox_right.pack_start(temp2Label, True, True, 0)

        self.temp2LCD = Gtk.Label("0")
        vbox_right.pack_start(self.temp2LCD, True, True, 0)

        self.bledy2 = Gtk.Label(EMPTY_STRING)
        vbox_right.pack_start(self.bledy2, True, True, 0)

        button = Gtk.Button( label = "Kasuj błędy")
        button.connect("clicked", self.kasowanieBledow2)
        vbox_right.pack_start(button, True, True, 0)

        vbox.pack_start(hbox, True, True, 0)
        self.add (vbox)
        self.set_default_size(500, 350)

    def on_button_clicked(self, event, dada):
        dialog = DialogExample(self)
        dialog.run()
        dialog.destroy()

    def torqueEngineChange1(self, event):
        self.silnik1LCD.set_text(str(int(self.silnik1Obroty.get_value())))
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotySilnika1 = self.silnik1Obroty.get_value() / 4

    def torqueEngineChange2(self, event):
        self.silnik2LCD.set_text(str(int(self.silnik2Obroty.get_value())))
        self.counter = 0
        self.actualTemp2 = self.temp2
        self.t2 = 0
        self.obrotySilnika2 = self.silnik2Obroty.get_value() / 4

    def torqueCoolerChange1(self, event):
        self.cooler1LCD.set_text(str(int(self.cooler1Obroty.get_value())))
        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotyCoolera1 = (self.cooler1Obroty.get_value() / 50) + 1

    def torqueCoolerChange2(self, event):
        self.cooler2LCD.set_text(str(int(self.cooler2Obroty.get_value())))
        self.counter = 0
        self.actualTemp2 = self.temp2
        self.t2 = 0
        self.obrotyCoolera2 = (self.cooler2Obroty.get_value() / 50) + 1

    def timerEvent(self):
        self.temp1, self.t1 = self.obliczTemperature(self.temp1, self.actualTemp1, self.t1, self.obrotySilnika1,
                                                     self.obrotyCoolera1)
        temp = ("%.2f" % self.temp1)
        self.temp1LCD.set_text(temp)
        self.generujBledy1()

        self.temp2, self.t2 = self.obliczTemperature(self.temp2, self.actualTemp2, self.t2, self.obrotySilnika2,
                                                     self.obrotyCoolera2)
        temp2 = ("%.2f" % self.temp2)
        self.temp2LCD.set_text(temp2)
        self.generujBledy2()

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

    def generujBledy1(self):

        self.counter += 1

        if self.temp1 > 90 and not self.jestBlad1:
            self.bledy1.set_text("SILNIK PRZEGRZANY")
            self.jestBlad1 = True

        if (random.randint(1, 100) == 2 and not self.jestBlad1 and self.actualTemp1):
            rand = random.randint(1, 4)
            self.jestBlad1 = True
            if (rand == 1):
                self.bledy1.set_text("MAŁO PALIWA")
            elif (rand == 2):
                self.bledy1.set_text("MAŁO OLEJU")
            elif (rand == 3):
                self.bledy1.set_text("ZA DUŻO SPALIN")
            elif (rand == 4):
                self.bledy1.set_text("NIEZNANY BŁĄD")

    def generujBledy2(self):

        self.counter += 1

        if self.temp2 > 90 and not self.jestBlad2:
            self.bledy2.set_text("SILNIK PRZEGRZANY")
            self.jestBlad2 = True

        if (random.randint(1, 100) == 2 and not self.jestBlad2 and self.actualTemp2):
            rand = random.randint(1, 4)
            self.jestBlad2 = True
            if (rand == 1):
                self.bledy2.set_text("MAŁO PALIWA")
            elif (rand == 2):
                self.bledy2.set_text("MAŁO OLEJU")
            elif (rand == 3):
                self.bledy2.set_text("ZA DUŻO SPALIN")
            elif (rand == 4):
                self.bledy2.set_text("NIEZNANY BŁĄD")

    def kasowanieBledow1(self, event):
        self.counter = 0
        self.jestBlad1 = False
        self.bledy1.set_text(EMPTY_STRING)

    def kasowanieBledow2(self, event):
        self.counter = 0
        self.jestBlad2 = False
        self.bledy2.set_text(EMPTY_STRING)

w = ProductionLineViewer()
w.connect("delete-event", Gtk.main_quit)
w.show_all()
Gtk.main()