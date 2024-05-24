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

"""edit_permissions doc string"""

from __future__ import print_function


def get_typemap(server):
    type_dict = {}
    for entry in server.fetch_typemap().get("TypeMap", []):
        type_key, type_value = entry.split(" ")
        if type_key not in type_dict:
            type_dict[type_key] = set()
        type_dict[type_key].add(type_value)

    return type_dict


def add_type(type_dict, type_key, type_value):
    if type_key not in type_dict:
        type_dict[type_key] = set()

    type_dict[type_key].add(type_value)
    return type_dict


def save_typemap(type_dict, server, dryrun):
    typemap = {
        "TypeMap": [
            " ".join([file_type, file_path])
            for file_type in sorted(type_dict)
            for file_path in sorted(type_dict[file_type])
        ]
    }
    if dryrun:
        print("=" * 40)
        print("Projected Typemap edits:")
        print(typemap)
        print("=" * 40)
    else:
        result = server.save_typemap(typemap)
        print(result[0], "\n")


def append_new_typemap_entry(type_entries, server, dryrun=0):
    existing_types = get_typemap(server)
    for file_type in type_entries:
        for file_path in type_entries[file_type]:
            existing_types = add_type(existing_types, file_type, file_path)

    save_typemap(existing_types, server, dryrun)
