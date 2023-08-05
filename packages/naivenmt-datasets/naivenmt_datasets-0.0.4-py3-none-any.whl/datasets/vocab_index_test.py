import unittest

from datasets.vocab_index import VocabIndex


class VocabIndexTest(unittest.TestCase):

    def testVocabIndex(self):
        vocab = ['hello', 'word']
        index = VocabIndex(vocab)

        print(index.convert_ids_to_words([0, 1, 2]))
        print(index.convert_words_to_ids(['hello', 'word']))


if __name__ == "__main__":
    unittest.main()

