from ruamel.yaml import YAML

DEFAULT_DELAY = 30

TARGETS = 'targets'
HOST = 'host'
PORT = 'port'
USER = 'user'
PASSWORD = 'password'
URL = 'url'
QUEUE = 'queue'

DELAY = 'delay'
PREFIX = 'prefix'

SENDER = 'send'
RECEIVER = 'recv'

CARBON = 'carbon'
MQTT = 'mqtt'
AMQP = 'amqp'
CONSOLE = 'console'
FPING = 'fping'

def print_init():
    print(f"""
# Carbon is used to send to GraphiteDB
# Console is used for debugging another sender + bus configuration
{SENDER}: (mqtt | amqp | carbon | console)

# {RECEIVER} is only useful for relay configurations
{RECEIVER}: (mqtt | amqp)

{PREFIX}: mynode                  # Prefix is the metric name prefix, usually node-specific
{DELAY}: 30                       # Speedtest / fping will loop forever with this delay

# If you're configuring a fping reporter, you'll need this section
{FPING}: 
    {TARGETS}: 
    - 192.168.1.1
    - 8.8.8.8
    - github.com

# If you want to relay metrics to a GraphiteDB, you need this section
{CARBON}:
    # Carbon is not needed in 'pure' remote-sender configurations
    # Carbon would be well-suited to measurement / delivery without intermediary bus
    {HOST}: my.graphite-server.com
    {PORT}: 2023

# If you're reporting metrics over a MQTT bus, you need this
{MQTT}:
    {HOST}: m16.cloudmqtt.com
    {PORT}: 20966
    {USER}: blah
    {PASSWORD}: blah

# If you're reporting metrics over a AMQP bus, you need this
{AMQP}:
    {URL}: amqp://<user>:<pass>@my.amqp-server.com/<instance>
    {QUEUE}: some-queue
""")

def get_fping_targets(self, config):
    return config.get(TARGETS) or ['8.8.8.8']

class Configuration(object):
    def __init__(self, config_file):
        with open(config_file) as f:
            self.data = YAML(typ='safe').load(f)
        print(f"Configuration:\n{self.data}")
        self.sender = self.data[SENDER]
        self.prefix = self.data[PREFIX]
        self.delay = int(self.data.get(DELAY)) or DEFAULT_DELAY

    def get_relay_type(self):
        return self.data[RECEIVER]

    def get_mqtt(self):
        return self.data[MQTT]

    def get_carbon(self):
        return self.data[CARBON]

    def get_amqp(self):
        return self.data[AMQP]

    def get_fping(self):
        return self.data[FPING]
