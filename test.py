import os
import unittest
import download_tutorials
import parse_transcripts


class TestExtractReactComponent(unittest.TestCase):
    def test(self):
        with open(os.path.join('fixtures', 'react_component.html')) as f:
            data = f.read()
        self.assertEqual({'loggedIn': True, 'componentProps': {'foo': 'bar'}}, download_tutorials.extract_react_component(data))

    def test_component_not_found(self):
        data = '<script></script>'
        self.assertRaises(download_tutorials.ReactComponentNotFound, download_tutorials.extract_react_component, data)


class TestParseTranscript(unittest.TestCase):
    def test(self):
        transcript = '<?xml version="1.0" encoding="utf-8" ?><transcript>' \
                     '<text start="0" dur="0.83">foo</text><text start="0.83" dur="5.01">bar</text></transcript>'
        expected = '0    foo\n0.83  bar'
        self.assertEqual(expected, parse_transcripts.parse_transcript(transcript))


if __name__ == '__main__':
    unittest.main()
