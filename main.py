#!/usr/bin/env python3

from integrations import graph
from integrations import entities
from integrations import client
from integrations.samples import billcollection_generator

# Push data to remote system
billcollection = billcollection_generator(count=1)
node = graph.generate_graph(root=billcollection)
graph.depth_first_search(node=node)


# Get data from remote system
vendor_client = client.Client(endpoint="/vendors")
response = vendor_client.retrieve(1000)

vendor = entities.Vendor.deserialize(response.body)
breakpoint()
