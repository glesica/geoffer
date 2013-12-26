import json
from geoffer import Node, nodestr, relstr


class DictParser(object):
    """
    Parser to convert a dictionary or list of dictionaries to Geoff format
    nodes.

    >>> d1 = {'name': 'alice', 'type': 'employee', 'age': 23}
    >>> d2 = {'name': 'bob', 'type': 'employee', 'age': 48}
    >>> f1 = DictParser(name_key='name', label_keys=['type'], prop_keys=['name', 'age'])
    >>> f1(d1)
    '(alice:Employee {"age": 23, "name": "alice"})'
    >>> f2 = DictParser(name_key='name', extra_labels=['person'], unique_key='name')
    >>> f2(d1)
    '(alice:Person!name {"name": "alice"})'
    >>> f3 = DictParser(name_suffix='person1')
    >>> f3(d1)
    '(person1)'
    """
    def __init__(self, name_key=None, name_suffix='', label_keys=[], extra_labels=[],
                 unique_key=None, prop_keys=[]):
        self.name_key = name_key
        self.name_suffix = name_suffix
        self.label_keys = label_keys
        self.extra_labels = [s.title() for s in extra_labels]
        self.unique_key = unique_key

        if unique_key and unique_key not in prop_keys:
            self.prop_keys = prop_keys + [unique_key]
        else:
            self.prop_keys = prop_keys

    def __call__(self, data):
        if type(data) is dict:
            data_list = [data]
        else:
            data_list = data

        return '\n'.join([self.__parse(d) for d in data_list])


    def __parse(self, data_dict):
        try:
            name = data_dict[self.name_key] if self.name_key else self.name_suffix
        except KeyError, e:
            raise Exception("name_key '{}' not in data_dict".format(e))

        try:
            labels = [data_dict[k].title() for k in self.label_keys] + self.extra_labels
        except KeyError, e:
            raise Exception("label_keys element '{}' not in data_dict".format(e))

        try:
            props = {k: data_dict[k] for k in self.prop_keys}
        except KeyError, e:
            raise Exception("prop_keys element '{}' not in data_dict".format(e))

        node = Node(name, labels, props)

        return nodestr(node, self.unique_key)
