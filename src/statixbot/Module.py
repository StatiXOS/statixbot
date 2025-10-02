# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import logging
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path
from typing import Type

from pyrogram import Client

log: logging.Logger = logging.getLogger(__name__)


class ModuleBase(ABC):
    @abstractmethod
    async def register(self, app: Client) -> None:
        """Register commands or handlers with the provided app instance."""
        pass


async def load_module(app: Client, module_path: Path) -> None:
    """Load a single module from the given module_path."""
    module_name: str = module_path.stem
    try:
        log.info(f"Loading module: {module_name}")
        module: Type[ModuleBase] = import_module(f"statixbot.modules.{module_name}")
        if not hasattr(module, "Module"):
            log.error(f"Module '{module}' does not have a Module class, cannot load")
        if not issubclass(module.Module, ModuleBase):
            log.warning(f"Module '{module}' does not inherit from ModuleBase class")
        await module.Module().register(app)
    except Exception as e:
        log.error(f"Error loading module {module_name}: {e}")


async def load_modules(app: Client) -> None:
    """Load all modules except the help module, then load the help module last."""
    module_dir: Path = Path(__file__).parent / "modules"
    for module_path in module_dir.glob("*.py"):
        if module_path.stem != "help":
            await load_module(app, module_path)
            continue

    help_module_path: Path = module_dir / "help.py"
    if help_module_path.exists():
        await load_module(app, help_module_path)
