import json
from pprint import pprint


def parse_content_items(content_items):
    result = []
    for ci in content_items:
        # practice nodes do not have videos
        if 'youtubeId' not in ci:
            continue
        result.append((ci['title'], ci['description'], ci['youtubeId']))
    return result


def parse_tutorials(tutorials):
    videos = []
    for t in tutorials:
        videos.append({
            'title': t['title'],
            'videos': parse_content_items(t['contentItems'])})
    return videos


def get_tutorials(url):
    return []


def parse():
    url = 'https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces'
    tutorials = get_tutorials(url)
    videos = parse_tutorials(tutorials)
    pprint(videos)


def main():
    parse()


if __name__ == '__main__':
    main()
