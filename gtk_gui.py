#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi import require_version
require_version( 'Gtk', '3.0' )

from gi.repository import Gtk


class ProductionLineViewer( Gtk.Window ):
    def __init__(self):
        super().__init__(title = "Symulator Linii produkcyjnej", window_position = Gtk.WindowPosition.CENTER )

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
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)


        self.silnik1 = Gtk.Label( label = "<b>Silnik 1</b>", use_markup = True)
        vbox_left.pack_start(self.silnik1, True, True, 0)

        ad1 = Gtk.Adjustment(50, 0, 100, 1.0, 1.0, 0.0)
        self.suwak1 = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)

        self.suwak1.set_digits(0)
        self.suwak1.connect("value-changed", self.silnik1change)

        vbox_left.pack_start(self.suwak1, True, True, 0)

        chlodnica1 = Gtk.Label( label = "<b>Chłodnica 1</b>", use_markup = True )
        vbox_left.pack_start(chlodnica1, True, True, 0)

        silnik2 = Gtk.Label( label = "<b>Silnik 2</b>", use_markup = True )
        vbox_right.pack_start(silnik2, True, True, 0)


        # self.grid = Gtk.Grid()
        # self.grid.attach(row1,0,0,1,1)
        # self.grid.attach(row2,2,1,1,1)

        vbox.pack_start(hbox, False, True, 0)
        self.add (vbox)
        self.set_default_size( 800, 600 )

    def silnik1change(self, event):
        val = int(self.suwak1.get_value())
        val = "{:03d}".format()
        self.lcd1.set_text(val)


        self.counter = 0
        self.actualTemp1 = self.temp1
        self.t1 = 0
        self.obrotySilnika1 = wartosc / 4
        self.lcd.display(wartosc)

w = ProductionLineViewer()
w.connect("delete-event", Gtk.main_quit)
w.show_all()
Gtk.main()