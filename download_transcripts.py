import os
import json
import requests
from file import create_dir, write_text, read_text


def download_transcript(video_id):
    lang = 'en'
    resp = requests.get(
        'https://video.google.com/timedtext?lang=%s&v=%s' % (lang, video_id))
    return resp.text


def should_skip_transcript(dest_file):
    """
    Return true if the transcript has already been processed
    i.e. The file exists and is not empty
    """
    return os.path.exists(dest_file) and os.stat(dest_file).st_size != 0


if __name__ == '__main__':
    modules = json.loads(read_text('tutorials.json'))
    for m in modules:
        module_title = m['title']
        print(module_title)
        for t in m['tutorials']:
            for v in t['videos']:
                print('\t', v[0], v[2])
                dest_dir = os.path.join('transcripts', 'xml', module_title, t['title'])
                create_dir(dest_dir)
                dest_file = os.path.join(dest_dir, v[0].replace('/', '_') + '.xml')

                if should_skip_transcript(dest_file):
                    print('skipping', dest_file)
                    continue

                transcript = download_transcript(v[2])
                write_text(dest_file, transcript)
