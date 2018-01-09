import unittest
import main


class TestExtractTutorials(unittest.TestCase):
    def test(self):
        with open('fixture.html') as f:
            data = f.read()
        self.assertEqual('foo', main.extract_tutorials(data))

    def test_component_not_found(self):
        data = '<script></script>'
        self.assertRaises(main.ReactComponentNotFound, main.extract_tutorials, data)


if __name__ == '__main__':
    unittest.main()
