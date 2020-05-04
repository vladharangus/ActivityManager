from dataclasses import dataclass

from Service.handlers import UndoHandler


@dataclass
class UndoOperation:
    __source_object : object
    __handler : UndoHandler
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

class UndoManager:
    __undo_operations = []

    @staticmethod
    def clear_op():
        UndoManager.__undo_operations.clear()

    @staticmethod
    def register_operation(source_object, handler, *args):
        UndoManager.__undo_operations.append(UndoOperation(source_object, handler, args))

    @staticmethod
    def undo():
        if len(UndoManager.__undo_operations) == 0:
            raise ValueError("Nothing to undo")
        undo_operation = UndoManager.__undo_operations.pop()
        undo_operation.handler(undo_operation.source_object, *undo_operation.args)





