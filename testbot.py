from discord import Intents
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or
from os import getenv
import logging


def run(config, extensions):
    logging.basicConfig(level=logging.WARNING)
    bot = Bot(
        command_prefix=when_mentioned_or('$'),
        help_command=None,
        intents=Intents.all(),
    )
    bot.config = config
    for extension in extensions:
        bot.load_extension(f'Daug.extensions.{extension}')
    bot.run(getenv('DISCORD_BOT_TOKEN'))


if __name__ == '__main__':
    config = {
        'Daug': {
            'guild_id': 709729198075412601,
            'guild_logs_id': 674500858054180874,
            'role_bot_limited_id': 710758653321281597,
            'role_member_id': 709729198075412607,
            'role_contributor_id': 709729198075412609,
            'channel_tips_id': 709729198809415716,
            'category_issues_id': 709729199228846140,
            'category_open_id': 709729199509733383,
            'category_closed_id': 709729199954329679,
            'category_archive_id': 709729216245006457,
        },
    }
    extensions = ('channels', 'favorite', 'join', 'leave', 'thread', 'utils')
    run(config, extensions)
