import unittest
from ..string_utils.trie import SimpleTrie


class TestClientMethods(unittest.TestCase):

    def test_simpletrie(self):
        ptrie = SimpleTrie()
        inputs = ('123456789', 'abcdefghijk', 'lmnopq', 'r', '')
        for x in inputs:
            ptrie.add(x)
        for x in inputs:
            self.assertTrue(ptrie.exact_string_match(x))
            self.assertFalse(ptrie.exact_string_match(x + '12'))
        self.assertTrue(ptrie.approximate_string_match('1234567', 2)[0])
        self.assertTrue(ptrie.approximate_string_match('123456712', 2)[0])
        self.assertTrue(ptrie.approximate_string_match('12345678912', 2)[0])
        self.assertFalse(ptrie.approximate_string_match('1234567', 1)[0])
        self.assertFalse(ptrie.approximate_string_match('123456712', 1)[0])
        self.assertFalse(ptrie.approximate_string_match('12345678912', 1)[0])

    if __name__ == '__main__':
        unittest.main()
