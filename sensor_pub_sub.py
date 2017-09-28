import sys
import subprocess
import paho.mqtt.client as mqtt
import time
import logging
from readConfigFile import configs

# broker_address="192.168.0.47"
# #broker_address="146.115.80.244";
# broker_port="1883";
# sub_topic="tajanep";
# pub_topic="hub1";
# pub_msg="Sender Message !"

broker_address=configs['mqtt_broker_ip_address']
broker_port=configs['mqtt_broker_port']
sub_topic=configs['subscriber_topic']
pub_topic=configs['publisher_topic']
pub_msg="Sender Message !"

publish_return=();
logging.basicConfig(level=logging.ERROR)
#level : logging.INFO or logging.DEBUG or logging.WARNING

mqtt.Client.connected_flag = False;
mqtt_sensor_client = mqtt.Client(clean_session=True, userdata=None)


def on_connect(mqtt_client, userdata, flags, rc):
    if rc==0:
        mqtt_client.connected_flag=True
        logging.info("Sensor connected to broker.")
        try:
            logging.info("Initiating subscription process.")
            mqtt_sensor_client.subscribe(sub_topic);
        except Exception as e:
            logging.error("Subscription process failed.topic :"+sub_topic)
            logging.error(e);
            mqtt_sensor_client.loop_stop();
            sys.exit(1);
    else:
        logging.info("Bad connection returned code =",rc)
        mqtt_client.loop_stop()

def on_disconnect(client,userdata,rc):
    logging.info("Client Disconnected");
    logging.error("Client Reconnection initiated");
    mqtt_sensor_client.connect(broker_address, broker_port, 60)
    mqtt_sensor_client.loop_forever();


def on_log(client,userdat,level,buffer):
    logging.info("on_log callback")
    logging.info(buffer)

def on_publish(mqtt_client,useradata,received_mid):
    logging.info ("Message packet published sucessfully")
    logging.info("mid: " + str(received_mid))

def on_subscribe(client,userdata,mid,granted_qos):
    logging.info("Subscription succesful")
    logging.info("Subscription topic :" + sub_topic)
    logging.info("Subscription granted QoS :" + str(granted_qos))

def on_unsubscribe(client,userdata,mid,granted_qos):
    logging.info("unsubscribed")

def on_disconnect(client,userdata,rc):
    logging.info("Client Disconnected");

def on_message(client, userdata, msg):
    print("Received Packet")
    print("Counter :"+str(msg.payload))

mqtt_sensor_client.on_connect = on_connect
mqtt_sensor_client.on_disconnect=on_disconnect
mqtt_sensor_client.on_log=on_log
mqtt_sensor_client.on_publish = on_publish
mqtt_sensor_client.on_subscribe = on_subscribe
mqtt_sensor_client.on_unsubscribe = on_unsubscribe
mqtt_sensor_client.on_disconnect = on_disconnect
mqtt_sensor_client.on_message = on_message


try:
    print("start with connect")
    mqtt_sensor_client.connect(broker_address, broker_port, 60)
except:
    logging.error("Unable to connect to MQTT Broker")
    mqtt_sensor_client.loop_stop()
    sys.exit(1)

mqtt_sensor_client.loop_forever();

(result, mid) = mqtt_sensor_client.publish(pub_topic, pub_msg, 0, True)
if (result == 0):
    logging.info("Packet published succesfully !")
    logging.info("mid : " + str(mid))
    logging.info("Received publish status " + str(result))
else:
    logging.error("Packet publish failed !")