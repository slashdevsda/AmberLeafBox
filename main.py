##
# AmberLeafBox
# Soup - 2014
##

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
        self.win.resize(800, 600)

        self.em = EventManager()
        if self._options.replay:
            self.em.replay_events(
                self.win,
                self.view,
                self._options.filename
            )

        elif self._options.record:
            self.view.connect(
                * self.em.get_callback("button_press_event")
            )


        self.view.open("http://127.0.0.1:3000/")
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
            default=False
        )
        parser.add_option(
            "-r",
            action="store_true",
            dest="record",
            default=False
        )
        parser.add_option(
            "-f",
            "--file",
            dest="filename",
            default="events.pk",
            help="write/read events from [filename]."
        )

        self._options, args = parser.parse_args()

        return  (self._options, args)

    def save_session(self, *args):
        if self._options.record:
            self.em.dump(self._options.filename)
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
        quit_item = gtk.MenuItem("quit without saving")
        save_item = gtk.MenuItem("Save session")
        save_quit_item = gtk.MenuItem("Save session and quit...")

        # Add them to the menu
        file_menu.append(save_quit_item)
        file_menu.append(save_item)
        file_menu.append(quit_item)
                
        save_item.connect_object(
            "activate",
            self.save_session,
            "save_session"
        )

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

        # We can attach the Quit menu item to our exit function
        #quit_item.connect_object ("activate", destroy, "file.quit")
        save_quit_item.show()
        save_item.show()
        quit_item.show()

        menu_bar.append(file_item)
        file_item.set_submenu(file_menu)
        file_item.show()

        menu_bar.show()

        print("=" * 60)
        return menu_bar

if __name__ == '__main__':
    app = App()
    app.parse_args()
    app.run()