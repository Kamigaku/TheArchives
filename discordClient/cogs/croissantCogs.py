from discord.ext import commands
from discord.ext.commands import Context
from prettytable import PrettyTable
import calendar
import datetime


class CroissantCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.table = PrettyTable()
        self.table.field_names = ["Semaine", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        self.croissant = '\N{croissant}'

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="cdisplay")
    async def display(self, ctx: Context):
        self.table.clear_rows()
        tableTitle = f'{self.croissant} P\'tit dej {self.croissant}'
        weeks = self.getWeeksInMonth(datetime.date.today().year,
                                     datetime.date.today().month)
        for week in weeks:
            self.table.add_row([f'Semaine {week}', "", "", "", "", ""])

        await ctx.send(f'```\r\n{self.table.get_string(title=tableTitle)}```')

    def getWeeksInMonth(self, year: int, month: int):
        cal = calendar.Calendar()
        weeks = []
        for week in cal.monthdatescalendar(year, month):
            weeks.append(week[0].isocalendar()[1])
        return weeks


def setup(client):
    client.add_cog(CroissantCogs(client))
