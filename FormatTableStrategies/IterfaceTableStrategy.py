from abc import ABC, abstractmethod


class InterfaceTableFormatStrategy(ABC):

    @abstractmethod
    def formatLine(self, table_line):
        pass
