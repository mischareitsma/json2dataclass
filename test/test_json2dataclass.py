import pathlib
import unittest
from json2dataclass import generate_dataclasses_from_json

JSON_PATH = pathlib.Path(__file__).parent / 'json'
PY_PATH = pathlib.Path(__file__).parent / 'py'


class TestJson2DataClass(unittest.TestCase):

    def test_test1_json(self):
        json_content=read_json('test1.json')
        py_content = read_py('test1.py')

        gen_py = generate_code_from_json(json_content)

        print(gen_py)

        self.assertEqual(py_content, gen_py)


def read_json(json_name: str) -> str:
    with open(JSON_PATH / json_name, 'r') as f:
        return f.read()


def read_py(py_name: str) -> str:
    with open(PY_PATH / py_name, 'r') as f:
        return f.read()
