from daug.cogs.thread import Thread
from daug.cogs.join import Join
from daug.cogs.leave import Leave
from daug.cogs.favorite import Favorite


def setup(bot):
    bot.add_cog(Thread(bot))
    bot.add_cog(Join(bot))
    bot.add_cog(Leave(bot))
    bot.add_cog(Favorite(bot))
