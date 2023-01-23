#! /usr/bin/python
from dynatrace import Dynatrace
import csv
import matplotlib.pyplot as plt
from typing import List

# Create dynatrace API clients
dtClient1 = Dynatrace(
    "https://YOURENVID.live.dynatrace.com/",
    "dt0c01.PUBLIC.PRIVATE",
)
dtClient2 = Dynatrace(
    "https://YOURENVID.live.dynatrace.com/",
    "dt0c01.PUBLIC.PRIVATE",
)

# Small helper to generate a pie chart with Host Units per Host Group
def generatePieChart(filename: str, huConsumptions: List, labels: List):
    huPlot, ax1 = plt.subplots()
    ax1.pie(
        huConsumptions, labels=labels, autopct="%1.1f HU", shadow=True, startangle=90
    )
    ax1.axis("equal")

    huPlot.savefig(f"{filename}.png")


# List with clients for all environments
envs = [dtClient1, dtClient2]

# List containing the Host Group Names
hostGroups = []

# List containing the Host Unit consumptions for Host Groups
# Each index will contain the Host Units for the corresponding index in the hostGroups list.
huComsumptions = []

# Iterate through environments to get all hosts from multiple environments
for env in envs:
    # Get a list of all hosts in the current environment
    hosts = env.smartscape_hosts.list()

    # Interate through the hosts
    for host in hosts:
        # If the current hostgroup is already in the list, add the hosts HU to the huConsumption list
        if host.host_group.name in hostGroups:
            huComsumptions[
                hostGroups.index(host.host_group.name)
            ] += host.consumed_host_units
        # If the hostgroup is not in the list add it and the consumed HU of the current host
        else:
            hostGroups.append(host.host_group.name)
            huComsumptions.append(host.consumed_host_units)

# Write a csv file with a line for each Host Group
with open('huConsumption.csv', 'w') as file:
    # create the csv writer
    writer = csv.writer(file)

    for i in range(len(hostGroups)):
        file.write("{},{}\n".format(hostGroups[i], huComsumptions[i]))

    file.close()

# Generate a pie chart with a slice for each Host Group
generatePieChart("huPie", huComsumptions, hostGroups)

