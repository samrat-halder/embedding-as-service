from typing import List, Dict, Set, Optional, Union, Any

from models import Embedding
from utils import tokenizer
from tqdm import tqdm
import numpy as np
import os


class Embeddings(object):

    EMBEDDING_MODELS: List[Embedding] = [
        Embedding(name=u'twitter_100',
                  dimensions=100,
                  corpus_size='27B',
                  vocabulary_size='1.2M',
                  download_url='https://www.dropbox.com/s/q2wof83a0yq7q74/glove.twitter.27B.100d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Twitter 2B Tweets',
                  language='en'),
        Embedding(name=u'twitter_200',
                  dimensions=200,
                  corpus_size='27B',
                  vocabulary_size='1.2M',
                  download_url='https://www.dropbox.com/s/hfw00m77ibz24y5/glove.twitter.27B.200d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Twitter 2B Tweets',
                  language='en'),
        Embedding(name=u'twitter_25',
                  dimensions=25,
                  corpus_size='27B',
                  vocabulary_size='1.2M',
                  download_url='https://www.dropbox.com/s/jx97sz8skdp276k/glove.twitter.27B.25d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Twitter 2B Tweets',
                  language='en'),

        Embedding(name=u'twitter_50',
                  dimensions=50,
                  corpus_size='27B',
                  vocabulary_size='1.2M',
                  download_url='https://www.dropbox.com/s/9mutj8syz3q20e3/glove.twitter.27B.50d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Twitter 2B Tweets',
                  language='en'),
        Embedding(name=u'wiki_100',
                  dimensions=100,
                  corpus_size='6B',
                  vocabulary_size='0.4M',
                  download_url='https://www.dropbox.com/s/g0inzrsy1ds3u63/glove.6B.100d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Wikipedia+Gigaword',
                  language='en'),
        Embedding(name=u'wiki_200',
                  dimensions=200,
                  corpus_size='6B',
                  vocabulary_size='0.4M',
                  download_url='https://www.dropbox.com/s/pmj2ycd882qkae5/glove.6B.200d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Wikipedia+Gigaword',
                  language='en'),

        Embedding(name=u'wiki_300',
                  dimensions=300,
                  corpus_size='6B',
                  vocabulary_size='0.4M',
                  download_url='https://www.dropbox.com/s/9jbbk99p0d0n1bw/glove.6B.300d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Wikipedia+Gigaword',
                  language='en'),

        Embedding(name=u'wiki_50',
                  dimensions=50,
                  corpus_size='6B',
                  vocabulary_size='0.4M',
                  download_url='https://www.dropbox.com/s/o3axsz1j47043si/glove.6B.50d.txt.zip?dl=1',
                  format='zip',
                  architecture='glove',
                  trained_data='Wikipedia+Gigaword',
                  language='en'),

        Embedding(name=u'crawl_42B_300',
                  dimensions=300,
                  corpus_size='42B',
                  vocabulary_size='1.9M',
                  download_url='http://nlp.stanford.edu/data/glove.42B.300d.zip',
                  format='zip',
                  architecture='glove',
                  trained_data='Common Crawl (42B tokens)',
                  language='en'),

        Embedding(name=u'crawl_840B_300',
                  dimensions=300,
                  corpus_size='840B',
                  vocabulary_size='2.2M',
                  download_url='http://nlp.stanford.edu/data/glove.840B.300d.zip',
                  format='zip',
                  architecture='glove',
                  trained_data='Common Crawl (840B tokens)',
                  language='en')

    ]

    EMBEDDING_MODELS: Dict[str, Embedding] = {embedding.name: embedding for embedding in EMBEDDING_MODELS}

    word_vectors: Dict[Any, Any] = {}
    model: str

    @classmethod
    def _tokens(cls, text: str) -> List[str]:
        return tokenizer(text, cls.EMBEDDING_MODELS[cls.model].language)

    @classmethod
    def load_model(cls, model: str, model_path: str):
        try:
            model_file = [f for f in os.listdir(model_path) if os.path.isfile(os.path.join(model_path, f))]
            f = open(os.path.join(model_path, model_file[0]), 'r')
            for line in tqdm(f):
                split_line = line.split()
                word = split_line[0]
                cls.word_vectors[word] = np.array([float(val) for val in split_line[1:]])
            print("Model loaded Successfully !")
            cls.model = model
            return cls
        except Exception as e:
            print('Error loading Model, ', str(e))
        return cls

    @classmethod
    def encode(cls, text: str, pooling: str = 'mean', **kwargs) -> np.array:
        result = np.zeros(cls.EMBEDDING_MODELS[cls.model].dimensions, dtype="float32")
        tokens = cls._tokens(text)

        vectors = np.array([cls.word_vectors[token] for token in tokens if token in cls.word_vectors.keys()])

        if pooling == 'mean':
            result = np.mean(vectors, axis=0)

        elif pooling == 'max':
            result = np.max(vectors, axis=0)

        elif pooling == 'sum':
            result = np.sum(vectors, axis=0)

        elif pooling == 'tf-idf-sum':
            if not kwargs.get('tfidf_dict'):
                print('Must provide tfidf dict')
                return result

            tfidf_dict = kwargs.get('tfidf_dict')
            weighted_vectors = np.array([tfidf_dict.get(token) * cls.word_vectors.get(token)
                                         for token in tokens if token in cls.word_vectors.keys()
                                         and token in tfidf_dict])
            result = np.mean(weighted_vectors, axis=0)
        else:
            print(f'Given pooling method "{pooling}" not implemented in "{cls.embedding}"')
        return result

