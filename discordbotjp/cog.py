import discord
from discord.ext import commands
from dispander import compose_embed
from echidna.daug import get_default_embed
from echidna import base36


class DiscordBotPortalJP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = 494911447420108820
        self.guild_logs_id = 674500858054180874
        self.role_member_id = 579591779364372511
        self.role_contributor_id = 631299456037289984
        self.category_issues_id = 601219955035209729
        self.category_open_id = 575935336765456394
        self.category_closed_id = 640090897417240576
        self.category_archive_id = 689447835590066212
        self.close_keywords = [
            'close', 'closes', 'closed',
            'fix', 'fixes', 'fixed',
            'resolve', 'resolves', 'resolved',
        ]
        self.message_on_thread = \
            'この質問スレッドは close と発言することで解決済みカテゴリに移動します。'

    async def dispatch_thread(self, message):
        if len(name := message.content) > 30:
            name = message.channel.name
        channel_issue = await message.guild.create_text_channel(
            name=name,
            category=message.guild.get_channel(self.category_open_id),
        )
        await channel_issue.edit(position=0)
        await channel_issue.send(embed=get_default_embed(self.message_on_thread))
        await channel_issue.send(embed=compose_embed(message))
        await message.channel.send(
            embed=get_default_embed(
                f'スレッド {channel_issue.mention} を作成しました {message.author.mention}')
        )
        if len(message.content) <= 30:
            await message.delete()
            return
        await channel_issue.send(
            '質問のタイトルを入力してください。チャンネル名に反映します。'
        )
        title = await self.bot.wait_for(
            'message',
            check=lambda m: m.channel == channel_issue
        )
        await self.dispatch_rename(title, title.content)

    async def dispatch_reopen(self, channel):
        await channel.edit(
            category=channel.guild.get_channel(self.category_open_id)
        )

    async def dispatch_close(self, channel):
        await channel.edit(
            category=channel.guild.get_channel(self.category_closed_id)
        )

    def is_category_open(self, channel):
        return channel.category_id == self.category_open_id

    def is_category_closed(self, channel):
        if '✅' in channel.category.name:
            return True
        if '⛔' in channel.category.name:
            return True
        return False

    def is_category_thread(self, channel):
        if self.is_category_open(channel):
            return True
        if self.is_category_closed(channel):
            return True
        return False

    async def dispatch_age(self, message):
        await message.channel.edit(
            position=0
        )

    async def dispatch_rename(self, message, rename):
        await message.channel.edit(name=rename)
        await message.channel.send(
            embed=get_default_embed(f'チャンネル名を以下に変更しました\n{rename} ')
        )

    async def dispatch_archive(self, channel, member):
        if self.role_contributor_id in [role.id for role in member.roles]:
            await channel.edit(
                category=channel.guild.get_channel(self.category_archive_id)
            )
            return
        if not member.guild_permissions.administrator:
            return
        guild = self.bot.get_guild(self.guild_logs_id)
        channel = await guild.create_text_channel(
            name=channel.name,
            topic=str(channel.created_at)
        )
        messages = await channel.history().flatten()
        for message in reversed(messages):
            if message.content:
                await channel.send(embed=compose_embed(message))
            for embed in message.embeds:
                await channel.send(embed=embed)

    @commands.command()
    async def name(self, ctx, *, rename):
        message = ctx.message
        channel = ctx.message.channel
        conditions = (
            self.is_category_open(channel),
            self.is_category_closed(channel),
        )
        if not any(conditions):
            return
        await self.dispatch_rename(message, rename)

    @commands.command()
    async def archive(self, ctx):
        channel = ctx.channel
        author = ctx.author
        await dispatch_archive(channel, author)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        if message.guild.id != self.id:
            return
        if message.author.bot:
            return
        if not isinstance(channel, discord.channel.TextChannel):
            return
        ctx = await self.bot.get_context(message)
        if ctx.command:
            return
        if self.is_category_open(channel):
            if message.content in self.close_keywords:
                await self.dispatch_close(message.channel)
                return
            await self.dispatch_age(message)
        if channel.category_id == self.category_issues_id:
            await self.dispatch_thread(message)
            return
        if self.is_category_closed(channel):
            await self.dispatch_reopen(channel)
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != self.id:
            return
        if member.bot:
            return
        role_member = member.guild.get_role(self.role_member_id)
        await member.add_roles(role_member)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        if payload.guild_id != self.id:
            return
        if author.bot:
            return
        if payload.emoji.name == '✅':
            if not self.is_category_open(channel):
                return
            await self.dispatch_close(channel)
        if payload.emoji.name == '🚫':
            if not self.is_category_thread(channel):
                return
            await self.dispatch_archive(channel, author)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id != self.id:
            return
        await guild.system_channel.send(f'{member.mention} が退出しました')


def setup(bot):
    bot.add_cog(DiscordBotPortalJP(bot))
