import paho.mqtt.client as mqtt
import time
import logging
import sys

#broker_address="192.168.0.47";
broker_address="146.115.80.244";
broker_port="1883";
logging.basicConfig(level=logging.ERROR)

mqtt.Client.connected_flag = False;
mqtt_subscriber_client = mqtt.Client(client_id="sensor_sub_1", clean_session=False, userdata=None)

def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    try:
        logging.error("start eith subscription ")
        mqtt_subscriber_client.subscribe("tajanep");
        #logging.ERROR("Connection successful !");
    except Exception as e:
        logging.error("Error during subscription ")
        logging.error(e);
        mqtt_subscriber_client.loop_stop();
        sys.exit(1);


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received Packet")
    print("Counter :"+str(msg.payload))

def on_subscribe(client,userdata,mid,granted_qos):
    logging.ERROR("Subscription succesful!");

def on_unsubscribe(client,userdata,mid,granted_qos):
    logging.INFO("unsubscribed")

def on_disconnect(client,userdata,rc):
    logging.info("Client Disconnected");

mqtt_subscriber_client.on_connect = on_connect
mqtt_subscriber_client.on_message = on_message
mqtt_subscriber_client.on_disconnect=on_disconnect
mqtt_subscriber_client.on_unsubscribe=on_unsubscribe

logging.info("Initiating Subscriber Client Connection");

try:
    mqtt_subscriber_client.connect(broker_address, broker_port, 60)
except:
    logging.error("Unable to connect to subscriber")
    mqtt_subscriber_client.loop_stop()
    sys.exit(1)

#mqtt_subscriber_client.loop_start();
mqtt_subscriber_client.loop_forever();

while not mqtt_subscriber_client.connected_flag:
    logging.info("Client-Broker connection in progress")
    time.sleep(1)

(result, mid) = mqtt_subscriber_client.subscribe("tajane1",1)

if (result == 0):
    logging.info("Client subscription succesfully !")
    logging.info("mid : " + str(mid))
    logging.info("Received subscription status " + str(result))
else:
    logging.ERROR("Packet subscription failed !")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# mqtt_subscriber_client.loop_forever();