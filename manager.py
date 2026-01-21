from __future__ import annotations

import argparse
import queue
from multiprocessing.managers import BaseManager

_task_queue: "queue.Queue" = queue.Queue()
_result_queue: "queue.Queue" = queue.Queue()


def get_task_queue():
    return _task_queue


def get_result_queue():
    return _result_queue


class QueueManager(BaseManager):
    pass


QueueManager.register("task_queue", callable=get_task_queue)
QueueManager.register("result_queue", callable=get_result_queue)


class QueueClient:
    """
    Client utilisé par proxy.py:
    self.task_queue.get() pour récupérer une Task
    self.result_queue.put(task) pour renvoyer une Task
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 50000,
        authkey: bytes = b"secret",
    ):
        self._m = QueueManager(address=(host, port), authkey=authkey)
        self._m.connect()
        self.task_queue = self._m.task_queue()
        self.result_queue = self._m.result_queue()


def serve(
    host: str = "127.0.0.1", port: int = 50000, authkey: bytes = b"secret"
) -> None:
    """
    Lance le serveur de queues.
        python3 manager.py
    """
    m = QueueManager(address=(host, port), authkey=authkey)
    server = m.get_server()
    print(f"[manager] serving on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=50000)
    parser.add_argument("--authkey", default="secret")
    args = parser.parse_args()
    serve(args.host, args.port, args.authkey.encode())
