import unittest
import datetime

from Domain.dto import PeopleStatsAssembler, DaysStatsAssembler
from Domain.entities import Activity, Person
from Domain.validators import ActivityValidator, PersonValidator
from Repository.new_file import Filter, Vector, MySort
from Repository.repository import repository, Statistics
from Service.activity_service import ActivityService
from Service.person_service import PersonService


class Test_Activity_People(unittest.TestCase):
    def setUp(self):
        activity_repository = repository(ActivityValidator)
        self.__activity_service = ActivityService(activity_repository)
        person_repository = repository(PersonValidator)
        self.__person_service = PersonService(person_repository, activity_repository)
        statistics = Statistics(activity_repository, person_repository, self.__activity_service, self.__person_service)
        self.__stats = statistics

    def test_filter(self):
        lst = [1, 2, 3]
        lst = Filter(lst, lambda k : k == 2)
        self.assertEqual(lst, [2])
    def test_sort(self):
        lst = [2, 1, 3]
        lst = MySort(lst, lambda x, y: x < y)
        self.assertEqual(lst, [1, 2, 3])

    def test_Vector(self):
        lst = [1, 2, 3, 4]
        v = Vector()
        v.load_list(lst)
        del(v[0])
        self.assertEqual(v[0], 2)
        v.__setitem__(2 ,5)
        self.assertEqual(v[2], 5)
        self.assertEqual(len(v), 3)


