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

"""create_branch doc string"""

from __future__ import print_function


def create_branch(
    server, branch_name=None, owner=None, options=None, view=None, dryrun=None
):
    """create_branch doc string"""
    commands = ["p4", "branch", "-i"]

    branch_spec = server.fetch_branch(branch_name)

    if isinstance(options, (list, set)):
        options = " ".join(options)

    if isinstance(view, dict):
        view = [f"{k} {v}" for k, v in view.items()]

    if owner:
        branch_spec["Owner"] = owner

    if options:
        branch_spec["Options"] = options

    if view:
        branch_spec["View"] = view

    if dryrun:
        print("-" * 20)
        print(branch_spec)
        print("-" * 20)
    else:
        server.save_branch(branch_spec)


def populate_branch(server, branch_name):
    result = server.run("populate", "-b", branch_name)
    print(result)


def delete_branch(server, branch_name):
    result = server.delete_branch(branch_name)
    print(result)
