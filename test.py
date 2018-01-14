import unittest
import download_video_ids
import parse_transcripts


class TestGetUrlBase(unittest.TestCase):
    def test(self):
        expected = 'https://www.khanacademy.org'
        result = download_video_ids.get_url_base('https://www.khanacademy.org/math/linear-algebra')
        self.assertEqual(expected, result)


class TestExtractReactComponent(unittest.TestCase):
    def test_component_exists(self):
        fixture = 'ReactComponent({"componentProps": {"foo": "bar"}, "loggedIn": true})'
        self.assertEqual({'loggedIn': True, 'componentProps': {'foo': 'bar'}}, download_video_ids.extract_react_component(fixture))

    def test_component_not_found(self):
        fixture = 'ReactComponent({"componentProps": {"foo": "bar"}, "loggdIn": true})'
        self.assertRaises(download_video_ids.ReactComponentNotFound, download_video_ids.extract_react_component, fixture)


class TestParseTranscript(unittest.TestCase):
    def test_empty_text(self):
        transcript = '<?xml version="1.0" encoding="utf-8" ?><transcript>' \
                     '<text start="0" dur="0.83"></text><text start="1" dur="5.01">bar</text></transcript>'
        expected = '00:00  \n00:01  bar\n'
        self.assertEqual(expected, parse_transcripts.parse_transcript(transcript))

    def test_collapse_multiple_lines(self):
        transcript = '<?xml version="1.0" encoding="utf-8" ?>' \
                     '<transcript>' \
                     '<text start="0" dur="1">foo\nbar\nbaz</text>' \
                     '<text start="1" dur="1">qux</text>' \
                     '</transcript>'
        expected = '00:00  foo bar baz\n00:01  qux\n'
        self.assertEqual(expected, parse_transcripts.parse_transcript(transcript))

    def test_unescape_html(self):
        transcript = '<?xml version="1.0" encoding="utf-8" ?>' \
                     '<transcript>' \
                     '<text start="0" dur="1">fo&amp;#39;o</text>' \
                     '</transcript>'
        expected = '00:00  fo\'o\n'
        self.assertEqual(expected, parse_transcripts.parse_transcript(transcript))


class TestFormatStart(unittest.TestCase):
    def test_all_non_zero(self):
        self.assertEqual('15:32', parse_transcripts.format_start(932))

    def test_leading_0(self):
        self.assertEqual('01:02', parse_transcripts.format_start(62))

    def test_remove_decimal(self):
        self.assertEqual('00:03', parse_transcripts.format_start(3.14159))


if __name__ == '__main__':
    unittest.main()
