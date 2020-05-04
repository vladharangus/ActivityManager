import datetime
import random

from Domain.validators import PersonError
from Service.Redo.Redo_Manager import RedoManager
from Service.manager import UndoManager


class Console(object):
    def __init__(self, activity_service, person_service, stats):
        self.__activity_service = activity_service
        self.__person_service = person_service
        self.__stats = stats

    def run_menu(self):
        try:
            #self.__generate_entities()
            options = {1 : self.__ui_add_activities, 2 : self.__ui_remove_activity,
                        3 : self.__ui_print_activities, 4 : self.__ui_update_activity, 5 : self.__ui_print_people,
                        6 : self.__ui_add_people, 7 : self.__ui_reomove_person, 8 : self.__ui_update_person, 9 : self.__ui_search_activity,
                        10 : self.__ui_search_people, 11 : self.__ui_activities_with_a_given_person,
                        12 : self.__ui_activities_on_a_day, 13 : self.__ui_list_people, 14 : self.__ui_busiest_days, 15 : self.__ui_undo, 16 : self.__ui_redo}
            while True:
                try:
                    self.__print_options()
                    option = input("Choose an option: ")
                    if option == "exit":
                        break
                    else:
                        option = int(option)
                        options[option]()
                except KeyError:
                    print("This command does not exist")
        except PersonError as se:
            print("caught StoreError: ", se)

    def __print_options(self):
        print("You have the following options: \n"
              "1. Add activity \n"
              "2. Remove activity \n"
              "3. Show activities \n"
              "4. Update an activity \n"
              "5. Show people \n"
              "6. Add people \n"
              "7. Delete a person \n"
              "8. Update a person \n"
              "9. Search an activity \n"
              "10. Search a person \n"
              "11. Show activities for a certain person \n"
              "12. Show all activities which take place on a certain day \n"
              "13. Show all the people in descending order by the number of activites they take part in \n"
              "14. Show the busiest days \n"
              "15. Undo \n"
              "16. Redo \n"
              "Exit")

    def generate_entities(self):
        number_of_entities = 100
        addresses = ["Plopilor", "Regele Ferdinand", "Dragos VOda", "Calea Baciului", "Magnoliei", "Memorandumului", "Universitatii", "21 Decembrie", "Eroilor", "A.I. Cuza"]
        phone_numbers = ["0747191247", "0746185625", "0732754624", "0711111111", "0799999999", "0712345678"]
        first_names = ["Ioana", "Alex", "Vlad", "Dargos", "Bogdan", "Maria", "Andreea", "Denisa", "Madalina", "Tudor", "Iulian", "Cristian", "Alin"]
        last_names = ["Harangus", "Jercan", "Pop", "Ionescu", "Tanase", "Rusescu", "Atanasoaiei", "Medan", "Petcu"]
        descriptions = ["Film", "Theatre", "Dinner", "Lunch", "Business meeting", "Doctor", "Project", "Team building", "Lectures", "Video games", "Party", "Stroll"]
        for i in range(0, number_of_entities):
            address = random.choice(addresses)
            name = random.choice(first_names) + " " + random.choice(last_names)
            phone_number = random.choice(phone_numbers)

            self.__person_service.add_person(i, name, phone_number, address)

            year = random.randint(2018, 2066)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            hour = random.randint(1, 12)
            minute = random.randint(0, 59)
            date = datetime.date(year, month, day)
            time = datetime.time(hour, minute)

            nb_of_people = random.randint(1, 5)
            prsids = []
            for i in range(0, nb_of_people):
                id = random.randint(0, len(self.__person_service.get_all_people()) - 1)
                prsids.append(id)

            self.__activity_service.add_activity(prsids, date, time, random.choice(descriptions))
        UndoManager.clear_op()

