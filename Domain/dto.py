import datetime
from dataclasses import dataclass

from Domain.entities import Person


@dataclass
class PeopleStatistics:
    person = Person
    activites = list

@dataclass
class DaysStatistics:
    day = datetime.date
    activities = list




class PeopleStatsAssembler: #Clasa dto pt persone care are 3 atribute: o persoana de tip Person, activitatile acelei persoane si numarul de activitati la care participa
    def __init__(self, person, activities):
        self.__person = person
        self.__act = []
        for item in activities:
            if person.id in item.prsids:
                self.__act.append(item)
        self.__no_of_act = len(self.__act)

    @property
    def person(self):
        return self.__person

    @property
    def act(self):
        return self.__act

    @property
    def no_of_act(self):
        return self.__no_of_act

    def __str__(self) -> str:
        return " person_id: {0}, person: {1}, number_of_activites: {2}".format(self.person.id, self.person.name, self.no_of_act)

class DaysStatsAssembler:   #Clasa dto pt zile. Are 3 atribute. O zi de tip datetime, activitatile din acea zi si numarul lor
    def __init__(self, day, activities):
        self.__day = day
        self.__act = []
        for item in activities:
            if item.date == self.__day:
                self.__act.append(item)
        self.__no_of_act = len(self.__act)


    @property
    def day(self):
        return self.__day

    @property
    def act(self):
        return self.__act

    @property
    def no_of_act(self):
        return self.__no_of_act

    def __str__(self) -> str:
        return " day: {0}, activities: {1}, number_of_activites: {2}".format(self.day, self.act, self.no_of_act)






