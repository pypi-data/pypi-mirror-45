#!/usr/bin/env python2

from setuptools import setup, find_packages

version='0.1.0'

setup(
    zip_safe=True,
    name='buildchimp-netmeter',
    version=version,
    description="Metrics for network connectivity",
    long_description="Measurements to be pushed into Graphite/Elastic and monitor network connectivity",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Programming Language :: Python :: 3",
      "Topic :: Utilities",
    ],
    keywords='graphite metrics monitoring network mqtt amqp carbon',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/jdcasey/buildchimp-netmeter',
    license='GPLv3+',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
      'mulay',
      'speedtest-cli',
      'click',
      'ruamel.yaml'
    ],
    test_suite="tests",
    entry_points={
      'console_scripts': [
        'netmeter-fping = netmeter.command:fping',
        'netmeter-speedtest = netmeter.command:speedtest',
        'netmeter-send = netmeter.command:send',
        'netmeter-relay = netmeter.command:relay',
        'netmeter-init = netmeter.command:init'
      ]
    }

)

