# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import json
import logging
from pathlib import Path
from typing import Dict

log: logging.Logger = logging.getLogger(__name__)

JSON_FILE_PATH: Path = Path(__file__).parent.parent.parent / "maintainers.json"


def load_json_data(file_path: Path) -> Dict:
    """Load JSON data from a file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        log.error(f"Error decoding JSON file {file_path}: {e}")
        return {}
    except Exception as e:
        log.error(f"Unexpected error while loading JSON file {file_path}: {e}")
        return {}


JSON_DATA: Dict = load_json_data(JSON_FILE_PATH)
data: Dict = JSON_DATA
release: Dict = data.get("release", {})
