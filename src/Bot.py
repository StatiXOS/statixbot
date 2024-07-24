# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os

from dotenv import load_dotenv
from pyrogram import Client

from .Module import load_modules

# Load environment variables from .env file
load_dotenv(override=True)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN must be set in the .env file.")

# Initialize the Client
app = Client("app", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def main():
    load_modules(app)
    app.run()
