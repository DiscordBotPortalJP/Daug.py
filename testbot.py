from discord.ext import commands
import logging
import os

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = commands.Bot(command_prefix='/', help_command=None)
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.load_extension('discordbotjp.cog')
    bot.run(token)
