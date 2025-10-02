# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import logging
from typing import Dict

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from str_to_bool import str_to_bool

from statixbot.Auth import authorized
from statixbot.Database import data, release
from statixbot.Module import ModuleBase

from .help import add_cmd

log: logging.Logger = logging.getLogger(__name__)


class Module(ModuleBase):
    async def register(self, app: Client) -> None:
        """Register the /post command."""

        @app.on_message(filters.command("post"))
        @authorized
        async def post_message(client: Client, message: Message) -> None:
            try:
                args: str = message.text.split(maxsplit=2)
                if len(args) < 2:
                    await message.reply_text(
                        "Usage: /post <code>&lt;codename&gt;</code> <code>[changelog (bool)]</code>",
                        parse_mode=ParseMode.HTML,
                    )
                    return

                codename: str = args[1]
                postcl: bool = str_to_bool(args[2]) if len(args) == 3 else True

                if codename not in data:
                    await message.reply_text(
                        f"Codename `{codename}` not found in database."
                    )
                    return

                device: Dict = data.get(codename, {})
                changelog: str = device.get("changelog", "")
                download: str = f"https://downloads.statixos.com/{release.get('version', '0')}-{release.get('codename', 'UNKNOWN')}/{codename}"

                message_text: str = (
                    f"#{codename} #{release.get('branch', 'unknown')}\n"
                    f"New **StatiXOS {release.get('codename', 'UNKNOWN')}** build for **{device.get('manufacturer', 'Unknown')} {device.get('model', 'Unknown')} ({codename})**!\n\n"
                    f"**Maintainer:** {device.get('maintainer', 'Unknown')}\n"
                    f"[Download]({download})"
                )

                if postcl:
                    if changelog:
                        message_text += (
                            f" | [Changelog](https://xdaforums.com/t/{changelog})"
                        )
                    else:
                        message_text += f" | [Changelog]({download}/changelog.txt)"

                await client.send_message(
                    chat_id="-1001238532711",
                    text=message_text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
                await message.reply_text(
                    "Successfully posted the build to @StatiXOSReleases!"
                )

            except Exception as e:
                log.error(f"Error posting message: {e}")
                await message.reply_text("An error occurred while posting the message.")

        add_cmd(
            "post <code>&lt;codename&gt;</code> <code>[changelog (bool)]</code>",
            "Post a new build to @StatiXOSReleases.",
        )
