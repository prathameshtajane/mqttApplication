import sys
import subprocess
import paho.mqtt.client as mqtt
import time
import logging

#broker_address="192.168.0.47"
broker_address="146.115.80.244";
broker_port="1883";
publish_return=();
logging.basicConfig(level=logging.ERROR)
#level : logging.INFO or logging.DEBUG or logging.WARNING

mqtt.Client.connected_flag = False;
mqtt_sensor_client = mqtt.Client(client_id="sensor_pub_sub_1", clean_session=False, userdata=None)


def on_connect(mqtt_client, userdata, flags, rc):
    if rc==0:
        mqtt_client.connected_flag=True
        print("Connection sucess !")
        logging.info ("Client connected to Broker")
        try:
            logging.error("start eith subscription ")
            mqtt_sensor_client.subscribe("tajanep");
            # logging.ERROR("Connection successful !");
        except Exception as e:
            logging.error("Error during subscription ")
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
    #mqtt_sensor_client.loop_start()
    mqtt_sensor_client.loop_forever();
    # data_generator(mqtt_client)
    # initiate_client_broker_connection();

def on_log(client,userdat,level,buffer):
    logging.info("on_log callback")
    logging.info(buffer)

def on_publish(mqtt_client,useradata,received_mid):
    logging.info ("Message packet published sucessfully")
    logging.info("mid: " + str(received_mid))

def on_subscribe(client,userdata,mid,granted_qos):
    print("subscription success !")
    #logging.INFO("subscribed")

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
#mqtt_sensor_client.loop_start();

# while not mqtt_sensor_client.connected_flag:
#     logging.info("Client-Broker connection in progress")
#     time.sleep(1)
#
# print("start with subscribe")
# (result, mid) = mqtt_sensor_client.subscribe("tajanep",1)

# if (result == 0):
#     logging.info("Client subscription succesfully !")
#     logging.info("mid : " + str(mid))
#     logging.info("Received subscription status " + str(result))
# else:
#     logging.ERROR("Packet subscription failed !")

systemParam="Sender Message !"

(result, mid) = mqtt_sensor_client.publish("someTopic", systemParam, 0, True)
if (result == 0):
    logging.info("Packet published succesfully !")
    logging.info("mid : " + str(mid))
    logging.info("Received publish status " + str(result))
else:
    logging.error("Packet publish failed !")

#mqtt_sensor_client.loop_forever()