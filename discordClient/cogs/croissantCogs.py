from discord.ext import commands
from discord.ext.commands import Context
from prettytable import PrettyTable
import calendar
from datetime import datetime
from datetime import date


class CroissantCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.table = PrettyTable()
        self.table.field_names = ["Semaine", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        self.croissant = '\N{croissant}'
        self.bookedDates = {}

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="cdisplay")
    async def display(self, ctx: Context):
        self.table.clear_rows()
        tableTitle = f'P\'tit dej'
        weeks = self.getWeeksAndDaysInMonth(date.today().year,
                                     date.today().month)
        for week in weeks:
            row = [f'Semaine {week}', "", "", "", "", ""]
            for day in weeks[week]:
                isoWeek = day.isoweekday()
                if isoWeek < 6 and day in self.bookedDates:
                    row[isoWeek] = self.bookedDates[day][0]
            self.table.add_row(row)

        await ctx.send(f'```\r\n{self.table.get_string(title=tableTitle)}```')

    @commands.command(name="cadd")
    async def add(self, ctx: Context, user: str, date: str):
        datetime_object = datetime.strptime(date, "%d/%m/%Y").date()
        if datetime_object not in self.bookedDates:
            self.bookedDates[datetime_object] = []
        self.bookedDates[datetime_object].append(user)

    def getWeeksAndDaysInMonth(self, year: int, month: int):
        cal = calendar.Calendar()
        weeks = {}
        for week in cal.monthdatescalendar(year, month):
            weekNumber = week[0].isocalendar()[1]
            weeks[weekNumber] = []
            for day in week:
                weeks[weekNumber].append(day)
        return weeks


def setup(client):
    client.add_cog(CroissantCogs(client))
