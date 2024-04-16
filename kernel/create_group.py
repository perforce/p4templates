#!/usr/bin/env python

"""create_group doc string"""

from __future__ import print_function


def create_group(
    server,
    group_name=None,
    description=None,
    max_results=None,
    max_scan_rows=None,
    max_lock_time=None,
    max_open_files=None,
    max_memory=None,
    timeout=None,
    password_timeout=None,
    subgroups=None,
    owners=None,
    users="",
    dryrun=0,
):
    """create_group doc string"""

    existing_group_names = {_["Group"] for _ in server.iterate_groups()}

    if group_name in existing_group_names:
        print("Group {} already exists\n".format(group_name))
        return

    group_spec = server.fetch_group(group_name)

    if description:
        group_spec["Description"] = description
    if max_results:
        group_spec["MaxResults"] = max_results
    if max_scan_rows:
        group_spec["MaxScanRows"] = max_scan_rows
    if max_lock_time:
        group_spec["MaxLockTime"] = max_lock_time
    if max_open_files:
        group_spec["MaxOpenFiles"] = max_open_files
    if max_memory:
        group_spec["MaxMemory"] = max_memory
    if timeout:
        group_spec["Timeout"] = timeout
    if password_timeout:
        group_spec["PasswordTimeout"] = password_timeout
    if subgroups:
        group_spec["Subgroups"] = subgroups
    if owners:
        group_spec["Owners"] = owners
    if users:
        group_spec["Users"] = users

    if dryrun:
        print("-" * 20)
        print(group_spec)
        print("-" * 20)

    else:
        result = server.save_group(group_spec)
        print(result)
