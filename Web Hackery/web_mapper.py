"""
Converts the web app mapper to Python 3
Once you identified the open source technology used by the target web app, you can download the open source code
to your directory. The mapper will send request to the target and spider the target using the directories and file names
used in the open source code.
"""

import queue
import threading
import requests
import os

threads = 10
target = "http://www.blackhatpython.com"
directory = "joomla3.1.1"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)
web_paths = queue.Queue()

for r,d,f in os.walk('.'):
    for files in f:
        remote_path = "%s%s" %(r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            if os.name == "nt":
                remote_path = remote_path.replace("\\", "/")
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)
        try:
            response = requests.get(url)
            content = response.content
            print("[%d] => %s" % (response.status_code, url))
        except requests.exceptions.RequestException as err:
            print(err)
            pass


for i in range(threads):
    print("Spawning thread: %d" % i)
    t = threading.Thread(target=test_remote)
    t.start()
