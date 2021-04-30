from discord.ext import commands
from discord import Message
from discordClient.api.malAPI import MalAPI
from mal import AnimeSearchResult


class AnimeCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = MalAPI()

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="asearch")
    async def search(self, ctx, name: str, amount=1):
        await ctx.send("Retrieving animes...")
        animes = self.api.retrieveAnimes(name)
        embeds = []
        cpt = 0
        for anime in animes.results:
            if anime.type == "TV":
                animeEntity = self.api.retrieveAnime(anime.mal_id)
                embeds.append(self.api.formatAnime(animeEntity))
                cpt += 1
                if cpt >= amount:
                    break
        for embed in embeds:
            msg = await ctx.send(embed=embed, delete_after=60)
            await msg.add_reaction('\N{leftwards black arrow}')
            await msg.add_reaction('\N{black rightwards arrow}')


def setup(client):
    client.add_cog(AnimeCogs(client))
