'''
Program: MQTT_Client
Date: 13.12.20
Developer: Jennie Klein
'''

import paho.mqtt.client as mqtt
import socket
from private import username, password

broker_address = "3.121.41.63"
port = 1883

num_bytes = 4
odd_bits = 0xAAAAAAAA
even_bits = 0x55555555
byte_size = 8



'''
The callback for when the client receives a CONNACK response from the server.
'''
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")

    else:
        print("Connection failed - return code = ", rc)
        exit(1)


'''
The callback for when a PUBLISH message is received from the server.
'''
def on_message(client, userdata, msg):
    if msg.topic == "input_data":
        output = flip_bits(msg.payload)
        client.publish("output_data", output)
    # for testing purposes
    if msg.topic == "output_data" or msg.topic == "hostname":
        print msg.topic + ": " + str(msg.payload)


"""
Flip all odd bits if msb is '1'
Flip all even bits if msb is '0'
"""
def flip_bits(input_data):
    num = int(input_data, 0)
    first_bit_lit = 1 << ((num_bytes * byte_size) - 1)
    # msb is '1'
    if num & first_bit_lit:
        # flip all odd bits
        flipped = num ^ odd_bits
    # msb bit is '0'
    else:
        # flip all even bits
        flipped = num ^ even_bits
    return input_data + "_" + hex(flipped)


'''
Initialize client and set callback functions
'''
def init_client():
    # create new instance
    new_client = mqtt.Client()
    new_client.username_pw_set(username=username, password=password)
    # callback functions
    new_client.on_connect = on_connect
    new_client.on_message = on_message

    return new_client


'''
The client subscribes to every topic in the list_of_sub
'''
def subscriptions(client, list_of_subs):
    for sub in list_of_subs:
        client.subscribe(sub)


if __name__ == "__main__":

    # initialize client and connect
    client = init_client()
    client.connect(broker_address, port)
    # get hostname and publish
    hostname = socket.gethostname()
    client.publish("hostname", hostname)
    # client subscribes to all topics in the list
    topics = ["input_data","output_data"]
    subscriptions(client, topics)
    # listening to servers publications until there is an interrupt
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        exit(0)
