# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from pyrogram import Client, filters
from pyrogram.types import Message

from statixbot.Module import ModuleBase

from .help import add_cmd


class Module(ModuleBase):
    async def register(self, app: Client) -> None:
        """Register the /start command."""

        @app.on_message(filters.command("start"))
        async def start(client: Client, message: Message) -> None:
            await message.reply_text(
                "'Ssup! What would you like me to do?\nUse /help to get a list of all commands and their usage."
            )

        add_cmd("start", "Starts the bot.")
