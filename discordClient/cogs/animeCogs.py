from discord.ext import commands
from discord.ext.commands import Context
from discordClient.api.malAPI import MalAPI
from discordClient.cogs import researchCogs


class AnimeCogs(researchCogs.ResearchCogs):

    def __init__(self, bot):
        super().__init__(bot, "anime")
        self.api = MalAPI()

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="asearch")
    async def search(self, ctx: Context, name: str):
        await self.search_element(ctx, name)

    @commands.command("aassign")
    async def assign(self, ctx: Context, channel_id: str):
        await self.assign_channel(ctx, channel_id)

    @commands.command("arate")
    async def rate(self, ctx: Context, anime_id: str, rate: str, description: str):
        await self.add_rating(ctx, anime_id, rate, description)

    @commands.command(name="adelete")
    async def delete(self, ctx: Context, element_id: str):
        await self.delete_rating(ctx, element_id)

    # Override methods
    def retrieve_elements(self, name: str, index: int):
        if self.previousResearch is None:
            self.previousResearch = self.api.retrieveAnimes(name)
        return self.previousResearch.results[index].mal_id

    async def format_element(self, ctx, element_id):
        tempMsg = await ctx.send("Retrieving anime...")
        animeEntity = self.api.retrieveAnime(element_id)
        await tempMsg.delete()

        generatedEmbed = self.api.formatAnime(animeEntity)
        for rate in self.rates:
            if rate.element_id == str(element_id):
                author = await rate.retrieve_member(self.bot)
                generatedEmbed.add_field(name="%s - %s / 20" % (author.display_name, rate.rating), value=rate.comment)
        return generatedEmbed


def setup(client):
    client.add_cog(AnimeCogs(client))
