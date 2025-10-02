# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import asyncio
from pyrogram import Client, idle

from . import Bot, Logging as Logging
from .Module import load_modules


async def amain() -> None:
    api_id, api_hash, bot_token = Bot.load_config()
    app: Client = Bot.create_client(api_id, api_hash, bot_token)
    await load_modules(app)
    await app.start()
    await idle()
    await app.stop()


def main() -> None:
    asyncio.run(amain())
