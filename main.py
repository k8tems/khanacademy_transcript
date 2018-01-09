import json


def get_videos_from_tutorials(tutorials):
    videos = []
    for t in tutorials:
        videos.append({
            'title': t['title'],
            'videos': [ci for ci in t['contentItems']]})
    return videos


def parse():
    with open('input.json', 'r') as f:
        data = json.loads(f.read())
    tutorials = data['componentProps']['curation']['tabs'][0]['modules'][0]['tutorials']
    videos = get_videos_from_tutorials(tutorials)


def main():
    parse()


if __name__ == '__main__':
    main()
