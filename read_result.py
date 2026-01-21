from manager import QueueClient

c = QueueClient()
t = c.result_queue.get()
print("Got result task:")
print(" - id:", t.identifier)
print(" - size:", t.size)
print(" - time:", t.time)
print(" - x length:", len(t.x))
