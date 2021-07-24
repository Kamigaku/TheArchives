from discord.ext import commands
from discord.ext.commands import Context
import calendar
from datetime import date
import os
import jsonpickle
from discordClient.model import event
from discordClient.config import settings
from discordClient.cogs import assignableCogs


class EventCogs(assignableCogs.AssignableCogs):

    def __init__(self, bot):
        super().__init__(bot, "events")
        self.bookedDates = []
        if os.path.exists("calendar.json"):
            calendarFile = open("calendar.json", "r")
            self.bookedDates = jsonpickle.decode(calendarFile.read())

    # Commands => commands.command va appeler des commandes customs
    @commands.command(name="edisplay")
    async def display(self, ctx: Context):
        if str(ctx.channel.id) == self.channel_id:
            await self.displayCalendar(ctx)

    @commands.command(name="eadd")
    async def add(self, ctx: Context, author: str, date_event: str, description: str):
        if str(ctx.channel.id) == self.channel_id:
            createdEvent = event.Event(author, date_event, description)
            self.bookedDates.append(createdEvent)
            self.saveCalendar()
            await ctx.message.delete()
            await ctx.send(content="The event has been successfully registered! 😃", delete_after=60)

    @commands.command(name="edelete")
    async def delete(self, ctx: Context, id_event: str):
        if str(ctx.channel.id) == self.channel_id:
            for currentEvent in self.bookedDates:
                if str(currentEvent.uuid) == id_event:
                    self.bookedDates.remove(currentEvent)
            self.saveCalendar()
            await ctx.message.delete()
            await ctx.send(content="The event has been successfully removed! 😃", delete_after=60)

    @commands.command("eassign")
    async def assign(self, ctx, channel_id: str):
        self.assign_channel(ctx, channel_id)

    # Public methods that helps
    def getWeeksAndDaysInMonth(self, year: int, month: int):
        cal = calendar.Calendar()
        weeks = {}
        for week in cal.monthdatescalendar(year, month):
            weekNumber = week[0].isocalendar()[1]
            weeks[weekNumber] = []
            for day in week:
                weeks[weekNumber].append(day)
        return weeks

    def saveCalendar(self):
        f = open("calendar.json", "w")
        f.write(jsonpickle.encode(self.bookedDates))
        f.close()

    async def displayCalendar(self, ctx: Context):
        weeks = self.getWeeksAndDaysInMonth(date.today().year, date.today().month)
        for week in weeks:
            for day in weeks[week]:
                isoWeek = day.isoweekday()
                if isoWeek < 6:
                    for currentEvent in self.bookedDates:
                        if currentEvent.toDateTime().date() == day:
                            await ctx.send(embed=currentEvent.formatEvent())


def setup(client):
    client.add_cog(EventCogs(client))
