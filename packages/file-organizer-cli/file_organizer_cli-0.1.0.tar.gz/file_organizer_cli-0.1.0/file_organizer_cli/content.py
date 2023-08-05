import typing
import re


class DjangoContent:
    """
    Content storage for django model entity
    """
    model = None
    pk = None
    fields = None

    def __init__(self, model: str = None, pk: int = None, fields: typing.List = list):
        self.model = model
        self.pk = pk
        self.fields = fields

    def remove_fields(self, fieldset):
        for field in fieldset:
            del self.fields[field]

    def set_field(self, field, value):
        self.fields[field] = value

    def __str__(self):
        return '<DjangoContent model="{}" pk="{}">'.format(
            self.model if self.model else 'None',
            self.pk if self.pk else 'None'
        )

    def __dict__(self):
        """
        Serialization method
        :return:
        """
        return {
            'model': self.model or None,
            'pk': self.pk or None,
            'fields': self.fields or {}
        }


class DjangoContentList:
    """
    Content Manager for django model objs
    """
    objects = []
    objects_dict = {}
    fields_set = set()
    __iterator = 0

    def as_dict(self):
        """
        :return: content as dict
        """
        return self.objects_dict

    def as_list(self):
        """
        :return: content as list
        """
        return self.objects

    @property
    def length(self):
        """
        :return: num elem
        """
        return len(self.objects) - 1

    def exclude(self, app: str = None, model: str = None, pk: int = -1):
        """
        content exclusion filter
        :param app: app label
        :param model: model label
        :param pk: entities primary key
        :return: filtered list
        """
        if pk == -1:
            if model:
                new_list = [i for i in self.objects if i.model != model]
                new_dict = {i: v for i, v in self.objects_dict.items() if i != model}
                self.objects_dict = {}
                self.objects = []
                self.objects = new_list
                self.objects_dict = new_dict.copy()
                return self
            elif app:
                new_list = [i for i in self.objects if i.model.find(app) == -1]
                new_dict = {i: v for i, v in self.objects_dict.items() if i.find(app) == -1}
                self.objects_dict = {}
                self.objects = []
                self.objects = new_list
                self.objects_dict = new_dict.copy()
                return self
        else:
            regex = re.findall(r'pk="(?P<pk>[0-9]*)"', pk)
            if regex:
                for real_pk in regex:
                    new_list = [i for i in self.objects if i.pk != int(real_pk)]
                    new_dict = {i: v for i, v in self.objects_dict.items() for obj in v if obj.pk != int(real_pk)}
                    self.objects_dict = {}
                    self.objects = []
                    self.objects = new_list
                    self.objects_dict = new_dict.copy()
                return self

    def filter(self, app: str = None, model: str = None, pk: int = -1):
        """
        content filter
        :param app: app label
        :param model: model label
        :param pk: entities primary key
        :return: filtered list
        """
        if pk == -1:
            new_list = [i for i in self.objects if i.model == model]
            new_dict = {i: v for i, v in self.objects_dict.items() if i == model}
            self.objects_dict = {}
            self.objects = []
            self.objects = new_list
            self.objects_dict = new_dict.copy()
            del new_dict, new_list

    def reduce_model_fields(self, model, fieldset):
        elems = []
        for obj in self.objects:
            if obj.model == model:
                elem = self.objects.pop(self.objects.index(obj))
                elem.remove_fields(fieldset)
                elems.append(elem)
        self.objects.extend(elems)
        self.objects_dict[model] = elems

    def append(self, obj) -> None:
        """
        :param obj:
        :return:
        """
        self.objects.append(obj)
        try:
            self.objects_dict[obj.model].append(obj)
        except KeyError:
            self.objects_dict[obj.model] = [obj]

        self.fields_set.add(field for field in obj.fields.keys())

    def __str__(self):
        return '<DjangoContentList count={} models={} fields={}>'.format(
            self.length,
            self.objects_dict.keys(),
            self.fields_set
        )

    def __len__(self):
        return self.length

    def __iter__(self):
        """

        :return:
        """
        self.__iterator = 0
        return self

    def __next__(self):
        """

        :return:
        """
        if self.__iterator < self.length:
            self.__iterator += 1
            return self.objects[self.__iterator]
        else:
            raise StopIteration
