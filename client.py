import paho.mqtt.client as mqtt

broker_address="3.121.41.63"
username = "client1"
password = "0G*XXzzZu_ICwqBf~BQWkwsl"
num_bytes = 4

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("input_data")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    flip_bits(msg.payload)

def flip_bits(input_data):
    input_data = "0xf0ab22a2"


    num = int(input_data,0)

    first_bit_lit = 1 << ((num_bytes * 8 ) - 1)
    # first bit is '1'
    if num & first_bit_lit:
       flipped = num ^ 0xAAAAAAAA
    else:
        flipped = num ^ 0x55555555
    final_output = input_data + "_" + hex(flipped)

    print(final_output)


#create new instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#connect to broker
#client.connect(broker_address)
client.username_pw_set(username=username,password=password)
client.connect(broker_address, 1883, 60)
client.publish("hostname","OFF")
client.loop_forever()