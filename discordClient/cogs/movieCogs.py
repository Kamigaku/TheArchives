from discord.ext import commands
from discordClient.api.imdbAPI import ImdbAPI


class MovieCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = ImdbAPI()

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="msearch")
    async def search(self, ctx, name: str, amount=5):
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

def setup(client):
    client.add_cog(MovieCogs(client))