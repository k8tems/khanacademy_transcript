import unittest
import main


class TestParseTutorials(unittest.TestCase):
    def test(self):
        with open('fixture.html') as f:
            data = f.read()
        expected = {'componentProps': [{'foo': 'bar'}]}
        self.assertEqual(expected, main.parse_tutorials(data))


if __name__ == '__main__':
    unittest.main()
