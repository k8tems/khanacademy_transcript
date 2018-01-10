import os
import xml.etree.ElementTree as ET


def read_text(fname):
    with open(fname) as f:
        return f.read()


def parse_transcript(xml_transcript):
    result = ''
    root = ET.fromstring(xml_transcript)
    for child in root:
        # Make sure to convert `None` to ''
        text = child.text or ''
        result += '%s%s\n' % (child.attrib['start'].ljust(6), text)
    return result


if __name__ == '__main__':
    xml_dir = os.path.join('transcripts', 'xml')
    module_dirs = os.listdir(xml_dir)
    for md in module_dirs:
        print(md)
        content_dirs = os.listdir(os.path.join(xml_dir, md))
        for cd in content_dirs:
            print('\t', cd)
            tutorials = os.listdir(os.path.join(xml_dir, md, cd))
            for t in tutorials:
                print('\t\t', t)
                xml_transcript = read_text(os.path.join(xml_dir, md, cd, t))
                parse_transcript(xml_transcript)
