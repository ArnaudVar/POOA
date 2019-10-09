from classes.Exception import SetterException


class Media:

    def __init__(self, name, description, grade, image):
        self._name = name
        self.description = description        self.grade = grade
        self._image = image

    def _get_name(self):
        """
        Méthode appelée lorsque l'on veut accéder au nom du média
        :return: str : le nom de la série
        """
        return self._name

    def _set_name(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier le nom du média

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    def _get_description(self):
        """
        Méthode appelée lorsque l'on veut accéder à la description de la série
        :return: str : la description de la série
        """
        return self._description

    def _set_description(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier la description de la série

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    def _get_image(self):
        """
        Méthode appelée lorsque l'on veut accéder à l'image de la série
        :return: l'image de la série
        """
        return self._image

    def _set_image(self, *args):
        """
        Méthode appelée lorsque l'on veut modifier l'image de la série

        :return: None (on ne peut pas modifier l'attribut)
        """
        raise SetterException('This parameter is private, unable to set it')

    name = property(_get_name, _set_name)
    description = property(_get_description, _set_description)
    image = property(_get_image, _set_image)
