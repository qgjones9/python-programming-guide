import unittest

from trie import Trie


class TrieTests(unittest.TestCase):
    def test_insert_and_contains(self):
        trie = Trie()
        trie.insert('cat')
        trie.insert('coat')
        self.assertEqual(len(trie), 2)
        self.assertTrue(trie.contains('cat'))
        self.assertTrue(trie.contains('coat'))
        self.assertFalse(trie.contains('ca'))
        self.assertFalse(trie.contains('dog'))

    def test_insert_duplicate_updates_value_without_size_change(self):
        trie = Trie()
        trie.insert('cat', 'v1')
        trie.insert('cat', 'v2')
        self.assertEqual(len(trie), 1)
        self.assertEqual(trie.search('cat'), 'v2')

    def test_search(self):
        trie = Trie()
        trie.insert('analytics', {'id': 1})
        trie.insert('car')
        self.assertEqual(trie.search('analytics'), {'id': 1})
        self.assertIsNone(trie.search('car'))
        self.assertIsNone(trie.search('ana'))
        self.assertIsNone(trie.search('dog'))

    def test_starts_with(self):
        trie = Trie()
        trie.insert('cat')
        trie.insert('coat')
        self.assertTrue(trie.starts_with('c'))
        self.assertTrue(trie.starts_with('ca'))
        self.assertTrue(trie.starts_with('cat'))
        self.assertFalse(trie.starts_with('dog'))

    def test_delete_shared_prefix(self):
        trie = Trie()
        trie.insert('cat')
        trie.insert('car')
        self.assertTrue(trie.delete('cat'))
        self.assertEqual(len(trie), 1)
        self.assertFalse(trie.contains('cat'))
        self.assertTrue(trie.contains('car'))

    def test_delete_nonexistent(self):
        trie = Trie()
        trie.insert('cat')
        self.assertFalse(trie.delete('dog'))
        self.assertEqual(len(trie), 1)
        self.assertFalse(trie.delete('ca'))
        self.assertEqual(len(trie), 1)

    def test_delete_only_word(self):
        trie = Trie()
        trie.insert('cat')
        self.assertTrue(trie.delete('cat'))
        self.assertEqual(len(trie), 0)
        self.assertFalse(trie.contains('cat'))
        self.assertFalse(trie.starts_with('c'))

    def test_delete_longer_word_keeps_shorter(self):
        trie = Trie()
        trie.insert('analytics')
        trie.insert('analytics pro')
        self.assertTrue(trie.delete('analytics pro'))
        self.assertEqual(len(trie), 1)
        self.assertTrue(trie.contains('analytics'))
        self.assertFalse(trie.contains('analytics pro'))

    def test_empty_string_key(self):
        trie = Trie()
        trie.insert('', 'root-value')
        self.assertEqual(len(trie), 1)
        self.assertTrue(trie.contains(''))
        self.assertEqual(trie.search(''), 'root-value')
        self.assertEqual(trie.collect(''), [''])
        self.assertTrue(trie.delete(''))
        self.assertEqual(len(trie), 0)

    def test_collect_and_collect_values(self):
        trie = Trie()
        trie.insert('cat', 1)
        trie.insert('car', 2)
        trie.insert('coat', 3)
        self.assertEqual(trie.collect('ca'), ['car', 'cat'])
        self.assertEqual(trie.collect_values('ca'), [2, 1])

    def test_longest_common_prefix(self):
        trie = Trie()
        for word in ('cat', 'car', 'coat'):
            trie.insert(word)
        self.assertEqual(trie.longest_common_prefix(), 'c')

    def test_clear(self):
        trie = Trie()
        trie.insert('cat')
        trie.insert('car')
        trie.clear()
        self.assertEqual(len(trie), 0)
        self.assertFalse(trie.contains('cat'))

    def test_validate_key_type(self):
        trie = Trie()
        with self.assertRaises(TypeError):
            trie.insert(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trie.delete(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trie.collect_values(42)  # type: ignore[arg-type]


if __name__ == '__main__':
    unittest.main()
