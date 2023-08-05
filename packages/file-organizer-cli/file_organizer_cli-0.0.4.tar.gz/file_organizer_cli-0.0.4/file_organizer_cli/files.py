import abc
import json

from file_organizer_cli.constants import FileTypes
from file_organizer_cli.utils.exceptions import WrongFormatError, JSONFileError


class FileProcessor(abc.ABC):
    content = None

    def __init__(self, file_name: str = None, target_name: str = None) -> None:
        self.file_name = file_name
        self.target_name = target_name

    def read(self) -> object:
        """
        opens a file of type n
        :return: content of file
        """
        raise NotImplementedError

    def write(self, file_name: str = None):
        """
        writes a file of type n
        """
        raise NotImplementedError


class JsonFileProcessor(FileProcessor):
    file_type = FileTypes.JSON

    def read(self):
        try:
            self.content = json.loads(open(self.file_name).read())
        except json.JSONDecodeError:
            raise JSONFileError(self.file_name)
        return self.content

    def write(self, target_name: str = None):
        if target_name:
            self.target_name = target_name
        try:
            json.dump(self.content, open(self.target_name, 'w'), default=lambda x: x.__dict__())
        except TypeError:
            raise WrongFormatError(detail=self.file_type.verbose_name)
