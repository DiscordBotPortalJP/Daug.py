import io
import discord
from time import time
from discord.ext import commands
from Daug.utils import excepter

def compose_channel_tree(guild):
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

class Channels(commands.Cog):
    """チャンネル情報取得"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ch'])
    @commands.guild_only()
    @excepter
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.channel.send(embed=discord.Embed(description=f'チャンネル数:{count}'))

    @commands.group()
    @commands.guild_only()
    @excepter
    async def channels(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('{} = Text:{} + Voice:{} + Category:{}'.format(
                len(ctx.guild.channels),
                len(ctx.guild.text_channels),
                len(ctx.guild.voice_channels),
                len(ctx.guild.categories),
            ))

    @channels.command()
    @commands.guild_only()
    @excepter
    async def tree(self, ctx):
        await ctx.send(
            file=discord.File(
                io.StringIO(compose_channel_tree(ctx.guild)),
                f'channels{int(time())}.txt',
            )
        )
