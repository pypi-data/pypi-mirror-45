import gi
import paho.mqtt.client as mqtt
import time
import base64

MQTT="192.168.2.126"



gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0') 
from gi.repository import GObject
from gi.repository import Notify
from gi.repository import Gtk


class MyClass(GObject.Object):
    def __init__(self):

        super(MyClass, self).__init__()
        # lets initialise with the application name
        Notify.init("Message")

    def send_notification(self, title, text, file_path_to_icon=""):
        
        n = Notify.Notification.new(title, text, file_path_to_icon)
        n.set_timeout(4000)
        n.set_urgency(Notify.Urgency.LOW)
        n.show()
#        time.sleep(5)
#        n.close()
#        n.uninit()



def run():
    print("ok")

if (__name__=="__main__"):
    run()


def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature/#")
    client.subscribe("download/#")
    client.subscribe("ghome/#")

    pass

def on_message(client, userdata, msg):
    #print(msg.payload)
    message=msg.payload.decode('utf-8')
#    client.my.send_notification("Broker Qtt",message,"kde")
    icon="weather-clear"

    if (msg.topic=="download/info"):
        message=base64.b64decode(message).decode('utf-8')
        icon="flareGet"

    if (msg.topic=="ghome/nowplaying"):
        icon="web-google-play-music"
    
    

    my=MyClass()
    topic=msg.topic.split('/')[0]
    my.send_notification("%s"%topic,message,icon)
    my.uninit()
    return 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT, 1883, 60)
client.my=MyClass()

client.loop_start()


Gtk.main()
