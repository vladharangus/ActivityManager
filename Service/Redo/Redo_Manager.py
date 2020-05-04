from dataclasses import dataclass

from Service.Redo.Redo_Handlers import RedoHandler


@dataclass
class RedoOperation:
    __source_object : object
    __handler : RedoHandler
    __args : tuple

    @property
    def source_object(self):
        return self.__source_object

    @property
    def handler(self):
        return self.__handler

    @property
    def args(self):
        return self.__args

class RedoManager:
    __redo_operations = []

    @staticmethod
    def register_operation(source_object, handler, *args):
        RedoManager.__redo_operations.append(RedoOperation(source_object, handler, args))

    @staticmethod
    def redo():
        if len(RedoManager.__redo_operations) != 0:
            redo_operation = RedoManager.__redo_operations.pop()
            redo_operation.handler(redo_operation.source_object, *redo_operation.args)
        else:
            print("Nothing to redo")