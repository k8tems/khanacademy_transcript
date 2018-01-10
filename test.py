import unittest
import download_tutorials
import parse_transcripts


class TestExtractReactComponent(unittest.TestCase):
    def test(self):
        fixture = '''<script>
(function() {
    var React = KAdefine.require("react");
    var ReactDOM = KAdefine.require("react-dom");
    var ApolloWrapper = React.createFactory(KAdefine.require(
        "./javascript/apollo-package/apollo-wrapper.jsx"));
    var Component = KAdefine.require("./javascript/app-shell-package/app.jsx");
    var ReactComponent = React.createFactory(
        Component.default || Component);
    ReactDOM.render(ApolloWrapper({
        initialState: null,
        children: ReactComponent({"componentProps": {"foo": "bar"}, "loggedIn": true})
    }), document.getElementById("_kareact_0"));
})();
</script>'''
        self.assertEqual({'loggedIn': True, 'componentProps': {'foo': 'bar'}}, download_tutorials.extract_react_component(fixture))

    def test_component_not_found(self):
        data = '<script></script>'
        self.assertRaises(download_tutorials.ReactComponentNotFound, download_tutorials.extract_react_component, data)


class TestParseTranscript(unittest.TestCase):
    def test(self):
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
        expected = '00:00  foo\\nbar\\nbaz\n00:01  qux\n'
        self.assertEqual(expected, parse_transcripts.parse_transcript(transcript))

    def test_unescape_html(self):
        transcript = '<?xml version="1.0" encoding="utf-8" ?>' \
                     '<transcript>' \
                     '<text start="0" dur="1">fo&amp;#39;o</text>' \
                     '</transcript>'
        expected = '00:00  fo\'o\n'
        self.assertEqual(expected, parse_transcripts.parse_transcript(transcript))


class TestFormatStart(unittest.TestCase):
    def test(self):
        self.assertEqual('15:32', parse_transcripts.format_start('932'))


if __name__ == '__main__':
    unittest.main()
