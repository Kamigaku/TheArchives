import os
import jsonpickle
from discord.ext import commands
from discordClient.model import rating
from discordClient.cogs import assignableCogs


class ResearchCogs(assignableCogs.AssignableCogs):

    def __init__(self, bot, name):
        super().__init__(bot, name)
        self.rates = []
        self.messagesToListen = []
        self.previousResearch = None
        self.currentIndex = 0
        if os.path.exists(self.cogs_name + ".json"):
            file = open(self.cogs_name + ".json", "r")
            self.rates = jsonpickle.decode(file.read())

    async def search_element(self, ctx, name: str):
        if str(ctx.channel.id) == self.channel_id:
            self.currentIndex = 0
            self.previousResearch = None
            element_id = self.retrieve_elements(name, self.currentIndex)
            await self.display_element(ctx, element_id)

    async def add_rating(self, ctx, element_id, rate, description):
        if str(ctx.channel.id) == self.channel_id:
            rating_split = rate.split("/")
            await ctx.message.delete()
            if len(rating_split) != 2:
                await ctx.send("The rate has to be formatted the following way \"x/y\".", delete_after=10)
            else:
                rateX = float(rating_split[0].replace(",", "."))
                rateY = float(rating_split[1].replace(",", "."))
                newRate = rating.Rating(ctx.author.id, element_id, (rateX / rateY) * 20, description)
                self.rates.append(newRate)
                self.save_ratings()
                await ctx.send("Rating has been added :)", delete_after=10)

    async def delete_rating(self, ctx, element_id):
        if str(ctx.channel.id) == self.channel_id:
            for rate in self.rates:
                if str(rate.uuid) == element_id:
                    self.rates.remove(rate)
            self.save_ratings()
            await ctx.message.delete()
            await ctx.send(content="The rate has been successfully removed! 😃", delete_after=60)

    async def display_element(self, ctx, element_id):
        embed_message = await self.format_element(ctx, element_id)
        msg = await ctx.send(embed=embed_message, delete_after=60)
        await msg.add_reaction('\N{leftwards black arrow}')
        await msg.add_reaction('\N{black rightwards arrow}')
        self.messagesToListen.append(msg.id)

    def save_ratings(self):
        f = open(self.cogs_name + ".json", "w")
        f.write(jsonpickle.encode(self.rates))
        f.close()

    ################################
    #     OVERRIDABLE METHODS      #
    ################################

    def retrieve_elements(self, name: str, index: int):
        return None

    async def format_element(self, ctx, element_id):
        return None

    ################################
    #       LISTENER COGS          #
    ################################

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if str(message.channel.id) == self.channel_id and message.id in self.messagesToListen:
            self.messagesToListen.remove(message.id)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id in self.messagesToListen and user.bot is not True:
            ctx = await self.bot.get_context(reaction.message)
            if reaction.emoji == '\N{leftwards black arrow}':
                self.currentIndex -= 1
            else:
                self.currentIndex += 1
            searchResult = self.retrieve_elements("", self.currentIndex)
            await reaction.message.delete()
            await self.display_element(ctx, searchResult)
