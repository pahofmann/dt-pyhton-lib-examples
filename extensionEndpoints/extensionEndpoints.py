#! /usr/bin/python
from dynatrace import Dynatrace
import csv

# Create dynatrace API client
dtORP = Dynatrace(
    "https://YOURENVID.live.dynatrace.com/",
    "dt0c01.PUBLIC.PRIVATE",
)

# Properties for the extension, as some might be shared between all endpoints
# Can be found in plugin.json of the extensions .zip bundle  
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

# Instance of the plugin enabled Active Gate the extension should run on
# The extension needs to be present on the AG
# You can use a specific AG, we just use the first one here
# Get a list of all ActiveGates with the plugin module enabled
pluginAGs = dtORP.extensions.list_activegate_extension_modules()._get_next_page()

# Error if there are none, else use the first one
if len(pluginAGs) < 1:
    print("No Activegates with enabled Plugin Module found.")
else:
    pluginActiveGate = pluginAGs[0]


# Open serverlist csv
with open("serverList.csv", "r") as serverList:
    serverReader = csv.reader(serverList, delimiter=";")

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
            activegate=pluginActiveGate,
            enabled=False,
        )

        # Post plugin endpoint instance to server
        dtORP.extensions.post_instance(pluginInstance)
