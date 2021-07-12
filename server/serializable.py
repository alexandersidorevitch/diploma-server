import json
from copy import deepcopy
from sys import path
print(path)

class Serializable:
    def set_attributes(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __get_attributes(self, attributes):
        obj_dict: dict = deepcopy(self.__dict__)

        if hasattr(self, 'PROTECTED'):
            for attr in self.PROTECTED:
                obj_dict.pop(attr, None)

        if hasattr(self, 'DICT_TO_LIST'):
            for attr in self.DICT_TO_LIST:
                if attr in obj_dict:
                    obj_dict[attr] = list(obj_dict[attr].values())

        if attributes:
            for attr in obj_dict:
                if attr not in attributes:
                    obj_dict.pop(attr, None)

        return obj_dict

    @staticmethod
    def __default_serializer(obj):
        return obj

    def to_json_str(self, attributes=None):
        obj_dict = self.__get_attributes(attributes)
        return json.dumps(
            obj_dict,
            indent=4,
            sort_keys=True,
            default=self.__default_serializer
        )
