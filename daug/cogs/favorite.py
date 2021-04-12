from discord.ext import commands
from Daug.functions import excepter
from Daug.functions.embeds import compose_embed_from_message


class Favorite(commands.Cog):
    """お気に入り機能"""
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.channel_tips_id = self.bot.config['Daug']['channel_tips_id']

    async def dispatch_tips(self, message):
        channel = self.bot.get_channel(self.channel_tips_id)
        await channel.send(embed=compose_embed_from_message(message))

    @commands.Cog.listener()
    @excepter
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if not isinstance(channel, discord.channel.TextChannel):
            return
        author = channel.guild.get_member(payload.user_id)
        if payload.guild_id != self.id:
            return
        if author.bot:
            return
        if payload.emoji.name == '⭐':
            message = await channel.fetch_message(payload.message_id)
            await self.dispatch_tips(message)
