import random
import uuid
import os
from peewee import fn
from peewee import DoesNotExist
from discord.ext import commands
from discord.ext.commands import Context
from discord import File
from discordClient.cogs.abstract import assignableCogs
from discordClient.model.models import Character, CharactersOwnership, Affiliation, CharacterAffiliation, Economy
from discordClient.creator import card_creator


class CardCogs(assignableCogs.AssignableCogs):

    def __init__(self, bot):
        super().__init__(bot, "card")

    @commands.command("cards assign")
    async def assign(self, ctx: Context, channel_id: str):
        await self.assign_channel(ctx, channel_id)

    @commands.command("cards display")
    async def display_boosters(self, ctx: Context):
        pass

    @commands.command("cards_buy")
    async def buy_booster(self, ctx: Context):
        user_model, user_created = Economy.get_or_create(discord_user_id=ctx.author.id)
        if user_model.amount >= 20:
            booster_uuid = uuid.uuid4()
            random.seed(booster_uuid.hex)
            characters_selected = []
            for _ in range(5):
                characters_selected.append(self.distribute_random_character([50, 25, 12.5, 9, 3, 0.5]))
            i = 0
            while i < len(characters_selected):
                ownership_model, has_created_model = CharactersOwnership.get_or_create(CharactersOwnership.discord_user_id == ctx.author.id & CharactersOwnership.character_id == characters_selected[i].get_id())
                ownership_model.amount += 1
                ownership_model.save()
                i += 1
            user_model.amount -= 20
            user_model.save()
            front_pictures, back_pictures = self.generate_characters_picture(booster_uuid, characters_selected)
            global_pictures = card_creator.gather_pictures_in_one(front_pictures, 10, 10, 10, 10)
            global_pictures.save("global_picture_{}.jpg".format(booster_uuid.hex))
            with open("global_picture_{}.jpg".format(booster_uuid.hex), "rb") as f:
                picture = File(f)
                await ctx.channel.send(file=picture)
            os.remove("global_picture_{}.jpg".format(booster_uuid.hex))
        else:
            await ctx.author.send("You don't have enough biteCoin to buy a booster.")

    def distribute_random_character(self, rarities):
        value = random.random() * 100
        current_rarity = 0
        rarity_index = 1
        for rarity in rarities:
            current_rarity += rarity
            if current_rarity > value:
                break
            rarity_index += 1
        characters = Character.select().where(Character.rarity == rarity_index)
        return characters[random.randrange(0, len(characters) - 1)]

    def generate_characters_picture(self, default_uuid: uuid, characters):
        random.seed(default_uuid.hex)
        characters_picture_front = []
        characters_picture_back = []
        for character in characters:
            affiliation = ""
            for current_affiliation in (Affiliation.select().join(CharacterAffiliation).join(Character).where(CharacterAffiliation.character_id == character.get_id()).group_by(Affiliation)):
                if affiliation:
                    affiliation += "\n"
                affiliation += current_affiliation.name
            front, back = card_creator.create_card(random.random(), character.name, character.image_link,
                                                   character.description.encode().decode("ISO-8859-1", 'replace'),
                                                   character.rarity, affiliation)
            characters_picture_front.append(front)
            characters_picture_back.append(back)
        return characters_picture_front, characters_picture_back
