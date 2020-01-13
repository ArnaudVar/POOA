'''
Regroupe les exceptions utilisées dans les autres classes
'''

class SetterException(Exception):
    '''
    Exception lorsqu'on essaye de set un attribut d'une classe qui ne peut pas être set
    '''
    pass


class AttributeException(Exception):
    '''
    Exception quand on set un attribut du mauvais type dans une classe
    '''
    pass

