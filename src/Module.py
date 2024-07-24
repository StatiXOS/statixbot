# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import logging
import os
from importlib import import_module

log: logging.Logger = logging.getLogger(__name__)


def load_modules(app):
    module_dir = os.path.join(os.path.dirname(__file__), "modules")
    for filename in os.listdir(module_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                log.info(f"Loading module: {module_name}")
                module = import_module(f"src.modules.{module_name}")
                module.register(app)
            except Exception as e:
                log.error(f"Error loading module {module_name}: {e}")
