import enum
import json
import pathlib

from numbers import Number
from typing import Any, Union

"""JSON Classes

This section contains all the classes that deal with the JSON objects.
"""
class JSONType(enum.Enum):
    """Valid JSON Types.
    """

    STRING = 1
    NUMBER = 2
    OBJECT = 3
    ARRAY = 4
    BOOLEAN = 5
    NULL = 6


class JSONAttribute:
    """Class representing a JSON attribute.
    """

    def __init__(self, name:str, json_type: JSONType):
        self.name: str = name
        self.type: JSONType = json_type
        # name: Attribute, name="content" special case for ARRAY
        self.children: dict[str, JSONAttribute] = {}
    
    def __repr__(self):
        s = f'"{self.name}" : '
        if self.type is JSONType.OBJECT:
            s += '{\n'
            for child in self.children.values():
                s += child.__repr__()
            s += '}'
        elif self.type is JSONType.ARRAY:
            s += '[\n'
            s += self.children['content'].__repr__()
            s += ']'
        else:
            s += str(self.type)
        s += ',\n'
        return s


# TODO: These are optional, using JSONType vs using object type is a choice
# at this point. Went with using self.type for now. Code generation should
# ignore children if type not on [OBJECT, ARRAY]
# class JSONObject(JSONAttribute):

#     def __init__(self, name: str, json_type: JSONType):
#         super().__init__(name, json_type)
#         self.children: list[JSONAttribute]


# class JSONArray(JSONAttribute):

#     def __init__(self, name: str, json_type: JSONType):
#         super().__init__(name, json_type)
#         self.child: JSONAttribute


class JSONParser:

    class JSONObjectInJSONArrayNotSupported(Exception):
        pass

    def __init__(self, in_json: str, is_file: bool = False):
        """Initialize the JSON parser.

        :param in_json: A JSON string or a file path containing a JSON.
        :param is_file: True if `in_json` is a file path, False if
            `in_json` is a JSON string.
        """

        self.json: str = ''
        # TODO: JSON Attributes could have an `has_parents` flag? Plus a
        # reference to its direct parent for easy traversal?
        self.root: JSONAttribute = JSONAttribute('root', JSONType.OBJECT)

        # List of all the JSON objects inside the tree.
        # TODO: Might turn into a dict when implementing, easier to track.
        # TODO: An improvement over a list would be a set?
        self.json_objects: list[JSONAttribute] = []

        # Used if the root is an array, might need some different logic in
        # that case.
        self.root_is_array: boolean = False

        if is_file:
            with open(in_json, 'r') as f:
                self.json = f.read()
        else:
            self.json = in_json

    def parse(self):
        """Parse the JSON, and generate the attribute tree, starting with
        the root attribute.
        """
        raise NotImplementedError('JSONParser.parse() is abstract')

    def get_root_attribute(self) -> JSONAttribute:
        return self.root


class JSONPythonDictParser(JSONParser):
    
    def __init__(self, in_json: str, is_file: bool = False):
        super().__init__(in_json, is_file)

        self.loaded_json: Union[list, dict] = json.loads(self.json)
        self.root_is_array = isinstance(self.loaded_json, list)

    def parse(self):
        if self.root_is_array:
            for entry in self.loaded_json:
                # At this stage, we need object, or else there is not
                # much to parse, for now simple continue, might change to
                # an error at a latest stage
                if not isinstance(entry, dict):
                    continue
                self._parse_object(self.root, entry)
        else:
            self._parse_object(self.root, self.loaded_json)
    
    def _parse_object(self, current: JSONAttribute, json_object: dict):
        for k, v in json_object.items():
            self._parse_element(current, k, v)

    def _parse_element(self, parent: JSONAttribute, name: str, value: Any):
        """Parse the current element.

        :param parent: The parent JSONAttribute.
        :param name: Name of the current attribute.
        :param value: The value of the current attribute.
        """

        attr_type: JSONType = PythonTypeTranslator.get_json_type_from_type(
            type(value))

        # If the attribute is already part of the parent, and not an object or
        # array, skip
        if name in parent.children and not attr_type is JSONType.OBJECT:
            return

        # If object, create new empty object and call parse object
        # TODO: What happens in case we encounter `null`?
        if attr_type is JSONType.OBJECT:
            parent.children[name] = JSONAttribute(name, JSONType.OBJECT)
            self._parse_object(parent.children[name], value)
        elif attr_type is JSONType.ARRAY:
            parent.children[name] = JSONAttribute(name, JSONType.ARRAY)

            # If value[0] is not an object, just populate content,
            # If value[0] is an object, loop and call _parse_object multiple
            # times.
            array_content_type = PythonTypeTranslator.get_json_type_from_type(
                type(value[0])
            )
            parent.children[name].children['content'] = \
                JSONAttribute('content', array_content_type)
            if array_content_type is JSONType.OBJECT:
                for entry in value:
                    self._parse_object(
                        parent.children[name].children['content'], entry)
        else:
            parent.children[name] = JSONAttribute(name, attr_type)


