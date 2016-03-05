#!/usr/bin/python

import platform
import os
import re
import json

if __name__ == "__main__":
    uname = platform.uname()
    platform_dict = {
        "system_name": uname[1],
        "kernel": uname[2],
        "architecture": uname[4]
    }
    package_list = []
    # get installed packages from dpkg
    packages_raw_info = \
        os.popen(
            "dpkg-query -W -f='${binary:Package}\t${Version}\t${Status}\n' | grep \"install ok installed\""
        ).read()
    packages_raw_info = packages_raw_info.split("\n")
    for line in packages_raw_info:
        if line:
            # regex catches {binary:Package} and {Version} from dpkg output
            package_re = re.compile(r"(.+)\t(.+)\t.*")
            package_info = package_re.match(line)
            package_dict = {
                "name": package_info.group(1),
                "version": package_info.group(2)
            }
            package_list.append(package_dict)
    data = {}
    data["platform"] = platform_dict
    data["packages"] = package_list
    json_data = json.dumps(data)
    print json_data
