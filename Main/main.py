import pickle
import traceback
import datetime
import unittest


from Domain.validators import ActivityValidator, PersonValidator
from Repository.Pickle import ActivityPickleRepo, PersonPickleRepo
from Repository.repository import repository, Statistics, prs_file_repo, acts_file_repo
from Service.activity_service import ActivityService
from Service.person_service import PersonService
from UI.Console import Console
try:
    file = open("settings.properties.txt", "r")
    line = file.readline().strip().split("=")
    okay = 0
    if line[1].strip() == "inmemory":
        person_repository = repository(PersonValidator)
        activity_repository = repository(ActivityValidator)
        okay = 1
    elif line[1].strip() == "textfiles":
        #okay = 1
        line1 = file.readline().strip().split("=")
        line1[1] = line1[1].strip()[1:len(line1[1]) - 2]
        person_repository = prs_file_repo(line1[1].strip(), PersonValidator)
        line2 = file.readline().strip().split("=")
        line2[1] = line2[1].strip()[1:len(line2[1]) - 2]
        activity_repository = acts_file_repo(line2[1].strip(), ActivityValidator)
    else:
        #okay = 1
        line1 = file.readline().strip().split("=")
        line1[1] = line1[1].strip()[1:len(line1[1]) - 2]
        person_repository = PersonPickleRepo(line1[1].strip())
        line2 = file.readline().strip().split("=")
        line2[1] = line2[1].strip()[1:len(line2[1]) - 2]
        activity_repository = ActivityPickleRepo(line2[1].strip())
    #activity_repository = acts_file_repo("Activities.txt", ActivityValidator)
    activity_service = ActivityService(activity_repository)
    person_service = PersonService(person_repository, activity_repository)
    statistics = Statistics(activity_repository, person_repository, activity_service, person_service)
    console = Console(activity_service, person_service, statistics)
    if okay == 1 :
        console.generate_entities()

    console.run_menu()
except Exception as ex:
    print("caught exception in main; printing stacktrace")
    traceback.print_exc()