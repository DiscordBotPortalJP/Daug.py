import asyncio

from discord.ext import commands
from Daug.functions import excepter
from Daug.functions.embeds import compose_embed_from_description


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.committer_role_id = self.bot.config['Daug']['role_committer_id']
        self.staff_role_id = self.bot.config['Daug']['role_staff_id']
        self.committer_perm_role_id = self.bot.config['Daug']['role_committer_perm_id']
        self.staff_perm_role_id = self.bot.config['Daug']['role_staff_perm_id']

    def is_committer(self, author) -> bool:
        if self.committer_role_id not in [role.id for role in author.roles]:
            return False
        return True

    def is_staff(self, author) -> bool:
        if self.staff_role_id not in [role.id for role in author.roles]:
            return False
        return True

    @commands.command(aliases=['ch'])
    @excepter
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.channel.send(embed=compose_embed_from_description(f'チャンネル数:{count}'))

    @commands.command(aliases=['sp'])
    @excepter
    async def switch_perm(self, ctx):
        if ctx.guild.id != self.id:
            return

        guild = ctx.guild
        committer_perm_role = guild.get_role(self.committer_perm_role_id)
        staff_perm_role = guild.get_role(self.staff_perm_role_id)

        if self.is_staff(ctx.author):
            await ctx.author.add_roles(staff_perm_role)
            await asyncio.sleep(300)
            await ctx.author.remove_roles(staff_perm_role)

        elif self.is_committer(ctx.author):
            await ctx.author.add_roles(committer_perm_role)
            await asyncio.sleep(300)
            await ctx.author.remove_roles(committer_perm_role)

        else:
            return
