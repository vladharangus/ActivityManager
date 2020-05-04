import pickle

from Domain.validators import PersonValidator, ActivityValidator
from Repository.repository import repository


class PersonPickleRepo(repository):
    def __init__(self, file = "people.pickle"):
        repository.__init__(self, PersonValidator)
        self.__file_name = file
        self.__load_file()

    def save(self, person):
        repository.save(self, person)
        self.__store_file()

    def delete_by_id(self,id):
        repository.delete_by_id(self, id)
        self.__store_file()

    def find_all(self):
        return repository.find_all(self)


    def find_by_id(self, id):
        return repository.find_by_id(self, id)

    def update(self, new_entity):
        repository.update(self, new_entity)
        self.__store_file()

    def current_id(self):
        return repository.current_id(self)

    def __store_file(self):
        f = open(self.__file_name, 'wb')
        pickle.dump(self._entities, f)
        f.close()

    def __load_file(self):
        f = open(self.__file_name, 'rb')
        try:
            self._entities = pickle.load(f)
            for en in self._entities:
                repository.save(self, en)
        except EOFError:
            self._entities = []
        except Exception as er:
            print("")
        finally:
            f.close()

class ActivityPickleRepo(repository):
    def __init__(self, file = "activity.pickle"):
        repository.__init__(self, ActivityValidator)
        self.__file_name = file
        self.__load_file()

    def save(self, activity):
        repository.save(self, activity)
        self.__store_file()

    def delete_by_id(self,id):
        repository.delete_by_id(self, id)
        self.__store_file()

    def find_all(self):
        return repository.find_all(self)


    def find_by_id(self, id):
        return repository.find_by_id(self, id)

    def update(self, new_entity):
        repository.update(self, new_entity)
        self.__store_file()

    def current_id(self):
        return repository.current_id(self)

    def __store_file(self):
        f = open(self.__file_name, 'wb')
        pickle.dump(self._entities, f)
        f.close()

    def __load_file(self):
        f = open(self.__file_name, 'rb')
        try:
            self._entities = pickle.load(f)
            for en in self._entities:
                repository.save(self, en)
        except EOFError:
            self._entities = []
        except Exception as er:
            print("")
        finally:
            f.close()


