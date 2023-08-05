import os


class Seq2VecLoader:

    def __init__(self, f):
        if not os.path.exists(f):
            raise ValueError('file does not exist: %s' % f)
        self.seq2vec_file = f
        self.seq2vec_dict = {}

    def load(self):
        with open(self.seq2vec_file, mode='rt', encoding='utf8', buffering=8192) as fin:
            for line in fin:
                line = line.strip('\n')
                if not line:
                    continue
                segs = line.split('@')
                if len(segs) != 2:
                    continue
                vec, seq = segs[0], segs[1]
                if not seq.strip() or not vec.strip():
                    continue
                self.seq2vec_dict[seq] = vec

        return self.seq2vec_dict


