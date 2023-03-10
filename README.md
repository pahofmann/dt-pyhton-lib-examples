# Examples for the Dynatrace Python API Client library

Python scripting examples for the Dynatrace API utilizing the great [Dynatrace Python API Client](https://github.com/dynatrace-oss/api-client-python) from the Dynatrace OSS team.

## Requirements

Requeired librarys can be installed via pip.

```
# The Dynatrace Python API Client library
~$ pip install dt

# For the graph in example 1
~$ pip install matplotlib
```

## Example 1: Get Host Unit consumption per Host Group from multiple Environments

While the UI has an overview and there are metrics for HU consumption, you can't get it by Host Group.

This example shows a quick script to get the HU consumption across multiple environments by host group as CSV and Graph.
It utilizes the *Environment v1 Smartscape Topology - Hosts* API.

## Example 2: Create extension endpoints from CSV

If you don't have config as code yet, this can be a quick way to multiply configuration.

This example shows how to create extension endpoints for the [Port Check Extesnion](https://github.com/Dynatrace/dynatrace-api/tree/master/third-party-synthetic/active-gate-extensions/extension-third-party-port) based on a csv list of servers.
