##
# AmberLeafBox
# Soup - 2014
##

import gtk
import webkit
from time import time
from gobject import timeout_add_seconds, timeout_add
import pickle

class EventManager:
    def __init__(self):
        self._event_log = []
        self._init_time = time()

    def replay_events(self, window, view, filename, end=None):
        f = open(filename, 'r')
        d = pickle.load(f)

        window.resize(* d['window_size'])
        for item in d['events']:
            
            timeout_add(
                int(item['trigger'] * 1000),
                self.make_callback(window, view, item)
            )
        if end :
            timeout_add(
                int((item['time'] + 2) * 1000),
                end
                )


    def make_callback(self, window, view, event_data, *args):
        """
        return a callback suitable
        for event simulation.
        """

        return self.make_button_callback(window, view, event_data)

    def make_button_callback(self, window, view, oevent):
        def btn_callback():
            event = gtk.gdk.Event(gtk.gdk.BUTTON_PRESS)
            event.x = oevent['x']
            event.y = oevent['y']
            event.window = view.window
            event.button = 1
            event.time = 0
            event.x_root = oevent['x_root']
            event.y_root = oevent['y_root']
            event.send_event = True
            view.emit("button_press_event", event)
            event = gtk.gdk.Event(gtk.gdk.BUTTON_RELEASE)
            event.x = oevent['x']
            event.y = oevent['y']
            event.window = view.window
            event.button = 1
            event.time = oevent['time']
            event.x_root = oevent['x_root']
            event.y_root = oevent['y_root']
            event.send_event = True
            view.emit("button_release_event", event)

        def key_callback():
            event = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
            event.window = view.window
            event.keyval = oevent['keyval']
            event.time = oevent['time']
            event.send_event = True
            view.emit("key_press_event", event)
            event = gtk.gdk.Event(gtk.gdk.KEY_RELEASE)
            event.keyval = oevent['keyval']
            event.window = view.window
            event.time = 0
            event.send_event = True
            view.emit("key_release_event", event)

        return {
            gtk.gdk.BUTTON_PRESS : btn_callback,
            gtk.gdk.KEY_PRESS : key_callback,
            }[oevent['type']]



    def button_press_event(self, widget, event):
        """
        handle click event
        """

        print('intercep :\nx : %d, y : %d' %(event.x, event.y))

        self._event_log.append(
                                {
                                    'type'   : gtk.gdk.BUTTON_PRESS,
                                    'x'      : event.x,
                                    'y'      : event.y,
                                    'x_root' : event.x_root,
                                    'y_root' : event.y_root,
                                    'time'   : event.time,
                                    'trigger': time() - self._init_time,
                                    'keyval' : None,
                                }
                            )
    def key_press_event(self, widget, event):
        """
        handle click event
        """

        print('intercep :\nx : %s' %(gtk.gdk.keyval_name(event.keyval)))

        self._event_log.append(
                                {
                                    'type'   : gtk.gdk.KEY_PRESS,
                                    'x'      : None,
                                    'y'      : None,
                                    'x_root' : None,
                                    'y_root' : None,
                                    'time'   : event.time,
                                    'trigger': time() - self._init_time,
                                    'keyval' : event.keyval,
                                }
                            )

    def export(self):
        return self._event_log


    def dump(self, filename, **datas):
        try :
            f = open(filename, 'w+')
        except Exception, e:
            print("[*] Can't open file %s." %filename)
            raise e

        dump = []
        for data in self._event_log:
            dump.append(data)

        datas['events'] = dump
        pickle.dump(datas, f, 0)
        f.close()


    def get_callback(self, event_type):
        return event_type, {
            "button_press_event"  : self.button_press_event,
            "key_press_event"     : self.key_press_event,
        }[event_type]



class EventPlayerPD(object):
    def __init__(self):
        self._event_list = []


    def load(self, event_list = []):
        self._event_list += event_list


    def replay_events(self, window, view):
        for time, event_string, original_event in self._event_list:
            print(time)
            timeout_add_seconds(1,
                self.make_callback(window,
                                   view,
                                   original_event,
                                   event_string))



    def make_callback(self, window, view, oevent, *args):
        """
        return a callback suitable
        for event simulation.
        """
        return self.make_button_callback(window, view, oevent)


    def make_button_callback(self, window, view, oevent):
        print("Event crafted")
        def callback():
            print("Event fired")
            event = gtk.gdk.Event(gtk.gdk.BUTTON_PRESS)
            event.x = oevent.x
            event.y = oevent.y
            event.window = view.window
            event.button = 1
            event.time = 0
            event.x_root = oevent.x_root
            event.y_root = oevent.y_root
            event.send_event = True
            view.emit("button_press_event", event)
            event = gtk.gdk.Event(gtk.gdk.BUTTON_RELEASE)
            event.x = oevent.x
            event.y = oevent.y
            event.window = view.window
            event.button = 1
            event.time = 0
            event.x_root = oevent.x_root
            event.y_root = oevent.y_root
            event.send_event = True
            view.emit("button_release_event", event)
        return callback

