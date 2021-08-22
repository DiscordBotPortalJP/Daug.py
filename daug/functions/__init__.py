import asyncio
import discord
import io
from discord.abc import Messageable, User
from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from discord.guild import Guild
from discord.member import Member
from discord.message import Message
from functools import wraps
from traceback import TracebackException
from typing import Union


def excepter(func):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            orig_error = getattr(e, 'original', e)
            error_msg = ''.join(TracebackException.from_exception(orig_error).format())
            appinfo = await self.bot.application_info()
            await appinfo.owner.send(f'```python\n{error_msg}\n```')
    return wrapped


def compose_channel_tree(guild: Guild) -> str:
    tree = []
    for category in guild.by_category():
        if category[0] is None:
            tree.append('C#')
        else:
            tree.append(f'C# {category[0].name}')
        for channel in category[1]:
            if isinstance(channel, discord.channel.TextChannel):
                tree.append(f'  T# {channel.name}')
            if isinstance(channel, discord.channel.VoiceChannel):
                tree.append(f'  V# {channel.name}')
    return '\n'.join(tree)


def get_emoji_numbers() -> tuple:
    return ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣')


async def react_numbers(message):
    for emoji in get_emoji_numbers():
        await message.add_reaction(emoji)


async def warn(
    channel: TextChannel,
    author: Union[User, Member],
    message: Message,
    delete_after: int = 10
) -> Message:
    return await channel.send(f'{author.mention} {message}', delete_after=delete_after)


async def dialog(
    bot: Bot,
    message: Message,
    target: Union[User, Member],
    timeout: int = 10,
    emoji_ok: str = '⭕',
    emoji_ng: str = '❌',
) -> bool:
    await message.add_reaction(emoji_ok)
    await message.add_reaction(emoji_ng)

    def check(reaction, user):
        if reaction.message.id != message.id:
            return False
        if user.id != target.id:
            return False
        if str(reaction.emoji) not in (emoji_ok, emoji_ng):
            return False
        return True

    try:
        reaction, _ = await bot.wait_for(
            'reaction_add',
            check=check,
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        await message.delete()
        return False

    await message.delete()
    return str(reaction.emoji) == emoji_ok


async def send_file_from_text(destination: Messageable, text: str, filename: str) -> Message:
    file=discord.File(io.StringIO(text), filename)
    return await destination.send(file=file)
