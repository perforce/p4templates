#!/usr/bin/env python

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
