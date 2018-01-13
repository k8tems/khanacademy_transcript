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


def process_tutorials(tutorials, base_dir):
    for t_i, t in enumerate(tutorials):
        dest_dir = os.path.join(base_dir, '%d %s' % (t_i, t['title']))
        create_dir(dest_dir)
        for v_i, (video_title, _, video_id) in enumerate(t['videos']):
            fname = '%d %s.xml' % (v_i, video_title.replace('/', '_'))
            fname = os.path.join(dest_dir, fname)
            print(fname, video_id)

            if should_skip_transcript(fname):
                print('\t', 'skipping')
                continue

            transcript = download_transcript(video_id)
            write_text(fname, transcript)


def process_modules(modules, base_dir):
    for m_i, m in enumerate(modules):
        # Do not overwrite `base_dir`
        dest_dir = os.path.join(base_dir, '%d %s' % (m_i, m['title']))
        process_tutorials(modules, dest_dir)


if __name__ == '__main__':
    subject = 'Linear Algebra'
    src_fname = os.path.join('transcripts', 'tutorials', subject + '.json')
    modules = json.loads(read_text(src_fname))
    base_dir = os.path.join('transcripts', 'xml', subject)
    process_modules(modules, base_dir)