class CodeGenerator:
    
    def __init__(self):
        self.type_translator: TypeTranslator = None
        self.json_parser: JSONParser = None

    def generate_code(self) -> str:
        """Generate code.

        This abstract method is implemented by classes for
        specific languages, and returns a string representation of
        the code.

        :returns: String of code.
        """
        raise NotImplementedError('CodeGenerator.generate_code() is abstract')

    def generate_code_file(self, file_path: pathlib.Path):
        with file_path.open('w') as f:
            f.write(self.generate_code())


class PythonCodeGenerator(CodeGenerator):
    pass


class TypeTranslator:

    json2type = {}
    type2json = {}

    # TODO If this method is only used for code generation, return type should
    # be str, not a str | type. Other way around, jsontype from type could use
    # Python type as input. But this does break a nice symmetry.
    @classmethod
    def get_type_from_json_type(cls, json_type: JSONType) -> Union[str, type]:
        return cls.json2type.get(json_type, '')

    @classmethod
    def get_json_type_from_type(cls, _type: Union[str, type]) -> JSONType:
        return cls.type2json.get(type, '')

class PythonTypeTranslator(TypeTranslator):

    @classmethod
    def get_type_from_json_type(cls, json_type: JSONType) -> type:

        if json_type is JSONType.STRING:
            return str

        if json_type is JSONType.NUMBER:
            return Number

        if json_type is JSONType.OBJECT:
            # TODO: This should have an optional type that can be passed
            # to the method.
            return object

        if json_type is JSONType.ARRAY:
            return list

        if json_type is JSONType.BOOLEAN:
            return bool

        if json_type is JSONType.NULL:
            return object

        # Default to 'Any'
        return object

    @classmethod
    def get_json_type_from_type(cls, _type: Union[str, type]) -> JSONType:

        if isinstance(_type, str):
            return cls._json_type_from_string(_type)

        return cls._json_type_from_python_type(_type)

    @classmethod
    def _json_type_from_python_type(cls, _type: type) -> JSONType:
        if _type is str:
            return JSONType.STRING

        if _type in [float, int]:
            return JSONType.NUMBER

        # The object is the 'default'? Handle later? If not, insert here

        if _type is list:
            return JSONType.ARRAY

        if _type is bool:
            return JSONType.BOOLEAN

        if _type is type(None):
            return JSONType.NULL

        return JSONType.OBJECT

    @classmethod
    def _json_type_from_string(cls, _type: str) -> JSONType:
        # TODO Not implemented? Or just try to convert to python type?
        # Or make some guess on what the strings can be (type.__name__?)
        return JSONType.NULL


def generate_code_from_json(json: str) -> str:
    return json


if __name__ == "__main__":
    for json_file in ['todoist-task.json', 'test1.json', 'test2.json']:
        jp = JSONPythonDictParser(f'test/json/{json_file}', True)
        jp.parse()
        print(jp.get_root_attribute().__repr__())
        print('')
