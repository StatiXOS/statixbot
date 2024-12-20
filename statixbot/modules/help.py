# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Dict

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from statixbot.Module import ModuleBase

cmds: Dict[str, str] = {}


def add_cmd(cmd: str, desc: str) -> None:
    """Add command to the help module."""
    cmds[cmd] = desc


class Module(ModuleBase):
    async def register(self, app: Client) -> None:
        """Register the /help command."""

        @app.on_message(filters.command("help"))
        async def help_handler(client: Client, message: Message) -> None:
            help_text: str = "<b>Available commands:</b>\n"
            for command, description in cmds.items():
                help_text += f"- /{command}: {description}\n"
            await message.reply_text(help_text, parse_mode=ParseMode.HTML)

        add_cmd("help", "Sends this message.")
