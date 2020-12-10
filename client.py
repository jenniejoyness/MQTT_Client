import paho.mqtt.client as mqtt

Connected = False
broker_address="3.121.41.63"
username = "client1"
password = "0G*XXzzZu_ICwqBf~BQWkwsl"
num_bytes = 4

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:
        print("Connection failed")
        exit(1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #TODO switch or whaatever it was in networks
    if msg.topic == "input_data":
        output = flip_bits(msg.payload)
        client.publish("output_data", output)
    # for testing purposes
    if msg.topic == "output_data":
        print "output_data: " + str(msg.payload)

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")

#TODO - ?? how to define funtion
def on_disconnect(client):
    # look up online
    client.disconnect()
    client.loop_stop()



def flip_bits(input_data):

    num = int(input_data,0)
    first_bit_lit = 1 << ((num_bytes * 8 ) - 1)
    # first bit is '1'
    if num & first_bit_lit:
       flipped = num ^ 0xAAAAAAAA
    else:
        flipped = num ^ 0x55555555

    final_output = input_data + "_" + hex(flipped)

    return final_output


#create new instance
client = mqtt.Client()
client.username_pw_set(username=username,password=password)

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect
#1
client.connect(broker_address, 1883, 60)
#2 TODO HOSTNAME?
client.publish("hostname","somthing")
#3
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
client.subscribe("input_data")
client.subscribe("output_data")

client.loop_forever()#connect to broker
