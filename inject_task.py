from manager import QueueClient
from task import Task

c = QueueClient()
c.task_queue.put(Task(identifier=1, size=50))
print("Injected one task")
