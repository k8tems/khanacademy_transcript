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


def extract_react_component(page_source):
    """
    Extract data used to initialize `ReactComponent` from the given page source
    This will only work if the `ReactComponent` is constructed in one line
    """
    regex = re.search('ReactComponent\((.+,\s*"loggedIn".+?})', page_source)
    if not regex:
        raise ReactComponentNotFound(page_source)
    return json.loads(regex.group(1))


def extract_tutorials(page_source):
    component = extract_react_component(page_source)
    return component['componentProps']['curation']['tabs'][0]['modules'][0]['tutorials']


def download_tutorials(url):
    resp = requests.get(url)
    return extract_tutorials(resp.text)


def get_tutorials(url):
    tutorials = download_tutorials(url)
    return serialize_tutorials(tutorials)


def main():
    """
    Download tutorials of every content in every module
    eg) Vectors and spaces(module) => Vectors(content) => Vector intro for linear algebra(tutorial)
    """
    modules = [{
        'title': 'Vectors and spaces',
        'url': 'https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces'}, {
        'title': 'Matrix transformations',
        'url': 'https://www.khanacademy.org/math/linear-algebra/matrix-transformations'}, {
        'title': 'Alternate coordinate systems(bases)',
        'url': 'https://www.khanacademy.org/math/linear-algebra/alternate-bases',
    }]
    for m in modules:
        m['tutorials'] = get_tutorials(m['url'])
    pprint(modules)
    with open('tutorials.json') as f:
        f.write(json.dumps(modules))


if __name__ == '__main__':
    main()
