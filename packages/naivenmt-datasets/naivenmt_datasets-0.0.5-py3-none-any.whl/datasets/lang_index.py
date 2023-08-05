from collections import Counter


class WordIndex:

    def __init__(self, name):
        self.name = name
        self.word2id = {}
        self.id2word = {0: 'unk'}
        self.vocab_size = 1 # unk

        self.word2count = Counter()

    def add_sentence(self, sentence):
        for word in sentence:
            self.add_word(word)

    def add_word(self, word):
        self.word2count[word] += 1
        if word in self.word2id:
            return
        self.word2id[word] = self.vocab_size
        self.id2word[self.vocab_size] = word
        self.vocab_size += 1

    def vocab(self, n=None):
        return [v for v, _ in self.word2count.most_common(n)]

    def words2ids(self, words):
        return [self.word2id[v] for v in words]

    def ids2words(self, ids):
        return [self.id2word[v] for v in ids]
