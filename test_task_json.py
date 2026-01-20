import unittest

from task import Task


class TestTaskJson(unittest.TestCase):
    def test_json_roundtrip(self):
        a = Task(identifier=123, size=20)
        txt = a.to_json()
        b = Task.from_json(txt)
        self.assertTrue(a == b)


if __name__ == "__main__":
    unittest.main()
