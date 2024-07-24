# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import logging
import os
from importlib import import_module
from typing import Any

from pyrogram import Client

log: logging.Logger = logging.getLogger(__name__)


def load_modules(app: Client) -> None:
    module_dir: str = os.path.join(os.path.dirname(__file__), "modules")
    for filename in os.listdir(module_dir):
        if filename.endswith(".py") and filename != "help.py":
            module_name: str = filename[:-3]
            try:
                log.info(f"Loading module: {module_name}")
                module: Any = import_module(f"src.modules.{module_name}")
                module.register(app)
            except Exception as e:
                log.error(f"Error loading module {module_name}: {e}")

    # Load the help module after other modules
    try:
        log.info("Loading help module")
        help_module: Any = import_module("src.modules.help")
        help_module.register(app)
    except Exception as e:
        log.error(f"Error loading help module: {e}")
