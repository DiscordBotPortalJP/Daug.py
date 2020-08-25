from discord.ext import commands


class Join(commands.Cog):
    """入室時の処理"""
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.role_member_id = self.bot.config['Daug']['role_member_id']

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != self.id:
            return
        if member.bot:
            return
        role_member = member.guild.get_role(self.role_member_id)
        await member.add_roles(role_member)
