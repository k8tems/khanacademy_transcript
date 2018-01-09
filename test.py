import unittest
import download_tutorials


class TestExtractReactComponent(unittest.TestCase):
    def test(self):
        with open('fixture.html') as f:
            data = f.read()
        self.assertEqual({'loggedIn': True, 'componentProps': {'foo': 'bar'}}, download_tutorials.extract_react_component(data))

    def test_component_not_found(self):
        data = '<script></script>'
        self.assertRaises(download_tutorials.ReactComponentNotFound, download_tutorials.extract_react_component, data)


if __name__ == '__main__':
    unittest.main()
