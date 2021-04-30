from mal import *
import discord


class MalAPI:

    def __init__(self):
            print("MAL API Init")

    def retrieveAnimes(self, name):
        return AnimeSearch(name)

    def retrieveAnime(self, animeId):
        return Anime(animeId)

    def formatAnime(self, anime: Anime):
        animeGenres = ""
        for genre in anime.genres:
            animeGenres += genre + ", "
        animeGenres = animeGenres[:-2]
        embed = discord.Embed(title=anime.title, colour=discord.Colour(0x28f0cc),
                              url=anime.url, description=anime.synopsis)
        embed.set_thumbnail(url=anime.image_url)
        embed.set_footer(text=f'Rating: {anime.score}/10 - Genres: {animeGenres} - Anime id: {anime.mal_id}',
                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Star_full.svg/1200px-Star_full.svg.png")
        return embed
