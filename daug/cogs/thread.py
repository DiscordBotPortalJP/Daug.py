import discord
from discord.ext import commands
from Daug.utils import excepter
from Daug.utils.embeds import compose_embed_from_description
from Daug.utils.embeds import compose_embed_from_message

async def change_category(channel, category) -> None:
    """チャンネルのカテゴリを変更"""
    await channel.edit(category=category)

async def transfer(channel_origin, guild) -> None:
    """テキストチャンネルを指定のguildに転送"""
    channel = await guild.create_text_channel(
        name=channel_origin.name,
        topic=str(channel_origin.created_at)
    )
    async for message in channel_origin.history(limit=None, oldest_first=True):
        if message.content:
            await channel.send(embed=compose_embed_from_message(message))
        for embed in message.embeds:
            await channel.send(embed=embed)

class Thread(commands.Cog):
    def __init__(self, bot, guild_id, guild_archive_id, category_issues_id, category_open_id, category_closed_id, category_archive_id):
        self.bot = bot
        self.guild_id = guild_id
        self.guild_archive_id = guild_archive_id
        self.category_issues_id = category_issues_id
        self.category_open_id = category_open_id
        self.category_closed_id = category_closed_id
        self.category_archive_id = category_archive_id
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
        await channel_issue.send(embed=compose_embed_from_description(self.message_on_thread))
        await channel_issue.send(embed=compose_embed_from_message(message))
        await message.channel.send(
            embed=compose_embed_from_description(
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
        if channel.category is None:
            return False
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
            embed=compose_embed_from_description(f'チャンネル名を以下に変更しました\n{rename} ')
        )

    async def dispatch_archive(self, channel, member):
        category_archive = channel.guild.get_channel(self.category_archive_id)
        if channel.category.id == category_archive.id:
            if not member.guild_permissions.manage_channels:
                return
            await transfer(
                channel_origin=channel,
                guild=self.bot.get_guild(self.guild_archive_id)
            )
            await channel.delete()
        else:
            await change_category(channel, category_archive)
            return

    @commands.command()
    @excepter
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
    @excepter
    async def archive(self, ctx):
        channel = ctx.channel
        author = ctx.author
        await self.dispatch_archive(channel, author)

    @commands.Cog.listener()
    @excepter
    async def on_message(self, message):
        channel = message.channel
        if not isinstance(channel, discord.channel.TextChannel):
            return
        if message.guild.id != self.guild_id:
            return
        if message.author.bot:
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
    @excepter
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if not isinstance(channel, discord.channel.TextChannel):
            return
        author = channel.guild.get_member(payload.user_id)
        if payload.guild_id != self.guild_id:
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
