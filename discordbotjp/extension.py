from discordbotjp.cogs.cog import DiscordBotPortalJP
from discordbotjp.cogs.join import Join


def setup(bot):
    bot.add_cog(DiscordBotPortalJP(bot))
    bot.add_cog(Join(bot))
