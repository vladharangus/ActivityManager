from Domain.dto import DaysStatsAssembler
from Domain.entities import Activity
from Service.handlers import UndoHandler
from Service.manager import UndoManager


class ActivityService(object):
    def __init__(self, act_repo):
        self.__repository = act_repo
    def add_activity(self, prsids, date, time, description):
        id = self.__repository.current_id()
        new_act = Activity(id, prsids, date, time, description)
        UndoManager.register_operation(self, UndoHandler.ADD_ACTIVITY, id, prsids, date, time, description)
        self.__repository.save(new_act)
    def get_all_activities(self):
        return self.__repository.find_all()
    def delete_activity(self, id):
        act = self.__repository.find_by_id(id)
        UndoManager.register_operation(self, UndoHandler.DELETE_ACTIVITY, id, act.prsids, act.date, act.time, act.description)
        self.__repository.delete_by_id(id)
    def update_activity_by_id(self, id, prsids, date, time, description):
        entity = self.__repository.find_by_id(id)
        UndoManager.register_operation(self, UndoHandler.UPDATE_ACTIVITY, entity.id, entity.prsids, entity.date, entity.time, entity.description, prsids, date, time, description)
        entity.prsids = prsids
        entity.date = date
        entity.time = time
        entity.description = description
        self.__repository.update(entity)
    def check_datetime(self, date, time):
        entity = self.get_all_activities()
        for item in entity:
            if(item.date == date and item.time == time):
                return True
        return False
    def search_by_date(self, date):
        entity = self.get_all_activities()
        dic = []
        for item in entity:
            if item.date == date:
                dic.append(item)
        return dic
    def search_by_descr(self, d):
        entity = self.get_all_activities()
        dic = []
        for item in entity:
            aux = item.description
            if aux.lower().find(d.lower()) != -1:
                dic.append(item)
        return dic

    def get_days_dto(self):
        activities = self.get_all_activities() #imi iau toate activitatile
        days_dto = []
        for item in activities:
            day_dto = DaysStatsAssembler(item.date, activities) #construiesc un obiect dto de tip DaysStatsAssembler
            if day_dto not in days_dto: #daca nu apare in lista, il adaug
                days_dto.append(day_dto)

        return days_dto
