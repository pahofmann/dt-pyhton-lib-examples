#! /usr/bin/python
from dynatrace import Dynatrace
import csv

# Create dynatrace API client
dtORP = Dynatrace(
    "https://YOURENVID.live.dynatrace.com/",
    "dt0c01.PUBLIC.PRIVATE",
)


# Properties for the extensions
# Can be found in plugin.json
properties = {
    "api_token": "superSecretToken",
    "api_url": "https://YOURENVID.live.dynatrace.com",
    "failure_count": "1",
    "frequency": "1",
    "log_level": "INFO",
    "proxy_address": "",
    "proxy_password": "",
    "proxy_username": "",
    "test_location": "testLocation",
    "test_name": "",
    "test_step_name": "",
    "test_target_hosts": "127.0.0.1",
    "test_target_ports": "",
}

# Workaround to get AG instance from existing test
instance = dtORP.extensions.get_instance(
    "custom.remote.python.thirdparty_port", "EXISTINGTESTID"
)
pluginAG = instance.active_gate

# Open serverlist csv
with open("serverlist.csv", "r") as serverlist:
    serverReader = csv.reader(serverlist, delimiter=";")

    # Skip header line
    next(serverReader)

    # Iterate throgh all servers
    for server in serverReader:
        # Overwrite properties that change per server
        properties["test_target_hosts"] = server[1]
        properties["test_target_ports"] = server[2]
        properties["frequency"] = server[3]

        # Create plugin endpoint instance
        # Plugin id can be found in plugin.json
        pluginInstance = dtORP.extensions.create_instance(
            "custom.remote.python.thirdparty_port",
            properties,
            endpoint_name=server[0],
            activegate=pluginAG,
            enabled=False,
        )

        # Post plugin endpoint instance to server
        dtORP.extensions.post_instance(pluginInstance)
