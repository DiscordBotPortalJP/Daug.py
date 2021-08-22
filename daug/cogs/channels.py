from time import time
from discord.ext import commands
from Daug.functions import excepter
from Daug.functions import send_file_from_text
from Daug.functions import compose_channel_tree


class Channels(commands.Cog):
    """チャンネル関連"""
    def __init__(self, bot):
        self.bot = bot

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
        await send_file_from_text(
            channel=ctx.channel,
            text=compose_channel_tree(ctx.guild),
            filename=f'channels{int(time())}.txt'
        )
