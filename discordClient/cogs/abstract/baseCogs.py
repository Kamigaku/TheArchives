from discord.ext import commands


class BaseCogs(commands.Cog):

    def __init__(self, bot, name):
        self.bot = bot
        self.cogs_name = name

    async def retrieve_member(self, discord_user_id: int):
        return await self.bot.fetch_user(discord_user_id)