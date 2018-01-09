import json
from pprint import pprint


def get_videos_from_content_items(content_items):
    result = []
    for ci in content_items:
        if 'youtubeId' not in ci:
            continue
        result.append((ci['title'], ci['description'], ci['youtubeId']))
    return result


def get_videos_from_tutorials(tutorials):
    videos = []
    for t in tutorials:
        videos.append({
            'title': t['title'],
            'videos': get_videos_from_content_items(t['contentItems'])})
    return videos


def parse():
    with open('input.json', 'r') as f:
        data = json.loads(f.read())
    tutorials = data['componentProps']['curation']['tabs'][0]['modules'][0]['tutorials']
    videos = get_videos_from_tutorials(tutorials)
    pprint(videos)


def main():
    parse()


if __name__ == '__main__':
    main()
