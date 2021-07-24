from discord.ext import commands
from discord.ext.commands import Context
from discordClient.api.imdbAPI import ImdbAPI
from discordClient.cogs import researchCogs


class MovieCogs(researchCogs.ResearchCogs):

    def __init__(self, bot):
        super().__init__(bot, "movie")
        self.api = ImdbAPI()

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="msearch")
    async def search(self, ctx: Context, name: str):
        await self.search_element(ctx, name)

    @commands.command("massign")
    async def assign(self, ctx: Context, channel_id: str):
        await self.assign_channel(ctx, channel_id)

    @commands.command("mrate")
    async def rate(self, ctx: Context, movie_id: str, rate: str, description: str):
        await self.add_rating(ctx, movie_id, rate, description)

    @commands.command(name="mdelete")
    async def delete(self, ctx: Context, movie_uuid: str):
        await self.delete_rating(ctx, movie_uuid)

    # Override methods
    def retrieve_elements(self, name: str, index: int):
        if self.previousResearch is None:
            self.previousResearch = self.api.retrieveMovies(name)
        return self.previousResearch[index].movieID

    async def format_element(self, ctx, element_id):
        tempMsg = await ctx.send("Retrieving movie...")
        movieEntity = self.api.retrieveMovie(element_id)
        await tempMsg.delete()

        generatedEmbed = self.api.formatMovie(movieEntity)
        for rate in self.rates:
            if rate.element_id == element_id:
                author = await rate.retrieve_member(self.bot)
                generatedEmbed.add_field(name="%s - %s / 20" % (author.display_name, rate.rating), value=rate.comment)


def setup(client):
    client.add_cog(MovieCogs(client))
