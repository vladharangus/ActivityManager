class Activity:
    def __init__(self, id, prsids, date, time, description):
        self.__id = id
        self.__prsids = prsids
        self.__date = date
        self.__time = time
        self.__description = description

    @property
    def id(self):
        return self.__id

    @property
    def prsids(self):
        return self.__prsids

    @prsids.setter
    def prsids(self, value):
        self.__prsids = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    def __str__(self) -> str:
        return " id: {0}, ids_of_people: {1}, date: {2}, time: {3}, description: {4}".format(self.id, self.prsids, self.date,
                                                                                        self.time, self.description)

class Person:
    def __init__(self, id, name, phone_no, address):
        self.__id = id
        self.__name = name
        self.__phone_no = phone_no
        self.__address = address

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def phone_no(self):
        return self.__phone_no

    @phone_no.setter
    def phone_no(self, value):
        self.__phone_no = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value


    def __str__(self) -> str:
        return " id: {0}, name: {1}, phone_number: {2}, address: {3}".format(self.id, self.name, self.phone_no, self.address)


