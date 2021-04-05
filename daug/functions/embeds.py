from discord import Colour
from discord import Embed


def compose_embed_from_description(description):
    return Embed.from_dict({
        'description': description,
        'color': Colour.blue().value,
    })


def compose_embed_from_message(message):
    embed = Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url,
    )
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed
