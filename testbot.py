from discord.ext import commands
import logging
import os

config = {
    'discordbotjp': {
        'guild_id': 494911447420108820,
        'guild_logs_id': 674500858054180874,
        'role_member_id': 579591779364372511,
        'role_contributor_id': 631299456037289984,
        'channel_tips_id': 693388545628438538,
        'category_issues_id': 601219955035209729,
        'category_open_id': 575935336765456394,
        'category_closed_id': 640090897417240576,
        'category_archive_id': 689447835590066212,
    },
}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = commands.Bot(command_prefix='/', help_command=None)
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.load_extension('discordbotjp.cog')
    bot.run(token)
