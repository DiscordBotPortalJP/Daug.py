from discord import Colour
from discord import Embed


def compose_embed_default(description):
    return Embed.from_dict({
        'description': description,
        'color': Colour.blue().value,
    })
