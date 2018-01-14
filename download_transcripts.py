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


def generate_videos(video_data, path=''):
    """Recursively generate `video_id`,`path` pairs from given video hierarchy"""
    for i, child in enumerate(video_data):
        title = child['title']
        # Do not update `path`
        child_path = os.path.join(path, '%d %s' % (i, title))
        if 'video_id' in child:
            yield child['video_id'], child_path
        else:
            yield from generate_videos(child['children'], child_path)


if __name__ == '__main__':
    subject = 'Linear Algebra'
    src_fname = os.path.join('transcripts', 'tutorials', subject + '.json')
    video_data = json.loads(read_text(src_fname))
    dest_dir = os.path.join('transcripts', 'xml', subject)

    for video_id, path in generate_videos(video_data):
        print(video_id, path)
        fname = os.path.join(dest_dir, path) + '.xml'

        if should_skip_transcript(fname):
            print('\t', 'skipping')
            continue

        transcript = download_transcript(video_id)
        create_dir(os.path.dirname(fname))
        write_text(fname, transcript)
