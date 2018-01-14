import html
import os
import xml.etree.ElementTree as ET
from stat import S_ISDIR, ST_MODE
from file import create_dir, read_text, write_text


def format_start(start):
    return '%02d:%02d' % (start // 60, start % 60)


def parse_transcript(xml_transcript):
    result = ''
    root = ET.fromstring(xml_transcript)
    for child in root:
        # Make sure to convert `None` to ''
        text = child.text or ''
        # Explicit newlines hinder search; using space instead
        text = text.replace('\n', ' ')
        text = html.unescape(text)
        start = format_start(int(float(child.attrib['start'])))
        result += '%s%s\n' % (start.ljust(7), text)
    return result


def remove_extension(fname):
    return fname[:fname.find('.')]


def is_directory(path):
    mode = os.stat(path)[ST_MODE]
    return S_ISDIR(mode)


def is_transcript_directory(path):
    """Check if the path is a directory containing transcripts"""
    first_fname = os.listdir(path)[0]
    first_fname = os.path.join(path, first_fname)
    return not is_directory(first_fname)


def generate_transcript_directories(root):
    """Generate all directories containing transcripts"""
    for path in os.listdir(root):
        path = os.path.join(root, path)
        if is_transcript_directory(path):
            yield path
        else:
            yield from generate_transcript_directories(path)


if __name__ == '__main__':
    from pprint import pprint
    pprint(list(generate_transcript_directories(os.path.join('transcripts', 'xml'))))
    a
    xml_dir = os.path.join('transcripts', 'xml')
    for path in generate_transcript_directories(xml_dir):
        for t in os.listdir(os.path.join(xml_dir, path)):
            print('\t\t', t)
            in_fname = os.path.join(xml_dir, path, t)
            xml_transcript = read_text(in_fname)
            # Sometimes the transcript is empty; Maybe try downloading again?
            if not xml_transcript:
                continue
            txt_transcript = parse_transcript(xml_transcript)

            out_dir = os.path.join('transcripts', 'txt', path)
            create_dir(out_dir)
            out_fname = os.path.join(out_dir, remove_extension(t) + '.txt')
            # `:` is illegal in windows
            out_fname = out_fname.replace(':', '_')
            write_text(out_fname, txt_transcript)
