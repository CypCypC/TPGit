import unittest

import numpy.testing as npt

from task import Task


class TestTask(unittest.TestCase):
    def test_ax_equals_b(self):
        t = Task(size=50)  # petit pour que le test soit rapide
        t.work()

        # Vérifie que A @ x ~= b
        npt.assert_allclose(t.a @ t.x, t.b)


if __name__ == "__main__":
    unittest.main()
