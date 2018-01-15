import os
import re
import json
import requests
from pprint import pprint
from file import write_text, create_dir


def download(url):
    return requests.get(url).text


class ReactComponentNotFound(RuntimeError):
    pass


class ReactSpider(object):
    @staticmethod
    def extract_react_component(page_source):
        """
        Extract data used to initialize `ReactComponent` from the given page source
        This will only work if the `ReactComponent` is constructed in one line
        """
        regex = re.search('ReactComponent\((.+,\s*"loggedIn".+?})', page_source)
        if not regex:
            raise ReactComponentNotFound(page_source)
        return json.loads(regex.group(1))

    @classmethod
    def crawl(cls, url):
        page_source = download(url)
        react_component = cls.extract_react_component(page_source)
        return cls.filter(react_component)

    @classmethod
    def filter(cls, component):
        """
        filter and return necessary data from react component
        :param component: unfiltered data used to initialize `ReactComponent`
        :return: filtered data
        """
        raise NotImplemented()


class TutorialSpider(ReactSpider):
    @classmethod
    def filter_content_items(cls, content_items):
        result = []
        for ci in content_items:
            # practice nodes do not have videos
            if 'youtubeId' not in ci:
                continue
            result.append({'title': ci['title'], 'video_id': ci['youtubeId']})
        return result

    @classmethod
    def filter(cls, component):
        tutorials = component['componentProps']['curation']['tabs'][0]['modules'][0]['tutorials']
        nodes = []
        for t in tutorials:
            nodes.append({
                'title': t['title'],
                'children': cls.filter_content_items(t['contentItems'])})
        return nodes


class ModuleSpider(ReactSpider):
    @classmethod
    def filter(cls, component):
        modules = component['componentProps']['curation']['tabs'][0]['modules']
        modules = [m for m in modules if m['kind'] == 'TableOfContentsRow']
        return [{'title': m['title'], 'url': m['url']} for m in modules]


def get_url_base(url):
    regex = re.search('(.+://.+?)/.+', url)
    return regex.group(1)


def adjust_module_urls(modules, url):
    """Convert relative paths to full urls"""
    url_base = get_url_base(url)
    for m in modules:
        m['url'] = url_base + m['url']
    return modules


def get_modules(url):
    modules = ModuleSpider.crawl(url)
    return adjust_module_urls(modules, url)


def save(title, modules):
    out_dir = os.path.join('transcripts', 'tutorials')
    create_dir(out_dir)
    fname = os.path.join(out_dir, title + '.json')
    write_text(fname, json.dumps(modules))


def generate_directories(root):
    """Convert dict hierarchy to directory hierarchy"""
    for c in root:
        for gc in c['children']:
            yield {'path': os.path.join(c['title'], gc['title']), 'video_id': gc['video_id']}


def main():
    """
    Download tutorials of every content in every module
    eg) Vectors and spaces(module) => Vectors(content) => Vector intro for linear algebra(tutorial)
    """
    subject = 'Linear Algebra'
    url = 'https://www.khanacademy.org/math/linear-algebra'
    print('Getting modules')
    result = []
    modules = get_modules(url)
    for m in modules:
        print('Processing ' + m['title'])
        result += generate_directories(TutorialSpider.crawl(m['url']))
        for r in result:
            r['path'] = os.path.join(subject, m['title'], r['path'])
    pprint(result)


if __name__ == '__main__':
    main()
