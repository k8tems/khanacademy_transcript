import os


if __name__ == '__main__':
    xml_dir = os.path.join('transcripts', 'xml')
    module_dirs = os.listdir(xml_dir)
    for md in module_dirs:
        print(md)
        content_dirs = os.listdir(os.path.join(xml_dir, md))
        for cd in content_dirs:
            print('\t', cd)
