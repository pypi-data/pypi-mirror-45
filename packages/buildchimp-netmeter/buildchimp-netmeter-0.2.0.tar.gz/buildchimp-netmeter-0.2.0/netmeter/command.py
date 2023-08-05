import click
import time
from ruamel.yaml import YAML
from speedtest import Speedtest

import netmeter.fping
import netmeter.speedtest
from netmeter.config import print_init
from netmeter.measure import (measure_periodically, measure_once)
import netmeter.transport as transport
from netmeter.config import Configuration

@click.command()
@click.argument('config_file')
def fping(config_file):
    """Use fping to measure network latencies"""
    measure_periodically(config_file, 
                         lambda config: config.get_fping(), 
                         netmeter.fping.fping)


@click.command()
@click.argument('config_file')
def speedtest(config_file):
    """Use speedtest.net client to measure network speeds.
    """
    measure_periodically(config_file, 
                         lambda config: None, 
                         netmeter.speedtest.speedtest)


@click.command()
@click.argument('config_file')
@click.argument('metric_name')
@click.argument('metric_value')
def send(config_file, metric_name, metric_value):
    """Command-line sender for metrics.

    This could be useful for testing a connection, or for calling from 
    a shell script to send a metric established through some external means.
    """
    measure_once(config_file, metric_name, metric_value)


@click.command()
@click.argument('config_file')
def relay(config_file):
    """Command to start a relay service which can read from something like
    MQTT or AMQP, and send to another transport such as MQTT, AMQP, or Carbon.

    Carbon is a transport that will store the metrics read by the relay into
    a GraphiteDB instance.

    MQTT -> MQTT and AMQP -> AMQP are not supported at present, due to 
    the configuration complexity involved.
    """
    config = Configuration(config_file)

    sender = transport.init_sender(config)
    relay = transport.init_relay(config, sender)

    try:
        sender.start()
        relay.start()
    except KeyboardInterrupt:
        print("Shutting down relay")
    finally:
        if relay is not None:
            relay.stop()
        if sender is not None:
            sender.stop()


@click.command()
def init():
    """Print a sample configuration file"""
    print_init()
