from discord.ext import commands
from discord import Intents
from discordClient.cogs.settingsCogs import SettingsCogs
#from discordClient.cogs.movieCogs import MovieCogs
#from discordClient.cogs.animeCogs import AnimeCogs
from discordClient.cogs.eventCogs import EventCogs
from discordClient.cogs.economyCogs import EconomyCogs
from discordClient.cogs.cardCogs import CardCogs


class Puppet:

    def __init__(self, token):
        self.token = token
        intents = Intents.default()
        intents.members = True
        intents.presences = True
        intents.reactions = True
        self.bot = commands.Bot(command_prefix='puppet ', intents=intents)
        self.bot.add_cog(SettingsCogs(self.bot))
        #self.bot.add_cog(MovieCogs(self.bot))
        #self.bot.add_cog(AnimeCogs(self.bot))
        self.bot.add_cog(EventCogs(self.bot))
        self.bot.add_cog(EconomyCogs(self.bot))
        self.bot.add_cog(CardCogs(self.bot))

    def connectToServer(self):
        self.bot.run(self.token)

