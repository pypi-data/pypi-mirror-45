import unittest

from datasets.seq2vec import Seq2VecLoader


class Seq2VecTest(unittest.TestCase):

    def testSeq2VecLoader(self):
        loader = Seq2VecLoader('testdata/seq2vec.txt')
        seq2vec_dict = loader.load()
        for k, v in seq2vec_dict.items():
            print('%s -> %s' % (k, v))


if __name__ == "__main__":
    unittest.main()
