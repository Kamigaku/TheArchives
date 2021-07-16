from discord.ext import commands
from discord.ext.commands import Context
from discord import Message
from discord import Reaction
from discord import RawReactionActionEvent
from discordClient.api.malAPI import MalAPI
from mal import Anime
from mal import AnimeSearchResult
from discordClient.config import settings


class AnimeCogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = MalAPI()
        self.messagesToListen = []
        self.previousResearch = None
        self.currentIndex = 0
        if "ANIME_COGS" in settings.configurationFile["COGS_CONFIGURATION"]:
            self.channel_id = settings.configurationFile["COGS_CONFIGURATION"]["ANIME_COGS"]
        else:
            self.channel_id = ""

    # Commands => commands.command va appelé des commandes customs
    @commands.command(name="asearch")
    async def search(self, ctx: Context, name: str):
        if str(ctx.channel.id) == self.channel_id:
            self.currentIndex = 0
            self.previousResearch = None
            anime = self.searchAnime(name, self.currentIndex)
            await self.displayAnime(ctx, anime)

    @commands.command("aassign")
    async def assign(self, ctx: Context, channel_id: str):
        self.channel_id = channel_id
        settings.registerCogChannel("ANIME_COGS", channel_id)
        await ctx.message.delete()

    # Listeners => commands.Cog.listener() va écouter une liste d'event particulier déclenché par discord
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user):
        if reaction.message.id in self.messagesToListen and user.bot is not True:
            ctx = await self.bot.get_context(reaction.message)
            if reaction.emoji == '\N{leftwards black arrow}':
                self.currentIndex -= 1
            else:
                self.currentIndex += 1
            animeEntity = self.searchAnime("", self.currentIndex)
            self.messagesToListen.remove(reaction.message.id)
            await reaction.message.delete()
            await self.displayAnime(ctx, animeEntity)

    # Public methods that helps
    def searchAnime(self, name: str, index: int):
        if self.previousResearch is None:
            self.previousResearch = self.api.retrieveAnimes(name)
        return self.previousResearch.results[index]

    async def displayAnime(self, ctx: Context, anime: Anime):
        tempMsg = await ctx.send("Retrieving animes...")
        animeEntity = self.api.retrieveAnime(anime.mal_id)
        await tempMsg.delete()
        msg = await ctx.send(embed=self.api.formatAnime(animeEntity), delete_after=60)
        await msg.add_reaction('\N{leftwards black arrow}')
        await msg.add_reaction('\N{black rightwards arrow}')
        self.messagesToListen.append(msg.id)

def setup(client):
    client.add_cog(AnimeCogs(client))
