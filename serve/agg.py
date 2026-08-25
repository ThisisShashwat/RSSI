import json
import time

import paho.mqtt.client as mqtt

from zones_config import DEVICES, MQTT_BROKER, MQTT_PORT

TRAIL_LOG = "trail.jsonl"

last_state = {}
zones = sorted(set(DEVICES.values()))

client = mqtt.Client(client_id="presence-agg")

def publish_discovery():

    for dev_id in DEVICES:

        client.publish(
            f"homeassistant/binary_sensor/{dev_id}_presence/config",
            json.dumps({
                "name":f"{dev_id}_presence",
                "state_topic": f"presence/{dev_id}/state",
                "payload_on" : "moving",
                "payload_off" : "absent",
                "device_class": "motion",
                "unique_id":f"{dev_id}_presence",
                "device": {"identifiers": [dev_id], "name": dev_id},

            }),
            retain=True,
        )

    for zone in zones:
        client.publish(
            f"homeassistant/binary_sensor/{zone}_occupancy/config",
            json.dumps({
                "name": f"{zone}_occupancy",
                "state_topic": f"zone/{zone}/occupancy",
                "payload_on": "occupied",
                "payload_off": "clear",
                "device_class": "occupancy",
                "unique_id": f"{zone}_occupancy",
            }),
            retain=True,

        )


def zone_state(zone):
    states = [last_state[d] for d, z in DEVICES.items() if z == zone and d in last_state]

    return "occupied" if any(s == "moving" for s in states) else "clear"

def log_trail(dev_id, zone, state):
    with open("trail.jsonl", "a") as f:
        f.write(json.dumps({
            "ts": time.time(),
            "device": dev_id,
            "zone": zone,
            "state": state,
        }) + "\n")

def on_message(client, userdate, msg):
    dev_id = msg.topic.split("/")[1]
    if dev_id not in DEVICES:
        return

    state = msg.payload.decode()
    if last_state.get(dev_id) == state:
        return

    last_state[dev_id] = state
    zone = DEVICES[dev_id]

    client.publish(f"zone/{zone}/occupancy", zone_state(zone), retain=True)

    log_trail(dev_id, zone, state)


client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=30)
client.subscribe("presence/+/state")
publish_discovery()
client.loop_forever()
