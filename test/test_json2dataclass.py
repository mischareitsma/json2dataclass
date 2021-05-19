import pathlib
import unittest
from json2dataclass import generate_code_from_json_string

JSON_PATH = pathlib.Path(__file__).parent / 'json'
PY_PATH = pathlib.Path(__file__).parent / 'py'

NUMBER_OF_TEST_JSONS = 5


class TestJson2DataClass(unittest.TestCase):

    def test_generated_python_code(self):

        self.maxDiff = None

        for i in range(NUMBER_OF_TEST_JSONS):
            with self.subTest(i=i):
                json_content = read_json(f'test{i+1}.json')
                py_content = read_py(f'test{i+1}.py')

                gen_py = generate_code_from_json_string(json_content)

                self.assertEqual(py_content, gen_py)


def read_json(json_name: str) -> str:
    with open(JSON_PATH / json_name, 'r') as f:
        return f.read()


def read_py(py_name: str) -> str:
    with open(PY_PATH / py_name, 'r') as f:
        return f.read()
