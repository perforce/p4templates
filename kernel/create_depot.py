#!/usr/bin/env python
from __future__ import print_function


def create_depot(
    server, depot_name=None, depot_type="stream", stream_depth="1", dryrun=0
):
    """create_group doc string"""

    existing_depot_names = {_["Depot"] for _ in server.iterate_depots()}

    if depot_name in existing_depot_names:
        print("Depot {} already exists\n".format(depot_name))
        return

    depot_spec = server.fetch_depot(depot_name)

    depot_spec["Type"] = depot_type
    depot_spec["StreamDepth"] = "//{}/{}".format(depot_name, stream_depth)

    if dryrun:
        print("-" * 20, "\n")
        print(depot_spec, "\n")
        print("-" * 20, "\n")
    else:
        result = server.save_depot(depot_spec)
        print(result, "\n")
