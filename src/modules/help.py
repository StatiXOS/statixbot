# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from pyrogram import Client, filters

# This dictionary will store commands and their descriptions
cmds = {}


def register(app):
    # Register the /help command
    @app.on_message(filters.command("help"))
    async def help_handler(client, message):
        help_text = "Available commands:\n"
        for command, description in cmds.items():
            help_text += f"/{command}: {description}\n"
        await message.reply_text(help_text)


def add_cmd(cmd, desc):
    """Add command to the help module."""
    cmds[cmd] = desc
