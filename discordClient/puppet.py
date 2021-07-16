from discord.ext import commands
from discordClient.cogs.settingsCogs import SettingsCogs
from discordClient.cogs.movieCogs import MovieCogs
from discordClient.cogs.animeCogs import AnimeCogs
from discordClient.cogs.eventCogs import EventCogs


class Puppet:

    def __init__(self, token):
        self.token = token
        self.bot = commands.Bot(command_prefix='/')
        self.bot.add_cog(SettingsCogs(self.bot))
        self.bot.add_cog(MovieCogs(self.bot))
        self.bot.add_cog(AnimeCogs(self.bot))
        self.bot.add_cog(EventCogs(self.bot))

    def connectToServer(self):
        self.bot.run(self.token)

