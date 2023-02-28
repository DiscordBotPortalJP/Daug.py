from discord.ext import commands
from Daug.utils import excepter

class Join(commands.Cog):
    """メンバー入室時"""
    def __init__(self, bot, guild_id, channel_id = None, role_member_id = None, role_bot_id = None):
        self.bot = bot
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.role_member_id = role_member_id
        self.role_bot_id = role_bot_id

    @commands.Cog.listener()
    @excepter
    async def on_member_join(self, member):
        if member.guild.id != self.guild_id:
            return
        if self.channel_id is not None:
            self.bot.get_channel(self.channel_id).send(f'{member.mention} が入室しました')
        if not member.bot and self.role_member_id is not None:
            role_member = member.guild.get_role(self.role_member_id)
            await member.add_roles(role_member)
        if member.bot and self.role_bot_id is not None:
            role_bot = member.guild.get_role(self.role_bot_id)
            await member.add_roles(role_bot)
