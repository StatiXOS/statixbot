# Copyright 2024 StatiXOS
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import asyncio
import logging
import os
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from statixbot.Auth import authorized
from statixbot.Database import data, release
from statixbot.Module import ModuleBase

from .help import add_cmd

log: logging.Logger = logging.getLogger(__name__)

HOST: str = "karmakar@65.109.66.101"


async def upload_file(client: Client, message: Message, subdir: str, url: str, codename: str) -> None:
    """Download the given file locally using aria2 and upload it using rsync."""
    download_dir: Path = Path(__file__).parent.parent.parent / "tmp"
    upload_dir: Path = Path(
        f"/home/karmakar/dockerhome/h5ai/{release.get('version')}-{release.get('codename')}/{subdir}"
    )

    progress_msg = await message.reply_text("Downloading file...")
    try:
        aria2c: str = f"aria2c -x 16 -s 16 -d {download_dir} --download-result=hide --summary-interval=0"
        device: Dict = data.get(codename, {})
        changelog_url: str = device.get("changelog", "")
        type: str = subdir.split("/")[1] if len(subdir.split("/")) == 2 else ""

        if type == "changelog.txt" and not changelog_url:
            process = await asyncio.create_subprocess_shell(
                f"{aria2c} https://downloads.statixos.com/{release.get('version')}-{release.get('codename')}/{codename}/changelog.txt",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.wait()
            changelog_file: Path = download_dir / "changelog.txt"
            changelog_file.touch(exist_ok=True)
            aria2c += " -o changelog.txt"

        process = await asyncio.create_subprocess_shell(
            f"{aria2c} {url}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.wait()

        if type == "bootimages":
            filename: str = "*.img"
        elif type == "recoveryimages":
            filename: str = "recovery.img"
        elif type == "changelog.txt" and not changelog_url:
            filename: str = "changelog*.txt"
        elif type == "fastbootimages":
            filename: str = f"statix_{codename}*-????????-{release.get('version')}-v?.*-{release.get('codename')}-img.zip"
        else:
            filename: str = f"statix_{codename}*-????????-{release.get('version')}-v?.*-{release.get('codename')}.zip"

        if not any(download_dir.glob(filename)):
            log.error("No file with matching name(s) found!")
            await progress_msg.edit_text(
                f"An error occurred while downloading the file: No file with matching name(s) found!"
            )
            for file in download_dir.glob("[!.]*"):
                log.info(f"Deleting downloaded file: {file.name}")
                os.remove(file)
            return

        if type == "changelog.txt":
            with open(download_dir / "changelog.txt", "r+") as dest:
                changelog = dest.read()
                dest.seek(0)
                with open(download_dir / "changelog.1.txt", "r") as source:
                    dest.write(source.read())
                    dest.write("\n\n")
                    dest.write(changelog)
            os.remove(download_dir / "changelog.1.txt")

        await progress_msg.edit_text("Uploading file...")
        for file in download_dir.glob(filename):
            if type != "changelog.txt":
                upload_dir: str = str(upload_dir) + "/"
            process = await asyncio.create_subprocess_shell(
                f"rsync -au --chmod=D755,F644 --progress {file} {HOST}:{upload_dir}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.wait()

        for file in download_dir.glob("[!.]*"):
            log.info(f"Deleting downloaded file: {file.name}")
            os.remove(file)

        await progress_msg.edit_text(f"Successfully uploaded the file to [{subdir}](https://downloads.statixos.com/{release.get('version')}-{release.get('codename')}/{subdir})!")
    except Exception as e:
        log.error(f"Error uploading file: {e}")
        await progress_msg.edit_text(f"An error occurred while uploading the file: {e}")


class Module(ModuleBase):
    async def register(self, app: Client) -> None:
        """Register the /upload command."""

        @app.on_message(filters.command("upload"))
        @authorized
        async def upload_handler(client: Client, message: Message):
            args = message.text.split(maxsplit=2)
            if len(args) != 3:
                await message.reply_text(
                    "Usage: /upload <code>&lt;subdir&gt;</code> <code>&lt;url&gt;</code>", parse_mode=ParseMode.HTML
                )
                return

            subdir, url = args[1], args[2]
            codename = subdir.split("/")[0]
            if codename not in data:
                await message.reply_text(f"Codename `{codename}` not found in database.")
                return

            await upload_file(client, message, subdir, url, codename)

        add_cmd(
            "upload <code>&lt;subdir&gt;</code> <code>&lt;url&gt;</code>",
            "Upload a file to a specified subdirectory on the file server.",
        )
