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
        self.win.add(self.sw)
        self.win.resize(800, 600)


        self.win.show_all()

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

        try:
            gtk.main()
        except KeyboardInterrupt:
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
        
if __name__ == '__main__':
    app = App()
    app.parse_args()
    app.run()