# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os

from dotenv import load_dotenv
from pyrogram import Client


def load_config() -> tuple[int, str, str]:
    """Load environment variables from .env file."""
    load_dotenv(override=True)

    api_id: int = int(os.getenv("API_ID", "0"))
    api_hash: str = os.getenv("API_HASH", "")
    bot_token: str = os.getenv("BOT_TOKEN", "")

    if not all([api_id, api_hash, bot_token]):
        raise ValueError(
            "API_ID, API_HASH, and BOT_TOKEN must be set in the .env file."
        )

    return api_id, api_hash, bot_token


def create_client(api_id: int, api_hash: str, bot_token: str) -> Client:
    """Initialize the Client."""
    return Client("app", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
