#!/usr/bin/env python

#    p4templates - custom tooling to quickly create Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2024 Perforce Software, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
