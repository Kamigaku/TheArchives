from discord.ext import commands


class SettingsCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.name = "SettingsCogs"

    # Events => le format commands.Cog.listener va appelé des méthodes classiques
    @commands.Cog.listener()
    async def on_ready(self):
        print("The bot is online.")

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="unload")
    async def unloadExtension(self, ctx, extension: str):
        self.bot.unload_extension(f'discordClient.cogs.{extension}')
        print(f'The extension \"{extension}\" has been unloaded.')

    @commands.command(name="load")
    async def loadExtension(self, ctx, extension: str):
        print(extension)
        self.bot.load_extension(f'discordClient.cogs.{extension}')
        print(f'The extension \"{extension}\" has been loaded.')

    async def clearLogs(self, ctx):
        self.bot.send("Not implemented yet.")
