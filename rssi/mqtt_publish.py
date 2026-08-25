import paho.mqtt.client as mqtt


class StatePublisher:
    def __init__(self, device_id, broker, port =1883):
        self.topic = f"presence/{device_id}/rssi"
        self.client = mqtt.Client(client_id=device_id)
        self.client.connect(broker, port, keepalive=30)
        self.client.loop_start()

    def publish(self, state):
        self.client.publish(self.topic, state, retain=True)