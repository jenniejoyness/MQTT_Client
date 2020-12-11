import paho.mqtt.client as mqtt

Connected = False
broker_address = "3.121.41.63"
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
        print("Connection failed - returned code=", rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    # TODO switch or whaatever it was in networks
    if msg.topic == "input_data":
        output = flip_bits(msg.payload)
        client.publish("output_data", output)
    # for testing purposes
    if msg.topic == "output_data" or msg.topic == "hostname":
        print "published data: " + str(msg.payload)


def on_publish(client, userdata, result):
    print("data published \n")


# TODO - ?? how to define funtion
def on_disconnect(client):
    # look up online
    # client.loop_stop()
    client.disconnect()


def flip_bits(input_data):
    input_data = "0x33c51bd1"
    num = int(input_data, 0)
    first_bit_lit = 1 << ((num_bytes * 8) - 1)
    # msb is '1'
    if num & first_bit_lit:
        flipped = num ^ 0xAAAAAAAA
     # msb bit is '0'
    else:
        flipped = num ^ 0x55555555

    final_output = input_data + "_" + hex(flipped)

    return final_output


# initialize client and set callback functions

def init_client():
    # create new instance
    new_client = mqtt.Client()
    new_client.username_pw_set(username=username, password=password)
    # callback functions
    new_client.on_connect = on_connect
    new_client.on_message = on_message
    new_client.on_publish = on_publish
    new_client.on_disconnect = on_disconnect
    return new_client

def subscribe_to_subscriptions(client, list_of_subs):
    for sub in list_of_subs:
        client.subscribe(sub)


if __name__ == "__main__":

    client = init_client()
    # connect to broker
    client.connect(broker_address, 1883, 60)
    # 2 TODO HOSTNAME?
    # publish hostname to server

    import socket
    hostname = socket.gethostname()
    client.publish("hostname", hostname)
    # 3
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    subscriptions = ["input_data","hostname"]
    subscribe_to_subscriptions(client, subscriptions)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        # TODO
        # on_disconnect(client)
        exit(0)
