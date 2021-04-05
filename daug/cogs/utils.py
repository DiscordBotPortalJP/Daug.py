from discord.ext import commands
from Daug.functions.embeds import compose_embed_from_description


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']

    @commands.command(aliases=['ch'])
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.channel.send(embed=compose_embed_from_description(f'チャンネル数:{count}'))
