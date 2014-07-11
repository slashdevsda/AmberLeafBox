import gtk
import webkit
from time import time
from gobject import timeout_add_seconds, timeout_add
import pickle

class EventManager:
    def __init__(self):
        self._event_log = []
        self._init_time = time()

    def replay_events(self, window, view, filename):
        f = open(filename, 'r')
        d = pickle.load(f)
        for item in d:
            
            timeout_add(
                int(item['time'] * 1000),
                self.make_callback(window, view, item)
            )
            print("replay event")

    def make_callback(self, window, view, event_data, *args):
        """
        return a callback suitable
        for event simulation.
        """
        if event_data['type'] == gtk.gdk.BUTTON_PRESS:
            return self.make_button_callback(window, view, event_data)
        return self.make_button_callback(window, view, event_data)

    def make_button_callback(self, window, view, oevent):
        def callback():
            event = gtk.gdk.Event(gtk.gdk.BUTTON_PRESS)
            event.x = oevent['x']
            event.y = oevent['y']
            event.window = view.window
            event.button = 1
            event.time = 0
            event.x_root = oevent['x_root']
            event.y_root = oevent['y_root']
            event.send_event = True
            #pprint( { var:getattr(event, var) for var in dir(event) } )
            view.emit("button_press_event", event)
            #tshirt riri fifi loulou
            event = gtk.gdk.Event(gtk.gdk.BUTTON_RELEASE)
            event.x = oevent['x']
            event.y = oevent['y']
            event.window = view.window
            event.button = 1
            event.time = 0
            event.x_root = oevent['x_root']
            event.y_root = oevent['y_root']
            event.send_event = True
            view.emit("button_release_event", event)
        return callback

        
    def button_press_event(self, widget, event):
        """
        handle click event
        """
        #pprint( { var:getattr(event, var) for var in dir(event) } )

        print('intercep :\nx : %d, y : %d' %(event.x, event.y))

        self._event_log.append((time() - self._init_time,
                                'click',
                                event.x, event.y, event.x_root, event.y_root))

    def export(self):
        return self._event_log


    def dump(self, filename):
        try :
            f = open(filename, 'w+')
        except Exception, e:
            print("[*] Can't open file %s." %filename)
            raise e

        dump = []
        for event in self._event_log:
            print(event)
            d = {
                'time':event[0],
                'type':gtk.gdk.BUTTON_PRESS,
                'x':event[2],
                'y':event[3],
                'x_root':event[4],
                'y_root':event[5],
            }
            dump.append(d)
        pickle.dump(dump, f)
        f.close()


    def get_callback(self, event_type):
        return event_type, {
            #"motion_notify_event" : self.motion_notify_event,
            "button_press_event"  : self.button_press_event,
        }[event_type]


class EventPlayer(object):
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
            #pprint( { var:getattr(event, var) for var in dir(event) } )
            view.emit("button_press_event", event)
            #tshirt riri fifi loulou
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

