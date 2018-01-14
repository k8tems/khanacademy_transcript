import html
import os
import xml.etree.ElementTree as ET
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


if __name__ == '__main__':
    xml_dir = os.path.join('transcripts', 'xml')
    for path in generate_sub_directories(xml_dir):
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
