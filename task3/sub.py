from paho.mqtt import client as mqtt

broker = "localhost"
port = 1883
topic = "house/topic1"
msg_count = 0
read_data = []

def main():
    client = mqtt.Client("mqtt-sub-1")
    client.connect(broker, port)
    def on_message(client, userdata, message):
        count_avg(float(message.payload.decode()))
    client.on_message = on_message
    client.subscribe(topic)
    client.loop_forever()


def count_avg(num):
    global msg_count
    msg_count += 1
    read_data.append(num)
    if msg_count > 2:
        l = len(read_data)
        print(f"Sliding avg = {round(read_data[l - 1] * 0.6 + read_data[l - 2] * 0.3 + read_data[l - 3] * 0.1, 2)}")

main()
