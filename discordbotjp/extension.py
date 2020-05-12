from discordbotjp.cogs.thread import Thread
from discordbotjp.cogs.join import Join
from discordbotjp.cogs.leave import Leave
from discordbotjp.cogs.favorite import Favorite


def setup(bot):
    bot.add_cog(Thread(bot))
    bot.add_cog(Join(bot))
    bot.add_cog(Leave(bot))
    bot.add_cog(Favorite(bot))
