import json
from pprint import pprint


if __name__ == '__main__':
    with open('tutorials.json') as f:
        modules = json.loads(f.read())
    for m in modules:
        print(m['title'])
        for t in m['tutorials']:
            for v in t['videos']:
                print('\t', v[0], v[2])
