import tensorflow as tf

from datasets.dssm import QueryDocSameFileDataset, QueryDocSeparateFilesDataset
from datasets.utils import data_dir_utils as utils


class QueryDocDatasetTest(tf.test.TestCase):

    def testQueryDocSameFileDataset(self):
        config = {
            'train_batch_size': 1,
            'eval_batch_size': 1,
            'predict_batch_size': 1,
            'num_parallel_calls': 1
        }
        o = QueryDocSameFileDataset(
            train_files=[utils.get_data_file('dssm.query.doc.label.txt')],
            eval_files=[utils.get_data_file('dssm.query.doc.label.txt')],
            predict_files=[utils.get_data_file('dssm.query.doc.label.txt')],
            vocab_file=utils.get_data_file('dssm.vocab.txt'),
            params=config)

        train_dataset = o.build_train_dataset()
        eval_dataset = o.build_eval_dataset()
        predict_dataset = o.build_predict_dataset()

        # print(train_dataset)

        for v in iter(train_dataset):
            (q, d), l = v
            print(q)
            print(d)
            print(l)
            print('=====================================')
        print('+++++++++++++++++++++++++++++++++++++')

        (q, d), l = next(iter(eval_dataset))
        print(q)
        print(d)
        print(l)
        print('=====================================')

        (q, d) = next(iter(predict_dataset))
        print(q)
        print(d)
        print('=====================================')

    def testQueryDocSeparateFilesDataset(self):
        config = {
            'train_batch_size': 1,
            'eval_batch_size': 1,
            'predict_batch_size': 1,
            'num_parallel_calls': 1
        }
        o = QueryDocSeparateFilesDataset(
            train_query_files=[utils.get_data_file('dssm.query.txt')],
            train_doc_files=[utils.get_data_file('dssm.doc.txt')],
            train_label_files=[utils.get_data_file('dssm.label.txt')],
            eval_query_files=[utils.get_data_file('dssm.query.txt')],
            eval_doc_files=[utils.get_data_file('dssm.doc.txt')],
            eval_label_files=[utils.get_data_file('dssm.label.txt')],
            predict_query_files=[utils.get_data_file('dssm.query.txt')],
            predict_doc_files=[utils.get_data_file('dssm.doc.txt')],
            vocab_file=utils.get_data_file('dssm.vocab.txt'),
            params=config)

        train_dataset = o.build_train_dataset()
        eval_dataset = o.build_eval_dataset()
        predict_dataset = o.build_predict_dataset()

        # print(train_dataset)

        for v in iter(train_dataset):
            (q, d), l = v
            print(q)
            print(d)
            print(l)
            print('=====================================')
        print('+++++++++++++++++++++++++++++++++++++')

        (q, d), l = next(iter(eval_dataset))
        print(q)
        print(d)
        print(l)
        print('=====================================')

        (q, d) = next(iter(predict_dataset))
        print(q)
        print(d)
        print('=====================================')


if __name__ == '__main__':
    tf.test.main()
