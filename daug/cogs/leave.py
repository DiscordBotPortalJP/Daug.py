from discord.ext import commands


class Leave(commands.Cog):
    """退出時の処理"""
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id != self.id:
            return
        await guild.system_channel.send(f'{member.mention} が退出しました')
