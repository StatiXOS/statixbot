# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from pyrogram import Client, filters


def register(app: Client):
    @app.on_message(filters.command("start"))
    async def start(client, message):
        await message.reply_text(
            "'Ssup! What would you like me to do?\nUse /help to get a list of all commands and their usage."
        )
