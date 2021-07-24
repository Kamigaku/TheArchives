import discord
from discord.ext import commands
import uuid

class Rating():

    def __init__(self, author: str, element_id: str, rating: float, comment: str):
        self.author = author
        self.element_id = element_id
        self.rating = rating
        self.comment = comment
        self.uuid = uuid.uuid4()

    def formatRating(self):
        pass

    async def retrieve_member(self, bot: commands.Bot):
        return await bot.fetch_user(int(self.author))

