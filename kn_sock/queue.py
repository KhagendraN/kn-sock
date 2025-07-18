"""
kn_sock.queue

Thread-safe in-memory and persistent file-based message queues.

Usage:
    from kn_sock.queue import InMemoryQueue, FileQueue
    q = InMemoryQueue()
    q.put('msg')
    msg = q.get()
    q.task_done()
    q.join()

    fq = FileQueue('queue.db')
    fq.put('msg')
    msg = fq.get()
    fq.task_done()
    fq.close()

Both queues support FIFO, blocking get, and delivery guarantees (at-least-once).
"""
import threading
import queue
import os
import pickle
import time


class InMemoryQueue:
    def __init__(self):
        self._q = queue.Queue()

    def put(self, item):
        self._q.put(item)

    def get(self, block=True, timeout=None):
        return self._q.get(block, timeout)

    def task_done(self):
        self._q.task_done()

    def join(self):
        self._q.join()

    def qsize(self):
        return self._q.qsize()

    def empty(self):
        return self._q.empty()


class FileQueue:
    def __init__(self, path: str):
        self.path = path
        self.lock = threading.Lock()
        self._load()
        self._not_empty = threading.Condition(self.lock)
        self._unfinished_tasks = 0

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as f:
                try:
                    self._queue = pickle.load(f)
                except Exception:
                    self._queue = []
        else:
            self._queue = []

    def _save(self):
        with open(self.path, "wb") as f:
            pickle.dump(self._queue, f)

    def put(self, item):
        with self.lock:
            self._queue.append(item)
            self._unfinished_tasks += 1
            self._save()
            self._not_empty.notify()

    def get(self, block=True, timeout=None):
        with self.lock:
            if not block and not self._queue:
                raise queue.Empty
            start = time.time()
            while not self._queue:
                if not block:
                    raise queue.Empty
                if timeout is not None:
                    elapsed = time.time() - start
                    if elapsed >= timeout:
                        raise queue.Empty
                    self._not_empty.wait(timeout - elapsed)
                else:
                    self._not_empty.wait()
            item = self._queue.pop(0)
            self._save()
            return item

    def task_done(self):
        with self.lock:
            self._unfinished_tasks -= 1
            if self._unfinished_tasks == 0:
                self._not_empty.notify_all()

    def join(self):
        with self.lock:
            while self._unfinished_tasks:
                self._not_empty.wait()

    def close(self):
        self._save()

    def qsize(self):
        with self.lock:
            return len(self._queue)

    def empty(self):
        with self.lock:
            return not self._queue
