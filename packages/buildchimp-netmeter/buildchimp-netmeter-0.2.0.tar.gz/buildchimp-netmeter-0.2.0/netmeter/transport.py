import mulay.mqtt as mqtt
import mulay.amqp as amqp
import mulay.carbon as carbon
import mulay.console as console

from netmeter.config import (Configuration, AMQP, MQTT, CARBON, CONSOLE)

def init_sender(config):
    if config.sender == MQTT:
        sender = mqtt.Sender(config.get_mqtt())
    elif config.sender == AMQP:
        sender = amqp.Sender(config.get_amqp())
    elif config.sender == CARBON:
        sender = carbon.Sender(config.get_carbon())
    elif config.sender == CONSOLE:
        sender = console.Sender({})
    else:
        raise Exception(f"Unknown sender type: '{config.sender}")

    print(f"Started sender: {config.sender}, instance: {sender}")
    return sender

def init_relay(config, sender):
    relay_type = config.get_relay_type()
    if relay_type == MQTT:
        relay = mqtt.Relay(config.get_mqtt(), sender)
    elif relay_type == AMQP:
        relay = amqp.Relay(config.get_amqp(), sender)
    else:
        raise Exception(f"Unknown relay type: '{relay_type}")

    print(f"Started relay: {relay_type}, instance: {relay}")
    return relay

