import json


def get_videos_from_content_items(t):
    result = []
    for node in t['contentItems']:
        result.append(node)
    return result


def get_videos_from_tutorials(tutorials):
    videos = []
    for t in tutorials:
        videos += get_videos_from_content_items(t)
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
