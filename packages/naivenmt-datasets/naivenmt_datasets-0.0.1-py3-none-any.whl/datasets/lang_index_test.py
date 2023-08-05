import unittest

from datasets.lang_index import WordIndex


class LangIndexTest(unittest.TestCase):

    def testWordIndex(self):
        index = WordIndex('word_index')
        sententce = 'This is a test'
        index.add_sentence(sententce.split(' '))

        vocab = index.vocab(10)
        print(vocab)

        print(index.words2ids(['This']))


if __name__ == "__main__":
    unittest.main()
