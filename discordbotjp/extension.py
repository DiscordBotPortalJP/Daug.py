from discordbotjp.cogs.cog import DiscordBotPortalJP
from discordbotjp.cogs.join import Join
from discordbotjp.cogs.leave import Leave


def setup(bot):
    bot.add_cog(DiscordBotPortalJP(bot))
    bot.add_cog(Join(bot))
    bot.add_cog(Leave(bot))
