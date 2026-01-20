from __future__ import annotations

import multiprocessing as mp
from dataclasses import dataclass

from task import Task


@dataclass
class TaskResult:
    identifier: int
    size: int
    elapsed: float


def minion_loop(task_queue: mp.Queue, result_queue: mp.Queue) -> None:
    while True:
        task = task_queue.get()
        if task is None:
            break

        task.work()
        result_queue.put(TaskResult(task.identifier, task.size, task.time))


def main(n_tasks: int = 20, n_minions: int = 8) -> None:
    ctx = mp.get_context("spawn")

    task_queue: mp.Queue = ctx.Queue()
    result_queue: mp.Queue = ctx.Queue()

    minions: list[mp.Process] = []
    for _ in range(n_minions):
        p = ctx.Process(target=minion_loop, args=(task_queue, result_queue))
        p.start()
        minions.append(p)

    for i in range(n_tasks):
        t = Task(identifier=i, size=300)
        task_queue.put(t)

    for _ in range(n_minions):
        task_queue.put(None)

    results: list[TaskResult] = []
    for _ in range(n_tasks):
        results.append(result_queue.get())

    for p in minions:
        p.join()

    results.sort(key=lambda r: r.identifier)
    total = sum(r.elapsed for r in results)
    print("Results:")
    for r in results:
        print(f" - id={r.identifier:02d} size={r.size} time={r.elapsed:.4f}s")
    print(f"Total elapsed (sum of tasks): {total:.4f}s")


if __name__ == "__main__":
    main()
