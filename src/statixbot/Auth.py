# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from functools import wraps
from typing import Any

from pyrogram import Client
from pyrogram.types import Message

AUTHORIZED_USERS: set[int] = {
    271913103,  # Anay
    382989527,  # Andrew
    372450085,  # Ledda
    6920687756,  # Pranaya
    415397712,  # Sourajit
    327722191,  # Vaisakh
    1483125984,  # tofu
}


def authorized(func):
    """Decorator to restrict access to authorized users only."""

    @wraps(func)
    async def wrapper(
        client: Client, message: Message, *args: Any, **kwargs: Any
    ) -> None:
        if message.from_user.id in AUTHORIZED_USERS:
            return await func(client, message, *args, **kwargs)

    return wrapper
