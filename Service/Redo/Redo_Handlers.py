from enum import Enum


def add_activity_handler_redo(activity_service, activity_id):
    activity_service.delete_activity(activity_id)

def add_person_handler_redo(person_service, person_id):
    person_service.delete_person(person_id)

def update_person_handler_redo(person_service, person_id, person_name, person_phone, person_address):
    person_service.update_person_by_id(person_id, person_name, person_phone, person_address)

def update_activity_handler_redo(activity_service, id, prsids, date, time, descr):
    activity_service.update_activity_by_id(id, prsids, date,time, descr)

def delete_activity_handler_redo(activity_service, prsids, date, time, desc):
    activity_service.add_activity(prsids, date, time, desc)

def delete_person_handler_redo(person_service, acts, id, name, phone, address):
    person_service.add_person(id, name, phone, address)
    for item in acts:
        item.prsids.append(id)


class RedoHandler(Enum):
    ADD_ACTIVITY = add_activity_handler_redo
    ADD_PERSON = add_person_handler_redo
    UPDATE_PERSON = update_person_handler_redo
    UPDATE_ACTIVITY = update_activity_handler_redo
    DELETE_ACTIVITY = delete_activity_handler_redo
    DELETE_PERSON = delete_person_handler_redo