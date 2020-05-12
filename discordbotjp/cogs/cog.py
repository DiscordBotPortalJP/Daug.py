import discord
from discord.ext import commands
from dispander import compose_embed
from echidna.daug import get_default_embed


class DiscordBotPortalJP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['discordbotjp']['guild_id']
        self.guild_logs_id = self.bot.config['discordbotjp']['guild_logs_id']
        self.role_member_id = self.bot.config['discordbotjp']['role_member_id']
        self.role_contributor_id = self.bot.config['discordbotjp']['role_contributor_id']
        self.channel_tips_id = self.bot.config['discordbotjp']['channel_tips_id']
        self.category_issues_id = self.bot.config['discordbotjp']['category_issues_id']
        self.category_open_id = self.bot.config['discordbotjp']['category_open_id']
        self.category_closed_id = self.bot.config['discordbotjp']['category_closed_id']
        self.category_archive_id = self.bot.config['discordbotjp']['category_archive_id']
        self.close_keywords = [
            'close', 'closes', 'closed',
            'fix', 'fixes', 'fixed',
            'resolve', 'resolves', 'resolved',
        ]
        self.message_on_thread = \
            'この質問スレッドは close と発言することで解決済みカテゴリに移動します。'

    async def dispatch_thread(self, message):
        category_open = message.guild.get_channel(self.category_open_id)
        if channels := [ch for ch in category_open.text_channels if str(message.author.id) in ch.topic]:
            text = f'{message.author.mention} {channels[0].mention} こちらの質問が未解決です。'
            await message.channel.send(text)
            return
        if len(name := message.content) > 30:
            name = message.channel.name
        channel_issue = await message.guild.create_text_channel(
            name=name,
            topic=message.author.id,
            category=category_open,
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
        if '🚫' in channel.category.name:
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
        messages = await channel.history().flatten()
        guild = self.bot.get_guild(self.guild_logs_id)
        channel = await guild.create_text_channel(
            name=channel.name,
            topic=str(channel.created_at)
        )
        for message in reversed(messages):
            if message.content:
                await channel.send(embed=compose_embed(message))
            for embed in message.embeds:
                await channel.send(embed=embed)

    async def dispatch_tips(self, message):
        channel = self.bot.get_channel(self.channel_tips_id)
        await channel.send(embed=compose_embed(message))

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
        await self.dispatch_archive(channel, author)

    @commands.command(aliases=['ch'])
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.channel.send(embed=get_default_embed(f'チャンネル数:{count}'))

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
        if payload.emoji.name == '⭐':
            message = await channel.fetch_message(payload.message_id)
            await self.dispatch_tips(message)
