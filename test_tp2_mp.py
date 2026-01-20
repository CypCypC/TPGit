import unittest
import multiprocessing as mp

from task import Task


def worker(q_in, q_out):
    while True:
        t = q_in.get()
        if t is None:
            break
        t.work()
        q_out.put((t.identifier, t.size, t.time))


class TestTP2MP(unittest.TestCase):
    def test_collects_all_results(self):
        ctx = mp.get_context("spawn")
        q_in = ctx.Queue()
        q_out = ctx.Queue()

        p = ctx.Process(target=worker, args=(q_in, q_out))
        p.start()

        n = 5
        for i in range(n):
            q_in.put(Task(identifier=i, size=80))
        q_in.put(None)

        got = [q_out.get() for _ in range(n)]
        p.join()

        ids = sorted(x[0] for x in got)
        self.assertEqual(ids, list(range(n)))


if __name__ == "__main__":
    unittest.main()
