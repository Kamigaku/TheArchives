from discord.ext import commands
from discord import Intents

from discordClient.cogs.cardCogs import CardCogs
from discordClient.cogs.economyCogs import EconomyCogs
from discordClient.cogs.eventCogs import EventCogs
from discordClient.cogs.settingsCogs import SettingsCogs
from discordClient.cogs.museumCogs import MuseumCogs


class PuppetBot(commands.Bot):

    def __init__(self, commands_prefix: str):
        intents = Intents.default()
        intents.members = True
        intents.presences = True
        intents.reactions = True
        super().__init__(command_prefix=commands_prefix, intents=intents)

    def default_initialisation(self):
        self.add_cog(SettingsCogs(self))
        #self.bot.add_cog(MovieCogs(self.bot))
        #self.bot.add_cog(AnimeCogs(self.bot))
        self.add_cog(EventCogs(self))
        self.add_cog(EconomyCogs(self))
        self.add_cog(CardCogs(self))
        self.add_cog(MuseumCogs(self))
