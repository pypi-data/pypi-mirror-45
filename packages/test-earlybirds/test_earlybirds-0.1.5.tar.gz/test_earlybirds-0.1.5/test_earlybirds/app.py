# -*- coding: utf-8 -*-
from test_earlybirds.model import KNN
import logging
logging.basicConfig(level=logging.INFO)


def execute(learn_path='../data/technical-test_data-scientist_ratings.csv',
            eval_path='../data/technical-test_data-scientist_evaluation_ratings.csv', output_path='../data/output.csv',
            k=5, user_limit=20):
    knn = KNN(k=k, output_path=output_path, user_limit=user_limit)
    knn.load_dataset(learn_path, eval_path)
    knn.execute()


if __name__ == '__main__':
    execute()
"""Main module."""
