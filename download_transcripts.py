import os
import json
import requests
from file import create_dir, write_text, read_text
from stat import S_ISDIR, ST_MODE


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


def is_directory(path):
    """Check if `path` is a directory"""
    mode = os.stat(path)[ST_MODE]
    return S_ISDIR(mode)


def is_transcript_directory(path):
    """Check if the `path` is a directory containing transcripts"""
    first_fname = os.listdir(path)[0]
    first_fname = os.path.join(path, first_fname)
    return not is_directory(first_fname)


def generate_transcript_directories(root, path=''):
    """
    Recursively generate all subdirectories containing transcripts
    :param root: root path
    :param path: current relative path
    :return: directory containing transcripts
    """
    for sub in os.listdir(os.path.join(root, path)):
        subpath = os.path.join(path, sub)
        if is_transcript_directory(os.path.join(root, subpath)):
            yield subpath
        else:
            yield from generate_transcript_directories(root, subpath)


if __name__ == '__main__':
    src = 'video_ids'
    for path in generate_transcript_directories(src):
        cd = os.path.join(src, path)
        for fname in os.listdir(cd):
            print(cd, fname)
