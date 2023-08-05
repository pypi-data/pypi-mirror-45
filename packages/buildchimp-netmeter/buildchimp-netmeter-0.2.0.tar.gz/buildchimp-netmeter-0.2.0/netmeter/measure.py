import time
from netmeter.transport import init_sender
from netmeter.config import Configuration

def measure_once(config_file, metric_name, metric_value):
    sender = None
    try:
        config = Configuration(config_file)

        sender = init_sender(config)
        sender.start()

        now = int(time.time())
        sender.send_raw("%s %s %s" % (metric_name, metric_value, now))
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        if sender is not None:
            sender.stop()

def measure_periodically(config_file, config_extractor, command):
    sender = None
    try:
        while True:
            config = Configuration(config_file)

            prefix = config.prefix
            command_config = config_extractor(config)

            sender = init_sender(config)
            sender.start()

            print(f"Starting command: {command} with sender: {sender}, prefix: {prefix}, and config: {command_config}")
            command(sender, prefix, command_config)

            delay = config.delay
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        if sender is not None:
            sender.stop()
