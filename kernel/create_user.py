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

"""create_user doc string"""

from __future__ import print_function


def create_user(
    server,
    name,
    email,
    full_name=None,
    job_view=None,
    auth_method=None,
    reviews=None,
    dryrun=0,
):
    """create_user doc string"""

    user_query = server.fetch_user(name)
    if user_query.get("Update"):
        print("User {} already exists\n".format(name))
        return

    if not full_name:
        full_name = name

    if not email:
        email = "@".join([name, full_name])

    user_dict = {
        "User": name,
        "Type": "standard",
        "Email": email,
        "FullName": full_name,
    }

    if auth_method:
        user_dict["AuthMethod"] = auth_method

    if reviews:
        user_dict["Reviews"] = reviews

    if job_view:
        user_dict["JobView"] = job_view

    if dryrun:
        print("-" * 20)
        print(user_dict)

    else:
        result = server.save_user(user_dict, "-f")
        print(result)
