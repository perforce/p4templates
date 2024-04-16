#!/usr/bin/env python

"""edit_permissions doc string"""

from __future__ import print_function


def get_protections_table(server):
    raw_protect_list = server.fetch_protect()["Protections"]
    perm_table_list = []

    for entry in raw_protect_list:
        comment = ""
        if "## " in entry:
            entry, comment = entry.split("## ")
        while "  " in entry:
            entry = entry.replace("  ", " ")

        entry_split = [_.replace("\n", "") for _ in entry.split(" ")]

        if len(entry_split) < 5:
            continue

        perm_table_list.append(
            {
                "access": entry_split[0],
                "type": entry_split[1],
                "name": entry_split[2],
                "host": entry_split[3],
                "path": entry_split[4],
                "comment": comment,
            }
        )

    return perm_table_list


def validate_protection(protection):
    if not {"access", "type", "name", "host", "path"}.issubset(set(protection.keys())):
        print(
            "Required protection field missing skipping entry: {}".format(
                protection.get("name", "Invalid")
            )
        )
        return False
    return True


def prepend_protection(protections_table, permission):
    if permission not in protections_table:
        protections_table.insert(0, permission)
    else:
        print("protection already exists in table:", permission, "\n")

    return protections_table


def save_protections_table(protections_table, server, dryrun=0):
    protection_lines = []
    for entry in protections_table:
        entry_line = "{access} {type} {name} {host} {path}".format(
            access=entry["access"],
            type=entry["type"],
            name=entry["name"],
            host=entry["host"],
            path=entry["path"],
        )
        if entry["comment"]:
            entry_line = entry_line + " ## {}".format(entry["comment"])

        protection_lines.append(entry_line)

    if dryrun:
        print("=" * 40)
        print("Projected protection table edits:")
        print(protection_lines)
        print("=" * 40)
    else:
        result = server.save_protect({"Protections": protection_lines})
        print(result[0], "\n")


def append_new_protections(protections, server, dryrun=0):
    existing_protections = get_protections_table(server)
    for protection in protections:
        if validate_protection(protection):
            existing_protections = prepend_protection(existing_protections, protection)
    save_protections_table(existing_protections, server, dryrun)
