import sys
import subprocess
import paho.mqtt.client as mqtt
import time
import logging

broker_address="192.168.0.47";
#broker_address="146.115.80.244";
broker_port="1883";
publish_return=();
logging.basicConfig(level=logging.ERROR)
#level : logging.INFO or logging.DEBUG or logging.WARNING


mqtt.Client.connected_flag = False;
mqtt_client = mqtt.Client(client_id="sensor_pub_1", clean_session=False, userdata=None)

def on_publish(mqtt_client,useradata,received_mid):
    logging.info ("Message packet published sucessfully")
    logging.info("mid: " + str(received_mid))


def on_connect(mqtt_client, userdata, flags, rc):
    if rc==0:
        mqtt_client.connected_flag=True
        logging.info ("Client connected to Broker")
    else:
        logging.info("Bad connection returned code =",rc)
        mqtt_client.loop_stop()

def on_disconnect(client,userdata,rc):
    logging.info("Client Disconnected");
    logging.error("Client Reconnection initiated");
    mqtt_client.connect(broker_address, broker_port, 60)
    mqtt_client.loop_start()
    data_generator(mqtt_client)
    #initiate_client_broker_connection();



def on_log(client,userdat,level,buffer):
    logging.info("on_log callback")
    logging.info(buffer)

def on_subscribe(client,userdata,mid,granted_qos):
    logging.info("subscribed")

def on_message(client,userdata,message):
    subscribed_topic=message.topic
    msg_body=str(message.payload.decode("utf-8"))
    msg_recived="Received Message :"+msg_body
    logging.info(msg_recived)

def data_generator(mqtt_client):
    counter=0
    while counter != 1000:
        #publish_return=mqtt_client.publish("tajane",counter,0,True)
        systemParams=subprocess.check_output([sys.executable, "getGPUTemp.py"])
        systemParam=systemParams.split("=")[1].split("'")[0]
        # systemParam=counter;
        (result, mid) = mqtt_client.publish("tajanep", systemParam, 0, True)
        if (result == 0):
            logging.error("Packet published succesfully !")
            logging.error("counter : "+str(counter))
            logging.info("mid : " + str(mid))
            logging.info("Received publish status " + str(result))
        else:
            logging.error("Packet publish failed !")
            # publish(topic, payload=None, qos=0, retain=Falsae)
        counter = counter + 1
        time.sleep(2)
# def reset():
#     ret=mqttc.publish("tajane","",0,True)


mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log
mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_message = on_message

mqtt_client.connect(broker_address, broker_port, 60)
mqtt_client.loop_start()

while not mqtt_client.connected_flag:
    logging.info("Client-Broker connection in progress")
    time.sleep(1)

# mqtt.Client.connected_flag=False;
# mqtt_client = mqtt.Client(client_id="sensor_pub_1", clean_session=False, userdata=None)

#mqttc=initiate_client_broker_connection();
data_generator(mqtt_client)
