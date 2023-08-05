from __future__ import print_function, unicode_literals

from PyInquirer import prompt, style_from_dict, Token

from .constants import FileTypes
from .content import DjangoContent, DjangoContentList
from .files import JsonFileProcessor


class ClientAction:
    def __init__(self, name=None, method=None, help_text=None, params=None):
        self.name = name
        self.method = method
        self.help_text = help_text
        self.params = params


class ClientActionMixin:
    actions = {
        'h': ClientAction(name='help', method='', help_text='Display this help', params=['h', '?']),
        's': ClientAction(name='save', method='_save_action', help_text='Save into file', params=['s', 'S', 'save']),
        'l': ClientAction(name='list', method='_list_action', help_text='List models|apps', params=['l', 'L', 'list']),
        'd': ClientAction(name='delete', method='_delete_action', help_text='Delete model|app', params=['d', 'D']),
        'q': ClientAction(name='quit', method='', help_text='Quit', params=['q', 'Q', 'exit', 'quit']),
    }
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    def get_action(self, input_param):
        for action in self.actions.values():
            if input_param in action.params:
                return action

    def call(self, action: ClientAction):
        getattr(self, action.method)()

    def _list_objects_action(self, list_only=False) -> None or list:
        """

        :return:
        """
        model = None
        if not list_only:
            choices = [{'name': str(i), 'checked': i.pk} for i in self.file_content]
            if choices:
                models = [
                    {
                        'type': 'checkbox',
                        'message': 'Select models',
                        'name': 'delete_objects',
                        'choices': choices,
                        'validate': lambda answer: 'Choose at least one object!' if len(answer) < 1 else True
                    }
                ]
                model = prompt(models, style=self.style)['delete_objects']
        else:
            for model in self.file_content:
                print(model)
        return model

    def _list_models_action(self, list_only=False) -> None or list:
        """

        :return:
        """
        model = None
        if not list_only:
            models = [
                {
                    'type': 'checkbox',
                    'message': 'Select models',
                    'name': 'delete_models',
                    'choices': [{'name': i} for i in self.models],
                    'validate': lambda answer: 'Choose at least one model!' if len(answer) < 1 else True
                }
            ]
            model = prompt(models, style=self.style)['delete_models']
        else:
            for model in self.models:
                print(model)
        return model

    def _list_apps_action(self, list_only=False) -> None or list:
        """
        :param list_only: flag to just display apps
        :return: either chosen set of apps or None
        """
        if not self.apps:
            self._update_apps()
        answers = None
        if not list_only:
            print(self.apps)
            apps = [
                {
                    'type': 'checkbox',
                    'message': 'Select apps',
                    'name': 'delete_apps',
                    'choices': [{'name': i} for i in self.apps],
                    'validate': lambda answer: 'Choose one!' if len(answer) == 0 else True
                }
            ]
            answers = prompt(apps, style=self.style)['delete_apps']
        else:
            for app in self.apps:
                print(app)
        return answers

    def _delete_app_action(self):
        """

        :return:
        """
        while True:
            app_list = self._list_apps_action()

            if app_list in [-1] or not app_list:
                break
            apps = list(self.apps)
            try:
                for app in app_list:
                    self.file_content = self.file_content.exclude(app=app)
                    del apps[apps.index(app)]

            except IndexError:
                print('Not found!')
                continue
            self.apps = set(apps)

        self._update_models()

    def _delete_model_action(self):
        """

        :return:
        """
        while True:
            model = self._list_models_action()

            if model in [-1] or not model:
                break
            models = list(self.models)
            try:
                for mod in model:
                    self.file_content = self.file_content.exclude(app=mod)
                    del models[models.index(mod)]

            except IndexError:
                print('Not found!')
                continue
            self.models = set(models)

        self._update_apps()

    def _delete_objects_action(self):
        """

        :return:
        """
        while True:
            model = self._list_objects_action()

            if model in [-1] or not model:
                break
            try:
                choices = [{'name': i, 'checked': i.pk} for i in self.file_content]
                for mod in model:
                    self.file_content = self.file_content.exclude(pk=mod)

            except IndexError:
                print('Not found!')
                continue

        self._update_apps()
        self._update_models()

    def _save_action(self):
        """

        :return:
        """
        target_file_name = input('Target file name [incl. path]: ')
        self.file_processor.content = self.file_content.as_list()
        self.file_processor.write(target_file_name)

    def _update_apps(self):
        """

        :return:
        """
        self.apps = set()
        for app in self.models:
            self.apps.add(app.split('.')[0])

    def _update_models(self):
        """

        :return:
        """
        self.models = set()
        for obj in self.file_content:
            self.models.add(obj.model)

    def _list_action(self):
        list_type = input('Which type [A = app | M = model | O = object]: ')
        if list_type in ['A', 'a', 'app', 'App']:
            self._list_apps_action(list_only=True)
        elif list_type in ['M', 'm', 'Model', 'model']:
            self._list_models_action(list_only=True)
        elif list_type in ['O', 'o', 'object', 'objects', 'Objects', 'Object']:
            self._list_objects_action(list_only=True)

    def _delete_action(self):
        delete_type = input('Which type [A = app | M = model | O = object]: ')
        if delete_type in ['A', 'a', 'app', 'App']:
            self._delete_app_action()
        elif delete_type in ['M', 'm', 'Model', 'model']:
            self._delete_model_action()
        elif delete_type in ['O', 'o', 'object', 'objects', 'Objects', 'Object']:
            self._delete_objects_action()


class Client(ClientActionMixin):
    FILE_PROCESSORS = {
        FileTypes.JSON: JsonFileProcessor
    }
    input_type = None
    file_name = None
    target_name = None
    file_processor = None
    file_content = DjangoContentList()
    raw_file_content = None
    fields = set()
    models = set()
    apps = None

    @property
    def __file_processor(self):
        """

        :return:
        """
        return self.FILE_PROCESSORS[self.input_type]

    def __process_content(self):
        """

        :return:
        """
        if isinstance(self.raw_file_content, list):
            for instance in self.raw_file_content:
                self.models.add(instance['model'])
                self.fields.add(key for key in instance['fields'].keys())
                obj = DjangoContent(model=instance['model'], pk=instance['pk'], fields=instance['fields'])
                self.file_content.append(obj)

    def __process_file(self, file_name, file_type) -> None:
        """

        :param file_name:
        :param file_type:
        :return:
        """
        self.input_type = FileTypes(file_type)
        self.file_name = file_name
        self.file_processor = self.__file_processor(file_name)
        self.raw_file_content = self.file_processor.read()
        self.__process_content()

    def read_file(self, filename: str):
        """

        :param filename:
        :return:
        """
        self.__process_file(file_name=filename, file_type='.{}'.format(filename.split('.')[-1]))

    def manage_actions(self):
        """

        :return:
        """
        chose_action = True
        while chose_action:
            action = input('Chose action ([?|h] for help): ')
            if action in ['?', 'h']:
                for action in self.actions.values():
                    print('{:<30}: {}'.format(str(action.params), action.help_text))
                continue
            elif action in ['q', 'Q', 'exit', 'quit']:
                break
            action_obj = self.get_action(action)
            if action_obj:
                self.call(action_obj)
                continue
