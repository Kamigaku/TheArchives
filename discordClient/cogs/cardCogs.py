import random
import uuid
from peewee import DoesNotExist
from discord.ext import commands
from discord.ext.commands import Context
from discord import Colour, Embed, RawReactionActionEvent
from discordClient.cogs.abstract import assignableCogs
from discordClient.model.models import Character, CharactersOwnership, Affiliation, CharacterAffiliation, Economy

rarities_label = ["E", "D", "C", "B", "A", "S", "SS"]
rarities_colors_hex = ["9B9B9B", "FFFFFF", "69e15e", "4ccfff", "f0b71c", "f08033", "8f39ce"]
rarities_colors = [Colour(0x9B9B9B), Colour(0xFFFFFF), Colour(0x69e15e), Colour(0x4ccfff), Colour(0xf0b71c),
                   Colour(0xf08033), Colour(0x8f39ce)]
rarities_img_url = "https://www.colorhexa.com/{}.png"


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
            await ctx.channel.send(content=f"Booster generated for user {ctx.message.author.mention}")
            for _ in range(5):
                character_generated = distribute_random_character([50, 25, 12.5, 9, 3, 0.5])
                msg = await display_character(ctx, character_generated)
                ownership_model, has_created_model = CharactersOwnership.get_or_create(
                    discord_user_id=ctx.author.id, character_id=character_generated.get_id(), message_id=msg.id)
                ownership_model.save()
            user_model.amount -= 20
            user_model.save()
        else:
            await ctx.author.send("You don't have enough biteCoin to buy a booster.")

    ################################
    #       LISTENER COGS          #
    ################################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.member.bot is not True and payload.event_type == "REACTION_ADD":
            try:
                owner = CharactersOwnership.get(message_id=payload.message_id)
                if owner.discord_user_id == payload.user_id:
                    user_model, user_created = Economy.get_or_create(discord_user_id=payload.member.id)
                    character_concerned = Character.get_by_id(owner.character_id)
                    user_model.amount += character_concerned.rarity
                    user_model.save()
                    owner.delete_instance()
                    await payload.member.send(f"You have sold for {character_concerned.rarity} biteCoin the card "
                                              f"\"{character_concerned.name}\".")
                    return
                else:
                    await payload.member.send("You are not the owner of the card.")
                    channel = self.bot.get_channel(payload.channel_id)
                    msg = await channel.fetch_message(payload.message_id)
                    await msg.remove_reaction(payload.emoji, payload.member)
            except DoesNotExist:
                channel = self.bot.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction(payload.emoji, payload.member)
                pass


def distribute_random_character(rarities):
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


def generate_embed_character(character: Character):
    if len(character.description) > 255:
        character_description = character.description[:255] + "..."
    else:
        character_description = character.description

    embed = Embed(colour=rarities_colors[character.rarity], description=character_description)

    # Thumbnail
    embed.set_thumbnail(url=character.image_link)

    # Author
    embed.set_author(name=character.name, icon_url= rarities_img_url.format(rarities_colors_hex[character.rarity]),
                     url="")

    # Footer
    footer_text = f"Rarity: {rarities_label[character.rarity]}"
    affiliation = ""
    for current_affiliation in (Affiliation.select()
                                           .join(CharacterAffiliation)
                                           .join(Character)
                                           .where(CharacterAffiliation.character_id == character.get_id())
                                           .group_by(Affiliation)):
        if affiliation:
            affiliation += ", "
        affiliation += current_affiliation.name
    if affiliation:
        footer_text += f" | Affiliation(s): {affiliation}"
    embed.set_footer(text=footer_text, icon_url=rarities_img_url.format(rarities_colors_hex[character.rarity]))

    return embed


async def display_character(ctx: Context, character: Character):
    character_embed = generate_embed_character(character)
    msg = await ctx.channel.send(embed=character_embed)
    await msg.add_reaction('💰')
    return msg
