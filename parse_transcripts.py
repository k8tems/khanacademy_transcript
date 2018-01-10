import os


def read_text(fname):
    with open(fname) as f:
        return f.read()


def parse_transcript(xml_transcript):
    pass


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
