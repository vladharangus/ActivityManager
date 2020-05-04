from Domain.dto import PeopleStatsAssembler
from Domain.entities import Person
from Service.handlers import UndoHandler
from Service.manager import UndoManager


class PersonService(object):
    def __init__(self, prs_repo, act_repo):
        self.__repository = prs_repo
        self.__act_repo = act_repo
    def get_all_people(self):
        return self.__repository.find_all()

    def add_person(self, id, name, phone_no, address):
        new_prs = Person(id, name, phone_no, address)
        acts = self.__act_repo.find_all()
        Acts = []
        for act in acts:
            if id in act.prsids:
                Acts.append(act)
        UndoManager.register_operation(self, UndoHandler.ADD_PERSON, acts, id, name, phone_no, address)
        self.__repository.save(new_prs)

    def exist_id(self, id):
        people = self.get_all_people()
        for item in people:
            if id == item.id:
                return True
        return False

    def delete_person(self, id):
        activities = self.__act_repo.find_all()
        prs = self.__repository.find_by_id(id)
        acts = []
        for item in activities:
            if id in item.prsids:
                item.prsids.remove(id)
                acts.append(item)
        UndoManager.register_operation(self, UndoHandler.DELETE_PERSON, acts, prs.id, prs.name, prs.phone_no, prs.address)
        self.__repository.delete_by_id(id)

    def update_person_by_id(self, id, name, phone_no, address):
        entity = self.__repository.find_by_id(id)

        UndoManager.register_operation(self, UndoHandler.UPDATE_PERSON, id, entity.name, entity.phone_no, entity.address, name, phone_no, address)

        entity.name = name
        entity.phone_no = phone_no
        entity.address = address
        self.__repository.update(entity)

    def search_by_name(self, name):
        entity = self.get_all_people()
        dic = []
        for item in entity:
            aux = item.name
            if aux.lower().find(name) != -1:
                dic.append(item)
        return dic

    def search_by_pn(self, name):
        entity = self.get_all_people()
        dic = []
        for item in entity:
            if item.phone_no.find(name) != -1:
                dic.append(item)
        return dic

    def get_all_people_dto(self):
        people_dto = []
        people = self.get_all_people()
        activities = self.__act_repo.find_all()
        for item in people:
            prs = PeopleStatsAssembler(item, activities)
            people_dto.append(prs)
        return people_dto