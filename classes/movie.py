from classes.Exception import SetterException
from classes.media import Media


class Movie(Media):

    def __init__(self, id, name, description, grade, image, genre, date):
        Media.__init__(self, name=name,description=description,grade=grade,image=image)
        self.id = id
        self._genre = genre
        self.date = date