#_____________________________________________The UI functions for activities___________________________________________

    def __ui_print_activities(self):
        acts = self.__activity_service.get_all_activities()
        for item in acts:
            print(item)

    def __ui_add_activities(self):
        try:
            prsids = []
            nrprs = int(input("Insert the number of people who take part in activity: "))
            for x in range(0,nrprs):
                prsid = int(input("Type person id: "))
                while self.__person_service.exist_id(prsid) is False:
                    prsid = int(input("This id does not exist. Please try again: "))
                prsids.append(prsid)
            year = int(input("Insert year: "))
            month = int(input("Insert month: "))
            day = int(input("Insert day: "))
            hour = int(input("Insert hour: "))
            minutes = int(input("Insert minutes: "))
            date = datetime.date(year, month, day)
            time = datetime.time(hour, minutes)
            descr = input("Insert a description: ")
            if self.__activity_service.check_datetime(date, time) is False:
                self.__activity_service.add_activity(prsids, date, time, descr)
            else:
                print("There is another activity which has the same starting point. Activities must not overlap")
        except PersonError as se:
            print("caught StoreError: ", se)
        except ValueError:
            print("Wrong arguments were introduced")

    def __ui_remove_activity(self):
        id = int(input("Insert the id of the activity you want to remove: "))
        self.__activity_service.delete_activity(id)


    def __ui_update_activity(self):
        try:
            id = int(input("Introduce the id of the activity you want to update "))
            prsids = []
            nrprs = int(input("Insert the number of people who take part in activity: "))
            for x in range(0,nrprs):
                prsid = int(input("Type person id: "))
                while self.__person_service.exist_id(prsid) is False:
                    prsid = int(input("This id does not exist. Please try again: "))
            year = int(input("Insert new year: "))
            month = int(input("Insert new month: "))
            day = int(input("Insert new day: "))
            hour = int(input("Insert new hour: "))
            minutes = int(input("Insert new minutes: "))
            date = datetime.date(year, month, day)
            time = datetime.time(hour, minutes)
            descr = input("Insert a new description: ")
            self.__activity_service.update_activity_by_id(id, prsids, date, time, descr)
        except PersonError as se:
            print("caught StoreError: ", se)
        except ValueError:
            print("Wrong arguments were introduced")


    def __ui_search_activity(self):
        option = int(input("Please choose a searching criteria: 1. By date/time, 2. By description "))
        if option == 1:
            year = int(input("Insert new year: "))
            month = int(input("Insert new month: "))
            day = int(input("Insert new day: "))
            date = datetime.date(year, month, day)
            list = self.__activity_service.search_by_date(date)
            for item in list:
                print(item)
        elif option == 2:
            d = input("Introduce the description ")
            list = self.__activity_service.search_by_descr(d.lower())
            for item in list:
                print(item)
        else:
            print("Please choose an existent criteria ")
#______________________________The UI functions for people__________________________

    def __ui_print_people(self):
        ppl = self.__person_service.get_all_people()
        for item in ppl:
            print(item)

    def __ui_reomove_person(self):
        id = int(input("Introduce the id of the person "))
        if self.__person_service.exist_id(id):
            self.__person_service.delete_person(id)
        else:
            print("Nu exista id-ul")


    def __ui_update_person(self):
        try:
            id = int(input("Introduce the id of the person you want to update "))
            name = input("Introduce the name: ")
            pn = input("Introduce a phone number ")
            address = input("Introduce an address ")
            self.__person_service.update_person_by_id(id, name, pn, address)
        except PersonError as se:
            print("caught StoreError: ", se)
        except ValueError:
            print("Wrong arguments were introduced ")

    def __ui_add_people(self):
        try:
            id = int(input("Introduce an id: "))
            name = input("Introduce the name: ")
            pn = input("Introduce a phone number: ")
            address = input("Introduce an address: ")
            self.__person_service.add_person(id, name, pn, address)
        except PersonError as se:
            print("caught StoreError: ", se)
        except ValueError:
            print("Wrong arguments were introduced ")

    def __ui_search_people(self):
        option = int(input("Please choose a searching criteria: 1. By name, 2. By phone number "))
        if option == 1:
            name = input("Introduce the name: ")
            list = self.__person_service.search_by_name(name.lower())
            for item in list:
                print(item)
        elif option == 2:
            pn = input("Introduce the phone number: ")
            list = self.__person_service.search_by_pn(pn)
            for item in list:
                print(item)
        else:
            print("Wrong criteria")

#___________________________The UI functions for statistics______________________________

    def __ui_activities_with_a_given_person(self):
        id = int(input("Introduce the id of the person you are interested in: "))
        if self.__person_service.exist_id(id):
            list = self.__stats.act_for_prs(id)
            for item in list:
                print(item)
        else:
            print("The ID does not exist")
    def __ui_activities_on_a_day(self):
        try:
            year = int(input("Insert year: "))
            month = int(input("Insert month: "))
            day = int(input("Insert day: "))
            dayt = datetime.date(year, month, day)
            list = self.__stats.act_for_day(dayt)
            if len(list) == 0:
                print("There are no activities scheduled for this day")
            else:
                for item in list:
                    print(item)
                    #print (item.id, item.prsids, item.time, item.description)
        except ValueError:
            print("Wrong Arguments were passed")
    def __ui_list_people(self):
        list = self.__stats.list_ppl()
        for item in list:
            print(item)

    def __ui_busiest_days(self):
        list = self.__stats.busiest_days()
        for item in list:
            print(item.day, "number of activities: ", item.no_of_act)

    def __ui_undo(self):
        UndoManager.undo()

    def __ui_redo(self):
        RedoManager.redo()