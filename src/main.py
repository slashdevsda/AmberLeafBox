#!/usr/bin/env python
#-*- coding: utf-8 -*-#
#
# AmberLeafBox
# Soup - 2014
#

import gtk
import webkit
from time import time
from gobject import timeout_add_seconds, timeout_add
import pickle
from optparse import OptionParser
from events import EventManager


class App(object):
    def __init__(self):
        self._options = None

    def run(self):
        self.view = webkit.WebView()
        self.view.get_settings().set_property("enable-webgl", True)
        self.sw = gtk.ScrolledWindow()
        self.sw.add(self.view)
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        try:
            self.win.resize(*[int(i) for i in self._options.window_size.split(',')])
        except Exception as e:
            print(e)
            print('--size require 2 values : "x,y"')
            exit(0)
        self.em = EventManager()
        if self._options.replay:
            self.em.replay_events(
                self.win,
                self.view,
                self._options.filename,
                end = self.quit if self._options.exit_after_run else None
            )


        elif self._options.record:
            self.view.connect(
                * self.em.get_callback("button_press_event")
            )
            self.view.connect(
                * self.em.get_callback("key_press_event")
            )

        self.view.open(self._options.url)
        vbox = gtk.VBox(False)
        menu = self.create_menu()
        vbox.pack_start(menu, False, False, 0)
        vbox.pack_start(self.sw, True, True, 0)

        self.win.add(vbox)
        vbox.show()
        self.win.show_all()
        try:
            gtk.main()
        except KeyboardInterrupt:
            if self._options.record:
                self.em.dump(self._options.filename)

    def parse_args(self):
        parser = OptionParser()
        parser.add_option(
            "-p",
            action="store_true",
            dest="replay",
            default=False,
            help="replay a sequence of events."
        )
        parser.add_option(
            "-r",
            action="store_true",
            dest="record",
            default=False,
            help="record a sequence of events."
        )
        parser.add_option(
            "-f",
            "--file",
            dest="filename",
            default="events.pk",
            help="write/read events from [filename]."
        )
        parser.add_option(
            "-u",
            "--url",
            dest="url",
            default="http://127.0.0.1:3000/",
        )
        parser.add_option(
            "-s",
            "--size",
            action="store",
            dest="window_size",
            default="800,600",
            help="Window size."

        )
        parser.add_option(
            "-e",
            "--exit",
            dest="exit_after_run",
            action='store_true',
            default=False,
            help="(Only for replay-mode) exit when finished."
        )


        self._options, args = parser.parse_args()
        return  (self._options, args)

    def save_session(self, *args):
        if self._options.record:
            self.em.dump(
                self._options.filename,
                window_size=[int(i) for i in self._options.window_size.split(',')]
            )
        print("session saved!")
        return 0

    def quit(self, *args):
        gtk.main_quit()
        return 0

    def create_menu(self):
        """
        UI Stuff, again
        from http://www.pygtk.org/pygtk2tutorial/ch-MenuWidget.html
        """
        file_item = gtk.MenuItem("File")
        menu_bar = gtk.MenuBar()
        file_menu = gtk.Menu()
        quit_item = gtk.MenuItem("Quit")
        save_item = gtk.MenuItem("Save session")
        save_quit_item = gtk.MenuItem("Save session and quit...")
        file_menu.append(quit_item)


        quit_item.connect_object(
            "activate",
            self.quit,
            "quit_session"
        )

        # recording options
        if self._options.record:
            file_menu.append(save_quit_item)
            file_menu.append(save_item)

            save_item.connect_object(
                "activate",
                self.save_session,
                "save"
            )

            save_quit_item.connect_object(
                "activate",
                lambda x : self.save_session() + self.quit(),
                "quit"
            )

            save_quit_item.show()
            save_item.show()


        quit_item.show()
        menu_bar.append(file_item)
        file_item.set_submenu(file_menu)
        menu_bar.show()

        return menu_bar

def main():
    app = App()
    app.parse_args()
    app.run()