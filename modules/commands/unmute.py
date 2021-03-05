from typing import List
from config import IRC
import requests
import ipaddress
import fido
from modules.access import require_permission, Levels
from models import config, SessionManager


@require_permission(level=Levels.OP, message='DENIED!')
async def invoke(bot: fido, channel: str, sender: str, args: List[str]):
    """
    Unmute a nick.
    :param bot: Bot reference
    :param channel: Channel the command is invoked in
    :param sender: Who invoked the command
    :param args: Who to mute
    :return: Reply message.
    """
    if len(args) == 0:
        return "Usage: " + IRC.commandPrefix + "mute <nickname>"
    session = SessionManager().session
    print(f"Processing {args}")
    for arg in args:
        if arg == "":
            continue
        if arg in bot.users:
            print(f"Doing: {arg}")
            mutetime = session.query(config.Config).\
                filter_by(module='channelprotection', key='mutetime').one_or_none()
            print(mutetime)
            await bot.set_mode(channel, "-b", f"~t:{mutetime.value or 6}:*!*@{bot.users[arg]['hostname']}")
            # await bot.rawmsg("MODE", f":#help +b ~t:{mutetime.value or 6}:~q:*!*@{bot.users[arg]['hostname']}")
            await bot.message(channel, f"Unmuted {bot.users[arg]['nickname']}.")
