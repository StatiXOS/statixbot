# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os

from pathlib import Path

SCRIPT = r"""#!/bin/sh
set -o noglob

python3 scripts/install_hook.py || python scripts/install_hook.py

poetry run black .

files=$(git diff --cached --name-only)

if [ -n "$files" ]; then
    for file in $files; do
        if [ -f "$file" ]; then
            git add "$file"
        fi
    done
fi"""


def main() -> None:
    print("Installing pre-commit hook")
    with open(".git/hooks/pre-commit", "w") as f:
        f.write(SCRIPT)

    print(f"Installing dev dependencies (for black)")
    os.system("poetry install --with dev")
    Path(".git/hooks/pre-commit").chmod(0o700)


if __name__ == "__main__":
    main()
