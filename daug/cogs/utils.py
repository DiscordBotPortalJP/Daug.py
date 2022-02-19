import asyncio

from discord.ext import commands
from Daug.functions import excepter
from Daug.functions.embeds import compose_embed_from_description

expiration_minutes = 300

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.committer_role_id = self.bot.config['Daug']['role_committer_id']
        self.staff_role_id = self.bot.config['Daug']['role_staff_id']
        self.committer_perm_role_id = self.bot.config['Daug']['role_committer_perm_id']
        self.staff_perm_role_id = self.bot.config['Daug']['role_staff_perm_id']

    def is_committer(self, author) -> bool:
        return self.committer_role_id in [role.id for role in author.roles]

    def is_staff(self, author) -> bool:
        return self.staff_role_id in [role.id for role in author.roles]

    @commands.command(aliases=['ch'])
    @excepter
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.channel.send(embed=compose_embed_from_description(f'チャンネル数:{count}'))

    @commands.command(aliases=['auth', 'su'])
    @excepter
    async def authorization(self, ctx):
        if ctx.guild.id != self.id:
            return

        guild = ctx.guild
        perm_role = None
        if self.is_staff(ctx.author):
            perm_role = guild.get_role(self.staff_perm_role_id)
        elif self.is_committer(ctx.author):
            perm_role = guild.get_role(self.committer_perm_role_id)
        if perm_role is None:
            return await ctx.reply('付与できる権限がありません')

        await ctx.author.add_roles(perm_role)
        await ctx.reply(f'{perm_role.name} を付与しました。{expiration_minutes}秒後に解除されます。')
        await asyncio.sleep(expiration_minutes)
        await ctx.author.remove_roles(perm_role)
