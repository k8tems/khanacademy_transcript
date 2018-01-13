import os
import re
import json
import requests
from pprint import pprint
from file import write_text, create_dir


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


def extract_modules(page_source):
    component = extract_react_component(page_source)
    modules = component['componentProps']['curation']['tabs'][0]['modules']
    return [m for m in modules if m['kind'] == 'TableOfContentsRow']


def download_modules(url):
    return extract_modules(requests.get(url).text)


def serialize_modules(modules):
    return [{'title': m['title'], 'url': m['url']} for m in modules]


def get_url_base(url):
    regex = re.search('(.+://.+?)/.+', url)
    return regex.group(1)


def get_modules(url):
    modules = download_modules(url)
    modules = serialize_modules(modules)
    url_base = get_url_base(url)
    for m in modules:
        m['url'] = url_base + m['url']
    return modules


def main():
    """
    Download tutorials of every content in every module
    eg) Vectors and spaces(module) => Vectors(content) => Vector intro for linear algebra(tutorial)
    """
    title = 'Linear Algebra'
    url = 'https://www.khanacademy.org/math/linear-algebra'
    print('Getting modules')
    modules = get_modules(url)
    for m in modules:
        print('Processing ' + m['title'])
        m['tutorials'] = get_tutorials(m['url'])
    pprint(modules)
    out_dir = os.path.join('transcripts', 'tutorials')
    create_dir(out_dir)
    fname = os.path.join(out_dir, title + '.json')
    write_text(fname, json.dumps(modules))


if __name__ == '__main__':
    main()
