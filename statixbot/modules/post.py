# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import json
import logging
from pathlib import Path
from typing import Dict

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from statixbot.Auth import authorized
from statixbot.Module import ModuleBase

from .help import add_cmd

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
                        "Usage: /post <code>&lt;codename&gt;</code> <code>[changelog]</code>",
                        parse_mode=ParseMode.HTML,
                    )
                    return

                codename: str = args[1]
                changelog: str = args[2] if len(args) == 3 else ""

                if codename not in JSON_DATA:
                    await message.reply_text(f"Codename `{codename}` not found in database.")
                    return

                data: Dict = JSON_DATA
                release: Dict = data.get("release", {})
                device: Dict = data.get(codename, {})

                message_text: str = (
                    f"#{codename} #{release.get('branch', 'unknown')}\n"
                    f"New **StatiXOS {release.get('codename', 'UNKNOWN')}** build for **{device.get('manufacturer', 'Unknown')} {device.get('model', 'Unknown')} ({codename})**!\n\n"
                    f"**Maintainer:** {device.get('maintainer', 'Unknown')}\n"
                    f"[Download](https://downloads.statixos.com/{release.get('version', '0')}-{release.get('codename', 'UNKNOWN')}/{codename})"
                )

                if changelog:
                    message_text += f" | [Changelog]({changelog})"

                await client.send_message(
                    chat_id="-1001238532711",
                    text=message_text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
                await message.reply_text("Successfully posted the build to @StatiXOSReleases!")

            except Exception as e:
                log.error(f"Error posting message: {e}")
                await message.reply_text("An error occurred while posting the message.")

        add_cmd(
            "post <code>&lt;codename&gt;</code> <code>[changelog]</code>",
            "Post a new build to @StatiXOSReleases.",
        )
