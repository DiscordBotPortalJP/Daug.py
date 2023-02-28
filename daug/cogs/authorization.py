import asyncio
from discord.ext import commands
from Daug.utils import excepter

class Utils(commands.Cog):
    def __init__(self, bot, guild_id, role_always_id, role_permission_id, expiration_minutes = 300):
        self.bot = bot
        self.guild_id = guild_id
        self.role_id = role_always_id
        self.role_permission_id = role_permission_id
        self.expiration_minutes = expiration_minutes

    @commands.command(aliases=['auth', 'su'])
    @excepter
    async def authorization(self, ctx):
        if ctx.guild.id != self.guild_id:
            return
        if ctx.author.get_role(self.role_always_id) is None:
            await ctx.reply('権限を付与できません')
            return
        role_permission = ctx.guild(self.role_permission_id)
        if ctx.author.get_role(self.role_permission_id):
            await ctx.author.remove_roles(role_permission)
            await ctx.reply(f'{role_permission.name} を削除しました。')
            return
        await ctx.author.add_roles(role_permission)
        if self.expiration_minutes > 0:
            await ctx.reply(f'{role_permission.name} を付与しました。{self.expiration_minutes}秒後に解除されます。')
            await asyncio.sleep(self.expiration_minutes)
            await ctx.author.remove_roles(role_permission)
        else:
            await ctx.reply(f'{role_permission.name} を付与しました。')
