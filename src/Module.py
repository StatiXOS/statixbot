# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
from importlib import import_module


def load_modules(app):
    module_dir = os.path.join(os.path.dirname(__file__), "modules")
    for filename in os.listdir(module_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                module = import_module(f"src.modules.{module_name}")
                module.register(app)
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")
