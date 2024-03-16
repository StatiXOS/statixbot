# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
from pathlib import Path
from typing import TypeAlias

# MIT License header
license_header = """\
# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
"""

StatusIsOk: TypeAlias = bool


def add_license_header(file_path) -> StatusIsOk:
    with open(file_path, "r+") as f:
        content = f.read()
        if license_header in content:
            return False
        f.seek(0, 0)
        f.write(license_header.lstrip("\n") + "\n" + content)
    return True


for file in Path(".").rglob("*.py"):
    if add_license_header(file):
        print(f"-> License header added to '{file}'")
    else:
        print(f"-> License header already exists in '{file}'")
