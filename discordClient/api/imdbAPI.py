from imdb import IMDb, Movie
import discord


class ImdbAPI:

    def __init__(self):
        self.db = IMDb()

    def retrieveMovies(self, name):
        return self.db.search_movie(name)

    def retrieveMovie(self, movieId):
        return self.db.get_movie(movieId)

    def formatMovie(self, movie: Movie):
        moviePlot = "No plot has been found."
        if "plot" in movie.data:
            moviePlot = movie["plot"][0].split("::")[0]
        movieRating = "Unrated"
        if "rating" in movie.data:
            movieRating = movie.data["rating"]
        movieGenres = "Undefined"
        if "genres" in movie.data:
            movieGenres = ""
            for genre in movie.data["genres"]:
                movieGenres += genre + ", "
            movieGenres = movieGenres[:-2]

        embed = discord.Embed(title=movie.data["title"], colour=discord.Colour(0x28f0cc),
                              url=f'https://www.imdb.com/title/tt{movie.movieID}', description=moviePlot)
        if "cover url" in movie:
            embed.set_thumbnail(url=movie["cover url"])
        else:
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text=f'Rating: {movieRating}/10 - Genres: {movieGenres} - Movie id: {movie.movieID}',
                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Star_full.svg/1200px-Star_full.svg.png")
        return embed
