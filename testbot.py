import os
import discord
from discord.ext import commands

extensions = (
)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.all(),
        )

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(f'extensions.{extension}')

if __name__ == '__main__':
    MyBot().run(os.getenv('DISCORD_BOT_TOKEN'))
