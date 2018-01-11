import os
import json
import requests
from file import create_dir, write_text


def download_transcript(video_id):
    lang = 'en'
    resp = requests.get(
        'https://video.google.com/timedtext?lang=%s&v=%s' % (lang, video_id))
    return resp.text


if __name__ == '__main__':
    with open('tutorials.json') as f:
        modules = json.loads(f.read())
    for m in modules:
        module_title = m['title']
        print(module_title)
        for t in m['tutorials']:
            for v in t['videos']:
                print('\t', v[0], v[2])
                dest_dir = os.path.join('transcripts', 'xml', module_title, t['title'])
                create_dir(dest_dir)
                dest_file = os.path.join(dest_dir, v[0].replace('/', '_') + '.xml')
                # Skip if already downloaded
                if os.path.exists(dest_file):
                    continue

                transcript = download_transcript(v[2])
                write_text(dest_file, transcript)
