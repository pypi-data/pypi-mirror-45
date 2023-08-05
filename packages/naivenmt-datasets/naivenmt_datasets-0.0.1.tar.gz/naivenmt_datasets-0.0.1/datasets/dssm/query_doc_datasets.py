import tensorflow as tf
from tensorflow.python.ops import lookup_ops

__all__ = ["QueryDocSameFileDataset", "QueryDocSeparateFilesDataset"]


def label_normalize_fn(x):
    """Normalize labels.
        For binary classification problem, one may use `0` or `1 0` to identify negative example,
    use `1` or `0 1` to identify positive examples.

    Args:
        x: A tensor, label

    Returns:
        A tensor, 0 or 1
    """
    res = tf.cond(
        tf.logical_or(tf.equal(x, '1'), tf.equal(x, '0 1')),
        lambda: tf.constant(1, dtype=tf.int32),
        lambda: tf.constant(0, dtype=tf.int32)
    )
    return res


class _BaseQueryDocDataset:

    def build_train_dataset(self):
        raise NotImplementedError()

    def build_eval_dataset(self):
        raise NotImplementedError()

    def build_predict_dataset(self):
        raise NotImplementedError()

    def default_config(self):
        params = {
            'unk_id': 0,
            'unk': '<unk>',
            'delimiter': '@',
            'separator': ' ',
            'num_parallel_calls': 4,
            'query_max_len': None,
            'doc_max_len': None,
            'train_batch_size': 32,
            'eval_batch_size': 32,
            'predict_batch_size': 32
        }
        return params

    def _build_dataset(self, dataset, str2id_table, params, mode='train'):
        dataset = dataset.map(
            lambda query, doc, label: (
                tf.string_split([query], delimiter=params['separator']).values,
                tf.string_split([doc], delimiter=params['separator']).values,
                label),
            num_parallel_calls=params['num_parallel_calls']
        ).prefetch(tf.data.experimental.AUTOTUNE)

        if params['query_max_len']:
            dataset = dataset.map(
                lambda query, doc, label: (query[:params['query_max_len']], doc, label),
                num_parallel_calls=params['num_parallel_calls']
            ).prefetch(tf.data.experimental.AUTOTUNE)
        if params['doc_max_len']:
            dataset = dataset.map(
                lambda query, doc, label: (query, doc[:params['doc_max_len']], label),
                num_parallel_calls=params['num_parallel_calls']
            ).prefetch(tf.data.experimental.AUTOTUNE)

        dataset = dataset.map(
            lambda query, doc, label: (
                str2id_table.lookup(query),
                str2id_table.lookup(doc),
                label),
            num_parallel_calls=params['num_parallel_calls']
        ).prefetch(tf.data.experimental.AUTOTUNE)

        batch_size = params['train_batch_size'] if mode == 'train' else params['eval_batch_size']
        dataset = dataset.padded_batch(
            batch_size=batch_size,
            padded_shapes=(tf.TensorShape([None]), tf.TensorShape([None]), tf.TensorShape([])),
            padding_values=(
                tf.constant(tf.cast(params['unk_id'], dtype=tf.int64)),
                tf.constant(tf.cast(params['unk_id'], dtype=tf.int64)),
                0)
        )

        dataset = dataset.map(lambda query, doc, label: ((query, doc), label)).prefetch(tf.data.experimental.AUTOTUNE)
        return dataset

    def _build_predict_dataset(self, dataset, str2id_table, params):
        dataset = dataset.map(
            lambda query, doc: (
                tf.string_split([query], delimiter=params['separator']).values,
                tf.string_split([doc], delimiter=params['separator']).values),
            num_parallel_calls=params['num_parallel_calls']
        ).prefetch(tf.data.experimental.AUTOTUNE)

        if params['query_max_len']:
            dataset = dataset.map(
                lambda query, doc: (query[:params['query_max_len']], doc),
                num_parallel_calls=params['num_parallel_calls']
            ).prefetch(tf.data.experimental.AUTOTUNE)

        if params['doc_max_len']:
            dataset = dataset.map(
                lambda query, doc: (query, doc[:params['doc_max_len']]),
                num_parallel_calls=params['num_parallel_calls']
            ).prefetch(tf.data.experimental.AUTOTUNE)

        dataset = dataset.map(
            lambda query, doc: (str2id_table.lookup(query), str2id_table.lookup(doc)),
            num_parallel_calls=params['num_parallel_calls']
        ).prefetch(tf.data.experimental.AUTOTUNE)

        dataset = dataset.padded_batch(
            batch_size=params['predict_batch_size'],
            padded_shapes=(tf.TensorShape([None]), tf.TensorShape([None])),
            padding_values=(
                tf.constant(params['unk_id'], dtype=tf.int64), tf.constant(params['unk_id'], dtype=tf.int64))
        ).prefetch(tf.data.experimental.AUTOTUNE)
        dataset = dataset.map(lambda query, doc: ([query, doc]))
        return dataset


