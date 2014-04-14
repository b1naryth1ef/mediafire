from mediafire import MediaFireAPI
import os, time
from multiprocessing import *

def get_api():
    api = MediaFireAPI()
    api.authenticate(os.getenv("MEDIAFIRE_EMAIL"), os.getenv("MEDIAFIRE_PASS"),
        os.getenv("MEDIAFIRE_APPID"), os.getenv("MEDIAFIRE_APPSECRET"))
    return api

class Consumer(object):
    def __init__(self, id, q, folder):
        self.id = id
        self.q = q
        self.api = get_api()
        self.folder = folder

    def run(self):
        while True:
            data = self.q.get()
            if not data:
                return
            self.consume(data)

    def consume(self, data):
        print "[%s] Backing up file @ `%s`" % (self.id, data)
        self.api.upload_file(open(data, "r"), {
            "uploadkey": self.folder,
            "path": data
        })

class Producer(object):
    def __init__(self, q):
        self.q = q

    def run(self):
        for item in self.produce():
            if not item: return
            self.q.put(item)

    def produce(self):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                yield os.path.join(root, name)

api = get_api()
folder = api.create_folder("backup-%s" % time.time())

q = Queue(2048)
PRODUCER = Producer(q)
CONSUMERS = [Consumer(i, q, folder) for i in range(10)]
CONSUMER_PROCS = [Process(target=c.run) for c in CONSUMERS]

# Start
[p.start() for p in CONSUMER_PROCS]

# Run producer
PRODUCER.run()

# Close consumers
[q.put(None) for i in range(10)]

# Join consumers
[p.join() for i in CONSUMER_PROCS]
