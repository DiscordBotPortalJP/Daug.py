import discord
from discord.ext import commands
import logging
import os

config = {
    'Daug': {
        'guild_id': 709729198075412601,
        'guild_logs_id': 674500858054180874,
        'role_bot_limited_id': 710758653321281597,
        'role_member_id': 709729198075412607,
        'role_contributor_id': 709729198075412609,
        'role_committer_id': 704548043537645621,
        'role_staff_id': 741325667550887946,
        'role_committer_perm_id': 858642308642897921,
        'role_staff_perm_id': 834963970615934996,
        'channel_tips_id': 709729198809415716,
        'category_issues_id': 709729199228846140,
        'category_open_id': 709729199509733383,
        'category_closed_id': 709729199954329679,
        'category_archive_id': 709729216245006457,
    },
}

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    bot = commands.Bot(
        command_prefix='/',
        help_command=None,
        intents=discord.Intents.all(),
    )
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.config = config
    bot.load_extension('Daug.extensions.channels')
    bot.load_extension('Daug.extensions.favorite')
    bot.load_extension('Daug.extensions.join')
    bot.load_extension('Daug.extensions.leave')
    bot.load_extension('Daug.extensions.thread')
    bot.load_extension('Daug.extensions.utils')
    bot.run(token)
