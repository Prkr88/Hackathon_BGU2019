from numpy import sqrt
from numpy import log2


class Ranker:

    h_other_words = {}
    h_cos_data = {}
    h_curr_exc = {}
    vocabulary = {}

    const = 1000
    i_N = 103
    sigma_w_iq = 0
    sqrt_w_iq = 0
    i_this_year = '2019'
    this_exercise = ''
    s_course_id = ''

    def __init__(self, vocabulary):
        self.hash_results = {}
        self.vocabulary = vocabulary
        # self.i_N = self.vocabulary['N']

    def set_curr_exam(self, h_curr_exc, this_exercise):
        try:
            self.this_exercise = this_exercise
            self.h_curr_exc = h_curr_exc
            for row in self.h_curr_exc.items():
                word = row[0]
                if word in self.vocabulary:
                    tf_q = self.vocabulary[word]['hash_exc'][this_exercise]['tf_d']
                    df = self.vocabulary[word]['df']
                    idf = float("{0:.2f}".format(log2((self.i_N - df + 0.5) / (df + 0.5))))
                    self.sigma_w_iq += tf_q * idf
        except Exception:
            print('takala')

    def rank(self, h_other_exc, other_exercise):
        self.sqrt_w_iq = sqrt(self.sigma_w_iq)
        sigma_w_ij = 0
        nmr = 0
        dnmr = 0
        cossim = 0
        try:
            for row in h_other_exc.items():
                word = row[0]
                if word in self.vocabulary:
                    tf_d = self.vocabulary[word]['hash_exc'][other_exercise]['tf_d']
                    df = self.vocabulary[word]['df']
                    idf = float("{0:.2f}".format(log2((self.i_N - df + 0.5) / (df + 0.5))))
                    sigma_w_ij += tf_d * idf
                    if word in self.h_curr_exc:
                        tf_q = self.vocabulary[word]['hash_exc'][self.this_exercise]['tf_d']
                        nmr += ((tf_d * idf) + (tf_q * idf)) * self.const
            if nmr == 0:
                return 0  # no similar words
            sqrt_w_ij = sqrt(sigma_w_ij)
            dnmr = self.sqrt_w_iq * sqrt_w_ij
            cossim = float("{0:.2f}".format((nmr / dnmr)))
            if cossim > 0:
                return cossim
        except Exception:
            print('takala')
