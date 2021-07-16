import discord
import uuid

class Rating():

    def __init__(self, author: str, element_id: str, rating: int, comment: str):
        self.author = author
        self.element_id = element_id
        self.rating = rating
        self.comment = comment
        self.uuid = uuid.uuid4()

    def formatRating(self):
        pass

