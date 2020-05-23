import threading
import queue
import requests

threads = 50
target_url = "http://testphp.vulnweb.com"
wordlist_file = "svndigger/all.txt"
resume = None
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/81.0.4044.138 Safari/537.36"


def build_wordlist(wordlist_file):
    fd = open(wordlist_file, 'r')
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = queue.Queue()

    for word in raw_words:
        word = word.rstrip()

        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: %s" % word)
        else:
            words.put(word)

    return words


def dir_buster(word_queue, extensions=None, target_status_code=None):

    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # Check if the word is a file or a directory
        if "." in attempt:
            attempt = "/" + attempt
        else:
            attempt = "/" + attempt + "/"

        attempt_list.append(attempt)

        # Check if extension brute force should be included
        if extensions:
            for extension in extensions:
                attempt_list.append("%s%s" % (attempt, extension))

        for brute in attempt_list:
            url = "%s%s" % (target_url, brute)
            try:
                response = requests.get(url)
                if target_status_code:
                    if response.status_code in target_status_code:
                        print("[%d] => %s" % (response.status_code, url))
                else:
                    print("[%d] => %s" % (response.status_code, url))

            except requests.RequestException as err:
                if hasattr(err, 'code') and err.code != 404:
                    print("*** [%d] => %s", (err.code, url))
                pass


word_queue = build_wordlist(wordlist_file)
extensions = [".php", ".bak", ".orig", ".inc"]
target_status_code = [200]
for i in range(threads):
    print("Spawning thread: %d" % i)
    t = threading.Thread(target=dir_buster,args=(word_queue, extensions, target_status_code,))
    t.start()
