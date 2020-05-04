import datetime
class PersonError(Exception):
    pass


class ValidatorError(PersonError):
    pass


class ActivityValidator:
    @staticmethod
    def validate(activity):
        if type(activity.id) is not int:
            raise ValidatorError("activity id should be integer")
        if type(activity.prsids) is not list:
            raise ValidatorError("people's ids should be a list")
        if type(activity.date) is not datetime.date:
            raise ValidatorError("activity date should be a date")
        if type(activity.time) is not datetime.time:
            raise ValidatorError("activity time should be a valid hour")
        if type(activity.description) is not str:
            raise ValidatorError("activity description should be a string")


class PersonValidator:
    @staticmethod
    def validate(person):
        if type(person.id) is not int:
            raise ValidatorError("person id should be integer")
        if type(person.name) is not str:
            raise ValidatorError("person name should be a string")
        if len(person.phone_no) != 10 or (len(person.phone_no) >= 2 and person.phone_no[0] != "0" and person.phone_no[1] != "7"):
            raise ValidatorError("person number is not a valid one")
        for d in person.phone_no:
            if d not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                raise ValidatorError("person number is not a valid one")
        if type(person.address) is not str:
            raise ValidatorError("person address should be astring")
