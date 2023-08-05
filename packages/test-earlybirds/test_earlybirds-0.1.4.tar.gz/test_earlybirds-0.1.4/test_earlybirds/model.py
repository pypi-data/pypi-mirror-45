from scipy.sparse import csr_matrix
from scipy.sparse import coo_matrix
from scipy.spatial.distance import pdist
from tqdm import tqdm

import logging
import numpy as np


class KNN:
    def __init__(self, output_path="./result.csv", k=5, user_limit=20):
        self.k = k
        # the train_set attribute is a lil matrix
        self.train_set = {}
        self.evaluation_set = {}
        self.id_to_movies = {}
        self.movies_to_id = {}
        self.users_to_id = {}
        self.output_path = output_path
        self.user_limit = user_limit

    def load_dataset(self, csv_train_path, csv_evaluation_path):
        logging.info('load dataset started ...')
        self.load_train_set(csv_train_path)
        self.load_evaluation_set(csv_evaluation_path)
        logging.info('load dataset started ...')

    def load_train_set(self, csv_train_set):
        logging.info('open csv file and parse each row')
        with open(csv_train_set, 'r') as csv_file:
            next(csv_file)
            u_idx = 0
            m_idx = 0
            t_row, t_col, t_data = [], [], []

            for idx, row in enumerate(tqdm(csv_file)):
                csv_row = row.split(',')
                f_rating = float(csv_row[2])
                if f_rating > 1.5:
                    u_row_0 = int(csv_row[0])
                    m_row_1 = int(csv_row[1])
                    t_data.append(f_rating)
                    if u_row_0 not in self.users_to_id.keys():
                        self.users_to_id[u_row_0] = u_idx
                        u_idx += 1
                    if m_row_1 not in self.id_to_movies.items():
                        self.id_to_movies[m_idx] = m_row_1
                    if m_row_1 not in self.movies_to_id.keys():
                        self.movies_to_id[m_row_1] = m_idx
                        m_idx += 1
                    t_row.append(self.users_to_id[u_row_0])
                    t_col.append(self.movies_to_id[m_row_1])
        logging.info('create and fill matrix ...')
        self.train_set = coo_matrix((t_data, (t_row, t_col))).tocsc()
        logging.info('remove film with a small frequency ...')
        self.remove_unfrequented_movies()
        self.train_set = self.train_set.tocsr()

    def remove_unfrequented_movies(self):
        for c_i in tqdm(range(self.train_set.get_shape()[1])):
            if self.train_set.getcol(0).count_nonzero() < 1000:
                self.train_set[:, c_i] = 0

    def load_evaluation_set(self, csv_eval_set):
        with open(csv_eval_set, 'r') as csv_file:
            next(csv_file)

            for row in csv_file:
                row = row.rstrip('\n')
                a_row = row.split(',')
                int_a_row = int(a_row[0])

                if int_a_row not in self.evaluation_set.keys():
                    self.evaluation_set[int_a_row] = []
                    if len(self.evaluation_set.keys()) > self.user_limit:
                        del self.evaluation_set[int_a_row]
                        break
                self.evaluation_set[int_a_row].append((int(a_row[1]), 0.0))

    def get_neighbors(self, k, c_user_index):
        """
        get the most common k neighbors for a given user
        :param k: number of neighbors to return
        :param c_user_index: index for a given user
        :return: list of most common neighbors
        """
        logging.info('get neighbors step started ...')
        n_list = []
        n_sim_list = []

        logging.info('browse each user and retrieve the most closest ...')
        self.train_set = self.train_set.tocsr()
        c_u_row = self.train_set[c_user_index]
        for i_row, row in tqdm(enumerate(self.train_set)):
            if i_row != c_user_index:
                sim = 1 - pdist(np.array([c_u_row.toarray()[0], row.toarray()[0]]), 'cosine')[0]
                # keep only the K closest users
                if len(n_list) < k:
                    n_list.append(i_row)
                    n_sim_list.append(sim)
                # remove user the least close user in list of size k if the current user is more close
                elif sim > min(n_sim_list):
                    min_idx = n_sim_list.index(min(n_sim_list))
                    n_list[min_idx] = i_row
                    n_sim_list[min_idx] = sim
        logging.info('get neighbors is finished ...')
        return n_list, n_sim_list

    def get_movies(self, neighbors, neighbors_sim, c_user_index):
        """
        this function is used to rank the suggested films according to a user in his k closest users
        :param neighbors: the list of the k closest users a given user
        :param neighbors_sim: the cosine similarity for each k closest user, the order must be the same than the
        neighbors list
        :param c_user_index: the index of a given user
        :return: a sorted list of suggested movies (the most suggested to the worst suggested)
        """
        logging.info('get movies step started ...')
        # get mean and initialize movie prediction matrix
        mean_c_user = self.mean_row(c_user_index)
        m_prediction_matrix = csr_matrix((1, self.train_set.get_shape()[1]))

        # for each neighbors we calculate for each item a part of the prediction computation
        logging.info('browsing each closest users')
        for s_u_i, s_u in tqdm(enumerate(neighbors_sim)):
            c_row = (self.train_set.getrow(neighbors[s_u_i]).tocsr() * s_u)
            c_row.data -= self.mean_row(neighbors[s_u_i])
            m_prediction_matrix = (m_prediction_matrix.tocsr() + c_row.tocsr())
        # then we complete the computation using the mean of rating of the user and the sum of all neighbors
        # similarity value
        logging.info('finishing the prediction computation')
        m_prediction_matrix += (m_prediction_matrix.tocsr() * (1 / sum(neighbors_sim)))
        m_prediction_matrix.data += mean_c_user

        # we sorted the result according to the probability of the prediction of each movie
        logging.info('sort and return the movies suggested')
        ns_movies_index = [m for m in m_prediction_matrix[0, :].indices
                           if m not in set(self.train_set[c_user_index, :].indices)]
        return {i for i in {(i, m_prediction_matrix[0, i]) for i in ns_movies_index}}

    def fill_evaluation_attribute(self, c_user_index, suggested_movies):
        """
        fill the predicted rating of evaluation_set attributes
        :param c_user_index: given user index
        :param suggested_movies: the parameter with suggested movies for a given user and the rating given 
        for each of them
        """
        logging.info('fill evaluation attribute step started ...')
        for m in self.evaluation_set[c_user_index]:
            if self.movies_to_id[m[0]] in suggested_movies:
                m[1] = suggested_movies[self.movies_to_id[m[0]]]

        logging.info('fill evaluation attribute step finished ...')

    def mean_row(self, user_index):
        """
        get the mean of the rating of a given user
        :param user_index: the index of a given user in the train set attribute
        """
        return self.train_set.getrow(user_index).sum() / self.train_set.getrow(user_index).count_nonzero()

    def write_csv(self):
        logging.info('write csv attribute step started ...')
        with open(self.output_path, 'w') as f:
            f.write('userId,movieId,rating\n')
            for u in sorted(self.evaluation_set.keys()):
                for m in self.evaluation_set[u]:
                    f.write(str(u) + ',' + str(m[0]) + ',' + str(round(m[1], 3)) + '\n')
        logging.info('write csv attribute step finished ...')

    def execute(self):
        for e in self.evaluation_set.keys():
            u_id = self.users_to_id[e]
            neighbors_list, neighbors_sim_list = self.get_neighbors(self.k, u_id)
            suggested_movies = self.get_movies(neighbors_list, neighbors_sim_list, e)
            self.fill_evaluation_attribute(e, suggested_movies)
        self.write_csv()
