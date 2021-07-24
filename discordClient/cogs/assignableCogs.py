from discord.ext import commands
from discordClient.config import settings


class AssignableCogs(commands.Cog):

    def __init__(self, bot, name):
        self.bot = bot
        self.cogs_name = name
        if name in settings.configurationFile["COGS_CONFIGURATION"]:
            self.channel_id = settings.configurationFile["COGS_CONFIGURATION"][name]
        else:
            self.channel_id = ""

    async def assign_channel(self, ctx, channel_id: str):
        self.channel_id = channel_id
        settings.registerCogChannel(self.cogs_name, channel_id)
        await ctx.message.delete()
