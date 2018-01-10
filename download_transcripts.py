import os
import json
import requests


def download_transcript(video_id):
    lang = 'en'
    resp = requests.get(
        'https://video.google.com/timedtext?lang=%s&v=%s' % (lang, video_id))
    return resp.text


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == '__main__':
    with open('tutorials.json') as f:
        modules = json.loads(f.read())
    for m in modules:
        module_title = m['title']
        print(module_title)
        for t in m['tutorials']:
            for v in t['videos']:
                print('\t', v[0], v[2])
                transcript = download_transcript(v[2])
                dest_dir = os.path.join('transcripts', 'xml', module_title, t['title'])
                create_dir(dest_dir)
                dest = os.path.join(dest_dir, v[0] + '.xml')
                with open(dest, 'w') as f:
                    f.write(transcript)
                a
