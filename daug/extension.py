from Daug.cogs.channels import Channels
from Daug.cogs.favorite import Favorite
from Daug.cogs.join import Join
from Daug.cogs.leave import Leave
from Daug.cogs.thread import Thread
from Daug.cogs.utils import Utils


def setup(bot):
    bot.add_cog(Channels(bot))
    bot.add_cog(Thread(bot))
    bot.add_cog(Join(bot))
    bot.add_cog(Leave(bot))
    bot.add_cog(Favorite(bot))
    bot.add_cog(Utils(bot))
