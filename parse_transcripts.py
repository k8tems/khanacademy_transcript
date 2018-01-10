import os
import xml.etree.ElementTree as ET


def read_text(fname):
    with open(fname) as f:
        return f.read()


def write_text(fname, text):
    with open(fname, 'w') as f:
        f.write(text)


def parse_transcript(xml_transcript):
    result = ''
    root = ET.fromstring(xml_transcript)
    for child in root:
        # Make sure to convert `None` to ''
        text = child.text or ''
        result += '%s%s\n' % (child.attrib['start'].ljust(6), text)
    return result


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def remove_extension(fname):
    return fname[:fname.find('.')]


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
                txt_transcript = parse_transcript(xml_transcript)

                out_dir = os.path.join('transcripts', 'txt', md, cd)
                create_dir(out_dir)
                out_file = os.path.join(out_dir, remove_extension(t) + '.txt')
                write_text(out_file, txt_transcript)
