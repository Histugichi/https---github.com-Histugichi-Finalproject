class Evenement:
    def __init__(self,nom, date,emplacement,prix,id_evenement) -> None:
        self.__nom = nom
        self.__date= date
        self.__emplacement = emplacement
        self.__prix = prix
        self.__id_evenement= id_evenement
    

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, value):
        self.__nom = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def emplacement(self):
        return self.__emplacement

    @emplacement.setter
    def emplacement(self, value):
        self.__emplacement = value

    @property
    def prix(self):
        return self.__prix

    @prix.setter
    def prix(self, value):
        self.__prix = value
    
    @property
    def id_evenement(self):
        return self.__id_evenement

    @id_evenement.setter
    def id_evenement(self, value):
        self.__id_evenement = value

