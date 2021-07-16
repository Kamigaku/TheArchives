from datetime import datetime
import discord
import uuid


class Event(object):

    def __init__(self, author: str, date: str, description: str):
        self.author = author
        self.date = date
        self.description = description
        self.uuid = uuid.uuid4()

    def toDateTime(self):
        return datetime.strptime(self.date, "%d/%m/%Y")

    def formatEvent(self):
        embed = discord.Embed(description=self.description, timestamp=self.toDateTime())
        embed.set_author(name="🗓️ %s" % self.author)
        embed.set_footer(text="Event id: %s" % self.uuid)
        return embed
