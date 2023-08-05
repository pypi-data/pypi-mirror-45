
class VocabIndex:
    """Build word2id and id2word map by a existing vocab."""

    def __init__(self, vocab):
        self.vocab2id = {}
        self.id2vocab = {0: 'unk'}
        self.vocab_size = 1 # unk

        for v in vocab:
            if v in self.vocab2id:
                continue
            self.vocab2id[v] = self.vocab_size
            self.id2vocab[self.vocab_size] = v
            self.vocab_size += 1

    def convert_words_to_ids(self, words):
        return [self.vocab2id[v] for v in words]

    def convert_ids_to_words(self, ids):
        return [self.id2vocab[v] for v in ids]



