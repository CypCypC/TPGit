import json
import time

import numpy as np


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        self.size = size or np.random.randint(300, 3_000)
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": int(self.size),
            "a": self.a.tolist(),
            "b": self.b.tolist(),
            "x": self.x.tolist(),
            "time": float(self.time),
        }
        return json.dumps(data)

    @staticmethod
    def from_json(text: str) -> "Task":
        data = json.loads(text)

        t = Task(identifier=int(data["identifier"]), size=int(data["size"]))
        t.a = np.array(data["a"], dtype=float)
        t.b = np.array(data["b"], dtype=float)
        t.x = np.array(data["x"], dtype=float)
        t.time = float(data["time"])
        return t

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return False
        return (
            self.identifier == other.identifier
            and self.size == other.size
            and np.array_equal(self.a, other.a)
            and np.array_equal(self.b, other.b)
            and np.array_equal(self.x, other.x)
            and self.time == other.time
        )
