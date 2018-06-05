import paho.mqtt.client as mqtt
import os.path

certificates_path = "/user/share/certificates"
ca_certificate = os.path.join(certificates_path, "ca.crt")
client_certificate = os.path.join(certificates_path, "device001.crt")
client_key = os.path.join(certificates_path, "device001.key")

mqtt_server_host = "localhost"
mqtt_server_port = 8883
mqtt_keepalive = 60


def on_connect(client, userdata, rc):
    print("Connect result: {}".format(mqtt.connack_string(rc)))
    client.subscribe("test/drone01")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))


def on_message(client, userdata, msg):
    payload_string = msg.payload.decode('utf-8')
    print("Topic: {}. Payload: {}".format(msg.topic, str(msg.payload), payload_string))

if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.tls_set(ca_certs=ca_certificate, certfile=client_certificate, keyfile=client_key)
    client.connect_async(host=mqtt_server_host, port=mqtt_server_port, keepalive=mqtt_keepalive)
    client.loop_forever()
