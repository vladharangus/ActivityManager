from enum import Enum

from Service.Redo.Redo_Handlers import RedoHandler
from Service.Redo.Redo_Manager import RedoManager


def add_activity_handler(activity_service, activity_id, prsids, date, time, descr):
    RedoManager.register_operation(activity_service, RedoHandler.DELETE_ACTIVITY, prsids, date, time, descr)
    activity_service.delete_activity(activity_id)

def add_person_handler(person_service, acts, person_id, name, phone, address):
    RedoManager.register_operation(person_service, RedoHandler.DELETE_PERSON, acts, person_id, name, phone, address)
    person_service.delete_person(person_id)

def update_person_handler(person_service, person_id, person_name, person_phone, person_address, old_name, old_ph, old_address):
    RedoManager.register_operation(person_service, RedoHandler.UPDATE_PERSON, person_id, old_name, old_ph, old_address)
    person_service.update_person_by_id(person_id, person_name, person_phone, person_address)

def update_activity_handler(activity_service, id, prsids, date, time, descr, old_prsids, old_date, old_time, old_descr):
    RedoManager.register_operation(activity_service, RedoHandler.UPDATE_ACTIVITY, id, old_prsids,old_date, old_time, old_descr)
    activity_service.update_activity_by_id(id, prsids, date,time, descr)

def delete_activity_handler(activity_service, id, prsids, date, time, desc):
    RedoManager.register_operation(activity_service, RedoHandler.ADD_ACTIVITY, id)
    activity_service.add_activity(prsids, date, time, desc)

def delete_person_handler(person_service, acts, id, name, phone, address):
    RedoManager.register_operation(person_service, RedoHandler.ADD_PERSON, id)
    person_service.add_person(id, name, phone, address)
    for item in acts:
        item.prsids.append(id)


class UndoHandler(Enum):
    ADD_ACTIVITY = add_activity_handler
    ADD_PERSON = add_person_handler
    UPDATE_PERSON = update_person_handler
    UPDATE_ACTIVITY = update_activity_handler
    DELETE_ACTIVITY = delete_activity_handler
    DELETE_PERSON = delete_person_handler



