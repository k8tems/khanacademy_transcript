import re
import json
import requests
from pprint import pprint


def serialize_content_items(content_items):
    result = []
    for ci in content_items:
        # practice nodes do not have videos
        if 'youtubeId' not in ci:
            continue
        result.append((ci['title'], ci['description'], ci['youtubeId']))
    return result


def serialize_tutorials(tutorials):
    videos = []
    for t in tutorials:
        videos.append({
            'title': t['title'],
            'videos': serialize_content_items(t['contentItems'])})
    return videos


class ReactComponentNotFound(RuntimeError):
    pass


def parse_tutorials(page_source):
    regex = re.search('ReactComponent\((.+,\s*"loggedIn".+?})', page_source)
    if not regex:
        raise ReactComponentNotFound(page_source)
    component = json.loads(regex.group(1))
    return component['componentProps']['curation']['tabs'][0]['modules'][0]['tutorials']


def get_tutorials(url):
    resp = requests.get(url)
    return parse_tutorials(resp.text)


def parse():
    url = 'https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces'
    tutorials = get_tutorials(url)
    videos = serialize_tutorials(tutorials)
    pprint(videos)


def main():
    parse()


if __name__ == '__main__':
    main()