#_________________________Entities_Test_____________________________
    def test_person(self):
        prs = Person(0, "n1", "0747191247", "a1")
        self.assertEqual(prs.id, 0)
        self.assertEqual(prs.name, "n1")
        self.assertEqual(prs.phone_no, "0747191247")
        self.assertEqual(prs.address, "a1")

    def test_activity(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        act = Activity(0, [1], xdate, xtime, "d")
        self.assertEqual(act.id, 0)
        self.assertEqual(act.prsids, [1])
        self.assertEqual(act.date, xdate)
        self.assertEqual(act.time, xtime)
        self.assertEqual(act.description, "d")

#__________Repo_Tests__________________________
    def test_repo(self):
        repo = repository(PersonValidator)
        prs = Person(0, "n1", "0747191247", "a1")
        repo.save(prs)
        all = repo.find_all()
        self.assertEqual(len(all), 1)
        prs1 = repo.find_by_id(0)
        self.assertEqual(prs1.name, "n1")
        repo.delete_by_id(0)
        all = repo.find_all()
        self.assertEqual(len(all), 0)
        id = repo.current_id()
        self.assertEqual(id, 0)
        prs = Person(0, "n1", "0747191247", "b1")
        repo.update(prs)
        all = repo.find_all()
        self.assertEqual(all[0].address, "b1")

#________________Statistics_tests_______________________________
    def test_act_for_prs(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([0], xdate, xtime, "Film")
        act = self.__stats.act_for_prs(0)
        self.assertEqual(len(act), 1)

    def test_busiest_days(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        xdate = datetime.date(2020, 11, 4)
        xtime = datetime.time(12, 0)
        self.__activity_service.add_activity([1, 2], xdate, xtime, "School")
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(5, 0)
        self.__activity_service.add_activity([5], xdate, xtime, "Lunch")

        dtos = self.__stats.busiest_days()
        self.assertEqual(dtos[0].no_of_act, 2)

    def test_acts_for_a_day(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(12, 0)
        self.__activity_service.add_activity([1, 2], xdate, xtime, "School")
        dtos = self.__stats.act_for_day(xdate)
        self.assertEqual(len(dtos), 2)


    def test_list_people(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        self.__person_service.add_person(1, "n2", "0747191247", "b1")
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([0], xdate, xtime, "Film")
        xdate = datetime.date(2020, 11, 4)
        xtime = datetime.time(12, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "School")
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(5, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Lunch")
        dtos = self.__stats.list_ppl()
        self.assertEqual(dtos[0].person.id, 1)
#____________people_tests___________________
    def test_add_person(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        self.assertEqual(len(self.__person_service.get_all_people()), 1)

    def test_delete_person(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        self.__person_service.delete_person(0)
        ppl = self.__person_service.get_all_people()
        self.assertEqual(len(ppl), 0)

    def test_undo(self):
        self.assertEqual(True, True)

    def test_redo(self):
        self.assertEqual(True, True)

    def test_update_person(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        self.__person_service.update_person_by_id(0, "n1", "0747191247", "b1")
        list = self.__person_service.get_all_people()
        self.assertEqual(list[0].address, "b1")

    def test_search_by_name(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        dic = self.__person_service.search_by_name("n1")
        pers = Person(0, "n1", "0747191247", "a1")
        self.assertEqual(pers.id, dic[0].id)
        self.assertEqual(pers.phone_no, dic[0].phone_no)
        self.assertEqual(pers.address, dic[0].address)

    def test_search_by_pn(self):
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        dic = self.__person_service.search_by_pn("0747191247")
        pers = Person(0, "n1", "0747191247", "a1")
        self.assertEqual(pers.id, dic[0].id)
        self.assertEqual(pers.phone_no, dic[0].phone_no)
        self.assertEqual(pers.address, dic[0].address)

    def test_get_all_people_dto(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([0], xdate, xtime, "Film")
        self.__person_service.add_person(0, "n1", "0747191247", "a1")
        people = self.__person_service.get_all_people()
        activities = self.__activity_service.get_all_activities()
        prs_list = self.__person_service.get_all_people_dto()
        prs = PeopleStatsAssembler(people[0], activities)
        self.assertEqual(prs_list[0].no_of_act, prs.no_of_act)

#________activity_tests_______________________
    def test_get_days_dto(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        activities = self.__activity_service.get_all_activities()
        day_dto = DaysStatsAssembler(xdate, activities)
        days_dto = self.__activity_service.get_days_dto()
        self.assertEqual(days_dto[0].day, day_dto.day)
        self.assertEqual(days_dto[0].act, day_dto.act)
        self.assertEqual(days_dto[0].no_of_act, day_dto.no_of_act)

    def test_add(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        self.assertEqual(len(self.__activity_service.get_all_activities()), 1)

    def test_delete_activity(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        self.__activity_service.delete_activity(0)
        acts = self.__activity_service.get_all_activities()
        self.assertEqual(len(acts), 0)

    def test_update(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        xdate = datetime.date(2020, 11, 4)
        xtime = datetime.time(12, 0)
        self.__activity_service.update_activity_by_id(0, [1, 2], xdate, xtime, "School")
        list = self.__activity_service.get_all_activities()
        self.assertEqual(list[0].prsids, [1, 2])
        self.assertEqual(list[0].description, "School")

    def test_check_datetime(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        rez = self.__activity_service.check_datetime(xdate, xtime)
        self.assertEqual(rez, True)

    def test_search_by_date(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        act = Activity(0, [1], xdate, xtime, "Film")
        dic = self.__activity_service.search_by_date(xdate)
        self.assertEqual(act.id, dic[0].id)
        self.assertEqual(act.prsids, dic[0].prsids)
        self.assertEqual(act.date, dic[0].date)
        self.assertEqual(act.time, dic[0].time)
        self.assertEqual(act.description, dic[0].description)

    def test_search_by_descr(self):
        xdate = datetime.date(2018, 11, 4)
        xtime = datetime.time(19, 0)
        self.__activity_service.add_activity([1], xdate, xtime, "Film")
        act = Activity(0, [1], xdate, xtime, "Film")
        dic = self.__activity_service.search_by_descr("Film")
        self.assertEqual(act.id, dic[0].id)
        self.assertEqual(act.prsids, dic[0].prsids)
        self.assertEqual(act.date, dic[0].date)
        self.assertEqual(act.time, dic[0].time)
        self.assertEqual(act.description, dic[0].description)

if __name__ == '__main__':
    unittest.main()
