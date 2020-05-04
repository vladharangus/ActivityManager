import datetime

from Domain.entities import Person, Activity
from Repository.new_file import Vector, Filter, MySort


class repository:
    def __init__(self, validatior_class):
        self._entities = Vector()
        self.__validator_class = validatior_class

    def save(self, entity):
        self.__validator_class.validate(entity)
        lst = self._entities[:]
        lst.append(entity)
        self._entities.load_list(lst)

    def find_all(self):
        return self._entities
        #return list(self._entities.values())

    def find_by_id(self, id):
        return self._entities[id]

    def update(self, new_entity):
        self.save(new_entity)

    def delete_by_id(self,id):
        del self._entities[id]

    def current_id(self):
        return len(self._entities)

class prs_file_repo(repository):
    def __init__(self, filename, validators):
        self.__filename = filename
        repository.__init__(self, validators)
        self.read()
    def read(self):
        try:
            file = open(self.__filename, "r")
            line = file.readline().strip()
            while line != "":
                line = line.split(";")
                prs = Person(int(line[0].strip()), line[1].strip(), line[2].strip(), line[3].strip())
                repository.save(self, prs)
                line = file.readline().strip()
            file.close()
        except IOError:
            print("Error")
    def write(self):
        list = self.find_all()
        file = open(self.__filename, "w")
        for prs in list:
            string = str(prs.id) + ";" + str(prs.name) + ";" + str(prs.phone_no) + ";" + str(prs.address) + "\n"
            file.write(string)
        file.close()

    def save(self, entity):
        repository.save(self, entity)
        self.write()

    def find_all(self):
        return repository.find_all(self)

    def find_by_id(self, id):
        return repository.find_by_id(self, id)

    def update(self, new_entity):
        repository.update(self, new_entity)
        self.write()

    def delete_by_id(self,id):
        repository.delete_by_id(self,id)
        self.write()

    def current_id(self):
        return repository.current_id(self)


class acts_file_repo(repository):
    def __init__(self, filename, validators):
        self.__filename = filename
        repository.__init__(self, validators)
        self.read()
    def read(self):
        try:
            file = open(self.__filename, "r")
            line = file.readline().strip()
            while line != "":
                line = line.split(";")
                #print(line[0].strip())
                line[1] = line[1][1:len(line[1]) - 1].strip().split(",")
                for i in range(len(line[1])):
                    line[1][i] = int(line[1][i])
                line[2] = line[2].strip().split("-")
                for i in range(len(line[2])):
                    line[2][i] = int(line[2][i])
                date = datetime.date(line[2][0], line[2][1], line[2][2])
                line[3] = line[3].strip().split(":")
                for i in range(len(line[2])):
                    line[3][i] = int(line[3][i])
                time = datetime.time(line[3][0], line[3][1], line[3][2])

                act = Activity(int(line[0].strip()), line[1], date, time, line[4].strip())
                repository.save(self, act)
                line = file.readline().strip()

            file.close()
        except IOError:
            print("Error")
    def write(self):
        list = self.find_all()
        file = open(self.__filename, "w")
        for acts in list:
            string = str(acts.id) + ";" + str(acts.prsids) + ";" + str(acts.date) + ";" + str(acts.time) + ";" + str(acts.description) +  "\n"
            file.write(string)
        file.close()

    def save(self, entity):
        repository.save(self, entity)
        self.write()

    def find_all(self):
        return repository.find_all(self)

    def find_by_id(self, id):
        return repository.find_by_id(self, id)

    def update(self, new_entity):
        repository.update(self, new_entity)
        self.write()

    def delete_by_id(self,id):
        repository.delete_by_id(self,id)
        self.write()

    def current_id(self):
        return repository.current_id(self)



class Statistics(object):
    def __init__(self, act_rep, prs_rep, act_service, prs_service):
        self.__act_rep = act_rep
        self.__prs_rep = prs_rep
        self.__act_service = act_service
        self.__prs_service = prs_service

#___________Stats_for_people________________________

    def act_for_prs(self, id):
        people_dto = self.__prs_service.get_all_people_dto()
        v = Vector()
        v.load_list(people_dto)
        list = Filter(v, lambda x: x.person.id == id)
        return list[0].act

    def list_ppl(self):
        people_dto = self.__prs_service.get_all_people_dto()
        v = Vector()
        v.load_list(people_dto)
        list = MySort(v, lambda x, y: x.no_of_act >= y.no_of_act)
        return list

#_______________Stats_for_activites___________________

    def act_for_day(self, day):
        days_dto = self.__act_service.get_days_dto()
        v = Vector()
        v.load_list(days_dto)
        list  = Filter(v, lambda x : x.day == day)
        if list == []:
            return []
        return list[0].act

    def busiest_days(self):
        days_dto = self.__act_service.get_days_dto()
        v = Vector()
        v.load_list(days_dto)
        print(len(v))
        list = MySort(v, lambda x, y: x.no_of_act >= y.no_of_act)
        return list