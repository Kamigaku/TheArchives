from discord.ext import commands
from discord.ext.commands import Context
from discordClient.api.imdbAPI import ImdbAPI
from discordClient.config import settings


class MovieCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = ImdbAPI()
        if "MOVIE_COGS" in settings.configurationFile["COGS_CONFIGURATION"]:
            self.channel_id = settings.configurationFile["COGS_CONFIGURATION"]["MOVIE_COGS"]
        else:
            self.channel_id = ""

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="msearch")
    async def search(self, ctx: Context, name: str, amount=5):
        if ctx.channel.id == self.channel_id:
            await ctx.send("Retrieving movies...")
            movies = self.api.retrieveMovies(name)
            embeds = []
            cpt = 0
            for movie in movies:
                movieEntity = self.api.retrieveMovie(movie.movieID)
                embeds.append(self.api.formatMovie(movieEntity))
                cpt += 1
                if cpt >= amount:
                    break
            for embed in embeds:
                await ctx.send(embed=embed)

    @commands.command("massign")
    async def assign(self, ctx: Context, channel_id: str):
        self.channel_id = channel_id
        settings.registerCogChannel("MOVIE_COGS", channel_id)
        await ctx.message.delete()


def setup(client):
    client.add_cog(MovieCogs(client))
