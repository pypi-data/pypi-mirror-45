import os


def gen_vocab(input_files, vocab_file):
    vocab = set()
    for f in input_files:
        if not os.path.exists(f):
            continue
        with open(f, mode='rt', encoding='utf8', buffering=8192) as fin:
            for line in fin:
                line = line.strip('\n')
                if not line:
                    continue
                for v in line:
                    if not v.strip():
                        continue
                    vocab.add(v)
    unk = False
    if '<unk>' in vocab:
        unk = True
    vocab = list(vocab)
    if not unk:
        vocab.insert(0, '<unk')

    with open(vocab_file, mode='wt', encoding='utf8', buffering=8192) as fout:
        for v in vocab:
            fout.write(v + '\n')
