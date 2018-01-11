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
    for m_i, m in enumerate(modules):
        for t_i, t in enumerate(m['tutorials']):
            for v_i, v in enumerate(t['videos']):
                dest_dir = os.path.join(
                    'transcripts', 'xml',
                    str(m_i) + ' ' + m['title'],
                    str(t_i) + ' ' + t['title'])
                create_dir(dest_dir)
                fname = '%d %s.xml' % (v_i, v[0].replace('/', '_'))
                fname = os.path.join(dest_dir, fname)
                print(fname, v[2])

                if should_skip_transcript(fname):
                    print('\t', 'skipping')
                    continue

                transcript = download_transcript(v[2])
                write_text(fname, transcript)
