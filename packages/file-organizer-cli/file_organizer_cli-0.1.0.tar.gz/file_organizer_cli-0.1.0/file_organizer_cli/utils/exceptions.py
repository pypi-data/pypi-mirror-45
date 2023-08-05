from file_organizer_cli.constants import FileTypes


class FileError(BaseException):
    def __init__(self, file_name, file_type):
        super().__init__('{} is not a valid {} file.'.format(file_name, file_type))


class JSONFileError(FileError):
    def __init__(self, file_name):
        super().__init__(file_name, FileTypes.JSON.value)


class WrongFormatError(BaseException):
    def __init__(self, detail: str = ''):
        super().__init__('Your content has the wrong format.{}'.format(' {}'.format(detail)))

