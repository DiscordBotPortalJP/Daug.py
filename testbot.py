from discord.ext import commands
import logging
import os

config = {
    'daug': {
        'guild_id': 709729198075412601,
        'guild_logs_id': 674500858054180874,
        'role_member_id': 709729198075412607,
        'role_contributor_id': 709729198075412609,
        'channel_tips_id': 709729198809415716,
        'category_issues_id': 709729199228846140,
        'category_open_id': 709729199509733383,
        'category_closed_id': 709729199954329679,
        'category_archive_id': 709729216245006457,
    },
}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = commands.Bot(command_prefix='/', help_command=None)
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.config = config
    bot.load_extension('daug.extension')
    bot.run(token)
