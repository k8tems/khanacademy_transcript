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


def convert_hierarchy(hierarchy):
    """Convert dict hierarchy to directory hierarchy"""
    for c in hierarchy:
        for gc in c['children']:
            yield {'path': os.path.join(c['title'], gc['title']), 'video_id': gc['video_id']}


def commit_hierarchy(hierarchy):
    """
    Commit hierarchy to file system so that they can be cached
    :param hierarchy: hierarchy to commit
    :param dest: directory in file system to commit to
    """
    for node in hierarchy:
        create_dir(os.path.dirname(node['path']))
        write_text(node['path'], node['video_id'])


def resolve_paths(hierarchy, dest):
    """
    Resolve relative paths in hierarchy
    :param hierarchy: hierarchy containing video ids; mutated
    :param dest: Destination in file system to save hierarchy
    :return: hierarchy with resolved paths
    """
    for node in hierarchy:
        node['path'] = os.path.join(dest, node['path'])
    return hierarchy


def resolve_indices(hierarchy):
    """
    Prepend index of array element to title so that the order is
    preserved after saving to the file system
    :param hierarchy: hierarchy containing video ids; mutated
    :return: hierarchy with resolved indices
    """
    for i, h in enumerate(hierarchy):
        h['title'] = '%d %s' % (i, h['title'])
        if 'children' in h:
            resolve_indices(h['children'])
    return hierarchy


def fix_illegal_names(hierarchy):
    """
    Fix illegal names
    :param hierarchy: hierarchy containing video ids; mutated
    :return: hierarchy with resolved indices
    """
    for i, h in enumerate(hierarchy):
        h['title'] = h['title'].replace('/', '_').replace(':', '_')
        if 'children' in h:
            fix_illegal_names(h['children'])
    return hierarchy


def process_modules(url, dest_dir):
    for m_i, m in enumerate(get_modules(url)):
        module_title = '%d %s' % (m_i, m['title'])
        print('\tProcessing ' + module_title)

        module_dir = os.path.join(dest_dir, module_title)

        if os.path.exists(module_dir):
            print('\t\tSkipping ' + module_dir)
            continue

        hierarchy = TutorialSpider.crawl(m['url'])
        hierarchy = resolve_indices(hierarchy)
        hierarchy = fix_illegal_names(hierarchy)
        hierarchy = list(convert_hierarchy(hierarchy))
        hierarchy = resolve_paths(hierarchy, module_dir)
        commit_hierarchy(hierarchy)

        print('\tSaved ' + module_title)


def main():
    """
    Download tutorials of every content in every module
    eg) Vectors and spaces(module) => Vectors(content) => Vector intro for linear algebra(tutorial)
    """
    for m in ModuleSpider.crawl('https://www.khanacademy.org/math'):
        module_title = m['title']
        print('Processing ' + module_title)
        subject_dir = os.path.join('video_ids', module_title)
        process_modules('https://www.khanacademy.org' + m['url'], subject_dir)


if __name__ == '__main__':
    main()
