from discord.ext import commands
from Daug.utils import excepter

class Leave(commands.Cog):
    """メンバー退出時"""
    def __init__(self, bot, guild_id, channel_id = None):
        self.bot = bot
        self.guild_id = guild_id
        self.channel_id = channel_id

    @commands.Cog.listener()
    @excepter
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id != self.guild_id:
            return
        text = f'{member.mention} が退出しました'
        if self.channel_id is None:
            await guild.system_channel.send(text)
        else:
            await self.bot.get_channel(self.channel_id).send(text)
