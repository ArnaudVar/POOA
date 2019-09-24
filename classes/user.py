class User :
    __id = 0
    def __init__(self, name, surname, password):
        self.__id = User.__id
        self.__password = password
        self.series = {}
        self.name = name
        self.surname = surname

    def add_serie(self, serie):
        self.series[serie.nom] = 'S1E1'

    def remove_serie(self, serie):
        del self.series[serie.nom]

    def next_episode(self,serie):
        if serie.nom not in self.series.keys() :
            raise ValueError("Série non commencée")
        else :
            separation = self.series[serie.nom].split('E')
            number_season = int(separation[0].split('S')[1])
            number_episode = separation[1]
            number_episode= int(number_episode)
            if number_episode == len(serie.seasons[number_season-1].episodes) :
                self.series[serie.nom] = 'S'+ str(number_season + 1) +'E1'
            else :
                self.series[serie.nom] = separation[0] + 'E' + str(number_episode + 1)


