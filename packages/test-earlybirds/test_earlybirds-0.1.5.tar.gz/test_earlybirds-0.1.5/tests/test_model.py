import operator
import os
import tempfile
import filecmp
from scipy.sparse import csr_matrix

from test_earlybirds.model import KNN


def test_get_neighbors():
    knn = KNN()
    knn.train_set = (4, 4)
    knn.train_set = csr_matrix(
        [[0.9, 1.0, 1.0, 0.0],
         [0.0, 0.2, 1.0, 1.0],
         [1.0, 0.5, 1.0, 0.0],
         [1.0, 1.0, 0.0, 0.0]]
    )

    assert sorted(knn.get_neighbors(2, 0)[0]) == [2, 3]


def test_get_movies():
    knn = KNN()

    knn.train_set = csr_matrix((4, 7))
    knn.train_set[0, 1] = 5.0
    knn.train_set[0, 2] = 2.5
    knn.train_set[0, 4] = 4.0

    knn.train_set[1, 1] = 3.0
    knn.train_set[1, 2] = 3.0
    knn.train_set[1, 3] = 5.0
    knn.train_set[1, 4] = 5.0
    knn.train_set[1, 5] = 2.5

    knn.train_set[2, 0] = 1.0
    knn.train_set[2, 1] = 5.0
    knn.train_set[2, 2] = 1.0
    knn.train_set[2, 3] = 5.0
    knn.train_set[2, 4] = 4.0
    knn.train_set[2, 5] = 4.5

    knn.train_set[3, 0] = 0.5
    knn.train_set[3, 1] = 5.0
    knn.train_set[3, 2] = 0.0
    knn.train_set[3, 3] = 5.0
    knn.train_set[3, 4] = 1.0
    knn.train_set[3, 5] = 5.0
    s_movies = knn.get_movies([2, 3], [0.8, 0.6], 0)
    assert [i[0] for i in sorted(s_movies, key=operator.itemgetter(1), reverse=True)] == [3, 5, 0]


def test_fill_evaluation():
    knn = KNN()
    suggested_movies_1 = {
        0: 5.0,
        1: 5.0,
        2: 3.0,
        3: 1.0,
    }
    suggested_movies_2 = {
        5: 3.0,
        6: 2.0,
        7: 10.0,
        8: 5.0,
    }
    knn.evaluation_set = {
        1: [[110, 0.0], [1968, 0.0], [4878, 0.0], [54503, 0.0], [91542, 0.0]],
        2: [[79, 0.0], [141, 0.0], [260, 10.0], [1210, 0.0]],
    }
    knn.movies_to_id = {
        110: 0,
        1968: 1,
        4878: 2,
        54503: 3,
        91542: 4,
        79: 5,
        141: 6,
        260: 7,
        1210: 8,
    }
    knn.id_to_movies = {
        0: 110,
        1: 1968,
        2: 4878,
        3: 64503,
        4: 91542,
        5: 79,
        6: 141,
        7: 260,
        8: 1210,
    }

    expected = {
        1: [[110, 5.0], [1968, 5.0], [4878, 3.0], [54503, 1.0], [91542, 0.0]],
        2: [[79, 3.0], [141, 2.0], [260, 10.0], [1210, 5.0]],
    }
    knn.fill_evaluation_attribute(1, suggested_movies_1)
    knn.fill_evaluation_attribute(2, suggested_movies_2)
    assert knn.evaluation_set == expected


def test_write_csv():
    folder = tempfile.mkdtemp()
    knn = KNN()
    knn.output_path = folder + '/output.csv'
    knn.evaluation_set = {
        1: [[110, 5.056565], [1968, 5.0], [4878, 3.0], [54503, 1.056464464], [91542, 0.3545465]],
        2: [[79, 3.08987], [141, 2.0], [260, 10.066566], [1210, 5.0]],
    }
    knn.write_csv()
    assert filecmp.cmp(knn.output_path,  os.getcwd() + '/resource/test_write_csv.csv')