class QueryDocSameFileDataset(_BaseQueryDocDataset):
    """Build dataset for DSSM network, produce ([query, doc], label) data.
    Query, doc and label are saved in the same files, separated by a special separator. e.g '@'.
    """

    def __init__(self,
                 train_files,
                 eval_files,
                 predict_files,
                 vocab_file,
                 params=None):
        """Init.

        Args:
            train_files: A list of files for training
            eval_files: A list of files for evaluation
            predict_files: A list of files for prediction, may not contains label
            vocab_file: The vocab file, `<unk>` should put in the first line
            params: A python dict(Optional), configurations
        """
        self.train_files = train_files
        self.eval_files = eval_files
        self.predict_files = predict_files
        self.vocab_file = vocab_file

        default_config = self.default_config()
        if params:
            default_config.update(**params)
        self.params = default_config

        self.str2id = lookup_ops.index_table_from_file(self.vocab_file, default_value=self.params['unk_id'])

    def _create_dataset_from_files(self, files):
        dataset = tf.data.Dataset.from_tensor_slices(files)
        dataset = dataset.flat_map(lambda x: tf.data.TextLineDataset(x))
        dataset = dataset.filter(
            lambda x: tf.equal(tf.size(tf.string_split([x], delimiter=self.params['delimiter']).values), 3))
        dataset = dataset.map(
            lambda x: (tf.string_split([x], delimiter=self.params['delimiter']).values[0],
                       tf.string_split([x], delimiter=self.params['delimiter']).values[1],
                       tf.string_split([x], delimiter=self.params['delimiter']).values[2]),
            num_parallel_calls=self.params['num_parallel_calls'])

        dataset = dataset.map(
            lambda query, doc, label: (query, doc, label_normalize_fn(label)),
            num_parallel_calls=self.params['num_parallel_calls'])

        dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
        return dataset

    def build_train_dataset(self):
        dataset = self._create_dataset_from_files(self.train_files)
        # process dataset
        dataset = self._build_dataset(dataset, self.str2id, self.params, mode='train')
        return dataset

    def build_eval_dataset(self):
        dataset = self._create_dataset_from_files(self.eval_files)
        # process dataset
        dataset = self._build_dataset(dataset, self.str2id, self.params, mode='eval')
        return dataset

    def build_predict_dataset(self):
        dataset = self._create_dataset_from_files(self.predict_files)
        dataset = dataset.map(
            lambda query, doc, label: (query, doc),
            num_parallel_calls=self.params['num_parallel_calls']
        )
        # process dataset
        dataset = self._build_predict_dataset(dataset, self.str2id, self.params)
        return dataset


class QueryDocSeparateFilesDataset(_BaseQueryDocDataset):
    """Build dataset for DSSM network, produce ([query, doc], label) data.
    Query, doc and label files are saved in difference files.
    """

    def __init__(self,
                 train_query_files,
                 train_doc_files,
                 train_label_files,
                 eval_query_files,
                 eval_doc_files,
                 eval_label_files,
                 predict_query_files,
                 predict_doc_files,
                 vocab_file,
                 params=None):
        """Init.

        Args:
            train_query_files: A list of query files for training
            train_doc_files: A list of doc files for training
            train_label_files: A list of label files for training
            eval_query_files: A list of query files for evaluation
            eval_doc_files: A list of doc files for evaluation
            eval_label_files: A list of label files for evaluation
            predict_query_files: A list of query files for prediction
            predict_doc_files: A list of doc files for prediction
            vocab_file: The vocab file, `<unk>` should put in the first line
            params: A python dict(Optional), configurations
        """
        self.train_query_files = train_query_files
        self.train_doc_files = train_doc_files
        self.train_label_files = train_label_files
        self.eval_query_files = eval_query_files
        self.eval_doc_files = eval_doc_files
        self.eval_label_files = eval_label_files
        self.predict_query_files = predict_query_files
        self.predict_doc_files = predict_doc_files

        self.vocab_file = vocab_file

        default_params = self.default_config()
        if params:
            default_params.update(**params)
        self.params = default_params

        self.str2id = lookup_ops.index_table_from_file(self.vocab_file, default_value=self.params['unk_id'])

    def _create_dataset_from_files(self, files):
        query, doc, label = files
        query_dataset = tf.data.Dataset.from_tensor_slices(query)
        query_dataset = query_dataset.flat_map(lambda x: tf.data.TextLineDataset(x))

        doc_dataset = tf.data.Dataset.from_tensor_slices(doc)
        doc_dataset = doc_dataset.flat_map(lambda x: tf.data.TextLineDataset(x))

        if label:
            label_dataset = tf.data.Dataset.from_tensor_slices(label)
            label_dataset = label_dataset.flat_map(lambda x: tf.data.TextLineDataset(x))
            label_dataset = label_dataset.map(
                lambda label: label_normalize_fn(label),
                num_parallel_calls=self.params['num_parallel_calls']
            ).prefetch(tf.data.experimental.AUTOTUNE)

            dataset = tf.data.Dataset.zip((query_dataset, doc_dataset, label_dataset))
        else:
            dataset = tf.data.Dataset.zip((query_dataset, doc_dataset))
        return dataset

    def build_train_dataset(self):
        dataset = self._create_dataset_from_files(
            (self.train_query_files, self.train_doc_files, self.train_label_files))
        # process dataset
        dataset = self._build_dataset(dataset, self.str2id, self.params, mode='train')
        return dataset

    def build_eval_dataset(self):
        dataset = self._create_dataset_from_files((self.eval_query_files, self.eval_doc_files, self.eval_label_files))
        # process dataset
        dataset = self._build_dataset(dataset, self.str2id, self.params, mode='eval')
        return dataset

    def build_predict_dataset(self):
        dataset = self._create_dataset_from_files((self.predict_query_files, self.predict_doc_files, None))
        # process dataset
        dataset = self._build_predict_dataset(dataset, self.str2id, self.params)
        return dataset
