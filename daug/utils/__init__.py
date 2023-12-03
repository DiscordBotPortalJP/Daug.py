import asyncio
import aiohttp
import re
import discord
from discord.ext import commands
from constants import COLOUR_EMBED_GRAY
from constants import EMOJI_NUMBERS


def extract_mentions(guild: discord.Guild, text: str) -> list[discord.Member]:
    return [guild.get_member(int(x)) for x in re.findall(r'<@!?([0-9]{15,20})>', text) if guild.get_member(int(x))]


def extract_role_mentions(guild: discord.Guild, text: str) -> list[discord.Role]:
    return [guild.get_role(int(x)) for x in re.findall(r'<@&([0-9]{15,20})>', text) if guild.get_role(int(x))]


def extract_channel_mentions(guild: discord.Guild, text: str) -> list[discord.abc.GuildChannel]:
    return [guild.get_channel(int(x)) for x in re.findall(r'<@&([0-9]{15,20})>', text) if guild.get_channel(int(x))]


def get_related_tc(voice_channel) -> discord.TextChannel:
    return discord.utils.get(
        voice_channel.category.text_channels,
        topic=str(voice_channel.id),
    )


def get_related_vc(text_channel: discord.TextChannel) -> discord.VoiceChannel:
    if text_channel.topic is None or not text_channel.topic.isdecimal():
        return None
    return discord.utils.get(
        text_channel.category.voice_channels,
        id=int(text_channel.topic),
    )


async def react_numbers(message: discord.Message):
    for emoji in EMOJI_NUMBERS:
        await message.add_reaction(emoji)


async def warn(channel: discord.TextChannel, author: discord.User | discord.Member, message: discord.Message, delete_after=10) -> discord.Message:
    return await channel.send(f'{author.mention} {message}', delete_after=delete_after)


async def dialog(bot: commands.Bot, message: discord.Message, target: discord.User | discord.Member) -> bool:
    await message.add_reaction('⭕')
    await message.add_reaction('❌')

    def check(reaction, user):
        if reaction.message.id != message.id:
            return False
        if user.id != target.id:
            return False
        if str(reaction.emoji) not in ('⭕', '❌'):
            return False
        return True

    try:
        reaction, _ = await bot.wait_for(
            'reaction_add',
            check=check,
            timeout=10,
        )
    except asyncio.TimeoutError:
        await message.delete()
        return False

    await message.delete()
    return str(reaction.emoji) == '⭕'


def count_all_vc_member(guild: discord.Guild):
    return sum(len([m for m in vc.members if not m.bot]) for vc in guild.voice_channels)


def get_member(guild: discord.Guild, keyword: str) -> discord.Member | None:
    for member in guild.members:
        if member.bot:
            continue
        if keyword == str(member.id):
            return member
        if keyword in f'{member.name}#{member.discriminator}':
            return member
    return None


def find_member(guild: discord.Guild, keyword: str) -> discord.Member | set[discord.Member] | None:
    """
    Guild 内の Member のリストから、keyword に完全一致または部分一致する Member を取得します。
    IDまたはアカウント名が完全一致した場合は discord.Member を返却します。
    アカウント名または表示名に部分一致した場合は Set[discord.Member] を返却します。
    完全一致も部分一致もしなかった場合は None を返却します。
    """
    results = set()
    for member in guild.members:
        if member.bot:
            continue
        if keyword == str(member.id):
            return member
        if keyword == f'{member.name}#{member.discriminator}':
            return member
        if keyword in f'{member.name}#{member.discriminator}':
            results.add(member)
        if keyword in member.display_name:
            results.add(member)
    return results or None


def find_members(guild: discord.Guild, keywords: str) -> list[set[discord.Member]]:
    perfect_match_members = set()
    partial_match_members = set()
    for keyword in keywords.split():
        match find_member(guild, keyword):
            case discord.Member() as member:
                perfect_match_members.add(member)
            case set() as members:
                partial_match_members |= members
            case None:
                pass
    return [perfect_match_members, partial_match_members]


async def fetch_image(message: discord.Message) -> bytes:
    image_url = message.attachments[0].url
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            return await response.read()


def compose_embed_from_description(description: str) -> discord.Embed:
    return discord.Embed.from_dict({
        'description': description,
        'color': COLOUR_EMBED_GRAY,
    })


def compose_embed_from_message(message: discord.Message) -> discord.Embed:
    embed = discord.Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar.url,
    )
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon.url,
    )
    if message.attachments and message.attachments[0].url:
        embed.set_image(
            url=message.attachments[0].url
        )
    return embed
