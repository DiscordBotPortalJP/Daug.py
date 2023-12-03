import datetime
from functools import wraps
import traceback
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
CHANNEL_TRACEBACK_ID = getenv('CHANNEL_TRACEBACK_ID')


def excepter(func, *, _channel_id=None):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            orig_error = getattr(e, 'original', e)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())

            channel_id = _channel_id or CHANNEL_TRACEBACK_ID
            if len(args) >= 1 and isinstance(args[0], discord.Interaction):
                interaction: discord.Interaction = args[0]
                channel = interaction.client.get_channel(channel_id)
            else:
                bot: commands.Bot = self.bot
                channel = bot.get_channel(channel_id)

            if channel:
                embed = discord.Embed()
                embed.add_field(name='class', value=self.__class__.__name__)
                embed.add_field(name='function', value=func.__name__)
                embed.add_field(name='datetime', value=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))
                await channel.send(f'```python\n{error_msg}\n```', embed=embed)
    return wrapped
