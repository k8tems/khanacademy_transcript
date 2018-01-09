import json


def download_transcript(video_id):
    pass


if __name__ == '__main__':
    with open('tutorials.json') as f:
        modules = json.loads(f.read())
    for m in modules:
        print(m['title'])
        for t in m['tutorials']:
            for v in t['videos']:
                print('\t', v[0], v[2])
                download_transcript(v[2])
                a
