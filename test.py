import unittest
import main


class TestParseTutorials(unittest.TestCase):
    def test(self):
        with open('fixture.html') as f:
            data = f.read()
        self.assertEqual('foo', main.parse_tutorials(data))

    def test_component_not_found(self):
        data = '<script></script>'
        self.assertRaises(main.ReactComponentNotFound, main.parse_tutorials, data)


if __name__ == '__main__':
    unittest.main()
