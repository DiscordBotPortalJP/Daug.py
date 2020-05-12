from discord.ext import commands
from echidna.daug import get_default_embed


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['discordbotjp']['guild_id']

    @commands.command(aliases=['ch'])
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.channel.send(embed=get_default_embed(f'チャンネル数:{count}'))
