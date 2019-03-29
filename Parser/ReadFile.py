import os
import time
import multiprocessing
import pickle

import numpy

from Parser.Indexer import Indexer
from Parser.Parser import Parser
from Parser.Ranker import Ranker

########################################################################################################################
# Relevant Data Structures:                                                                                            #
#                                                                                                                      #
# (1) vocabulary: <key: course_id, val: similar courses> ---> loaded from dict_sim.txt                                 #
# (2) hash_exc: <key: exam_id_exc_id, val: contents of the question> --->  built in runtime and saved to dict_exc.txt  #
# (3) hash_exc_in_exams: <key: course_id, val: [exc_id,year,moed]>                                                     #
########################################################################################################################


class ReadFile:
    files_list = []
    complete_list = []

    hash_stopwords = {}
    hash_punc = {}
    hash_words = {}

    vocabulary = {}
    voc_sim_exams = {}
    voc_exc_in_exam = {}
    voc_words_in_exc = {}
    voc_dict_ranks = {}

    dict_exc_rank = {}
    hash_results = {}

    data_path = ""
    post_path = ""
    abs_stopword_path = ""

    exc_counter = 0
    number_of_files = 0
    f_counter = 0
    N = 0

    controller = None
    indexer = None
    ranker = None

    # constructor #

    def __init__(self):
        self.set_paths()  # init paths for data files
        self.indexer = Indexer(self.post_path)  # init Indexer

    def set_paths(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(project_dir, 'resources\\Text_Cleaned')
        post_path = os.path.join(project_dir, 'outputs\\posting')
        str_path_stopwords = 'resources\\stopwords.txt'  # sets stop word dictionary
        self.data_path = data_path
        self.post_path = post_path
        self.abs_stopword_path = os.path.join(project_dir, str_path_stopwords)

    # function sets stopwords #

    def set_stopwords(self, file_path):
        with open(file_path, 'r', encoding="utf8") as file:
            data = file.read().replace('\n', ' ')
        list_stopwords = data.split()
        for word in list_stopwords:
            self.hash_stopwords[word] = ""
        del list_stopwords

    # function sets punctuation keywords #

    def set_puncwords(self):
        list_punc = {' ', '', "\"", '\"', "\\", '\\\\', ',', '"', '|' '?', '-', '--', '_', '*', '"', '`', ':', '.', '/',
                     ';', "'", '[', ']', '(', ')', '{', "}", '<', '>', '~', '%', '^', '?', '&', '!', "=", '+', "#"}
        for word in list_punc:
            self.hash_punc[word] = ""
        del list_punc

    # function inits stopwords, punctuation and Indexer class #

    def init_data(self):
        self.set_stopwords(self.abs_stopword_path)  # sets stop word dictionary
        self.set_puncwords()  # sets punctuation vocabulary

    # main function that runs over the given corpus and calls the Parser Class #

    def start_evaluating_exam(self):
        global f_counter
        f_counter = 1
        self.init_data()
        files_list = self.set_file_list()
        for file in files_list:
            self.parse_file(file)
            f_counter += 1

    # function sets path list of files for the process pool jobs #

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        return files_list

    # main function initializing folders saving data and sends exams to the parser #

    def parse_file(self, file_path):
        global f_counter
        p_name = "#NUM_" + str(f_counter)
        p = Parser(self.hash_stopwords, self.hash_punc)
        self.get_exam_from_file(file_path, p)
        with open(self.post_path + '/temp_hash_objects/file_hash_' + p_name + '.pkl', 'wb') as output:
            pickle.dump(p.hash_temp_words, output, pickle.HIGHEST_PROTOCOL)
        self.indexer.write_dict_exc(p.hash_exc)
        self.indexer.write_dict_exc_in_exams(p.hash_exc_in_exams)

    # main function extracting exams from given strings and calls the start_parse(exam) method #

    def get_exam_from_file(self, file_path, parser_object):
        l_exam_id = file_path.split('\\')
        s_exam_id = l_exam_id[len(l_exam_id)-1][:-4]
        skip_one = 0
        with open(file_path, 'r', encoding="utf8") as file:
            exc_counter = 0
            exc_counter2 = 0
            data = file.read()
            data_list = data.split("<Q>")
            del data
            for exc in data_list:
                exc_counter2 += 1
                if skip_one == 1:
                    exc_counter += 1
                    parser_object.start_parse(exc, s_exam_id)  # loops over exercises
                    self.N += 1
                else:
                    skip_one = 1
        del data_list

    def set_file_list_path(self, path):
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        return files_list

    # function merges the vocabulary #

    def load_main_vocabulary(self):
        file_list = self.set_file_list_path(self.post_path + '/temp_hash_objects')
        # self.N = self.vocabulary['N']
        for doc in file_list:
            with open(doc, 'rb') as data:
                hash_terms = pickle.load(data)
                for term, data in hash_terms.items():
                    if term not in self.vocabulary:
                        self.vocabulary[term] = data
                    else:
                        self.vocabulary[term]['df'] = self.vocabulary[term]['df'] + data['df']
                        for d_id in data['hash_exc']:
                            self.vocabulary[term]['hash_exc'].update({d_id: data['hash_exc'][d_id]})
        # self.indexer.write_dict_words(hash_words)
        # print("merged")

    # function loads the exams vocabulary #

    def load_similar_exams(self):
        dict_sim_path = self.post_path + '\\dict_sim.txt'
        with open(dict_sim_path, 'r', encoding="utf8") as file:
            l_exams = [line.strip() for line in file]
            file.close()
        for line in l_exams:
            l_info = line.split('|')
            curr_exam = l_info[0]
            l_sims = l_info[1].split(',')
            self.voc_sim_exams[curr_exam] = l_sims

    # function loads the exams vocabulary #

    def load_exc_in_exams(self):
        dict_sim_path = self.post_path + '\\dict_exc_in_exams.txt'
        with open(dict_sim_path, 'r', encoding="utf8") as file:
            l_exams = [line.strip() for line in file]
            file.close()
        for line in l_exams:
            l_info = line.split('|')
            curr_exam = l_info[0]
            if curr_exam not in self.voc_exc_in_exam:
                self.voc_exc_in_exam[curr_exam] = []
            l_sims = l_info[1].split(',')
            size = len(l_sims)
            for i in range(0, size, 2):
                if len(l_sims[i]) > 1:
                    if '>' in l_sims[i]:
                        l_split = l_sims[i].split('>')
                        self.voc_exc_in_exam[curr_exam].append(l_split[1])
                    else:
                        self.voc_exc_in_exam[curr_exam].append(l_sims[i])

    def load_words_in_exams(self):
        dict_sim_path = self.post_path + '\\dict_exc.txt'
        with open(dict_sim_path, 'r', encoding="utf8") as file:
            l_exams = [line.strip() for line in file]
            file.close()
        for line in l_exams:
            l_info = line.split('|')
            curr_exam = l_info[0]
            if curr_exam not in self.voc_words_in_exc:
                self.voc_words_in_exc[curr_exam] = {}
            l_sims = l_info[1].split(',')
            size = len(l_sims)
            for i in range(0, size):
                self.voc_words_in_exc[curr_exam][l_sims[i]] = ''

    def load_dict_rank(self):
        dict_sim_path = self.post_path + '\\dict_ranks.txt'
        with open(dict_sim_path, 'r', encoding="utf8") as file:
            l_exams = [line.strip() for line in file]
            file.close()
        for line in l_exams:
            l_info = line.split('|')
            curr_exam = l_info[0]
            if curr_exam not in self.voc_words_in_exc:
                self.voc_dict_ranks[curr_exam] = {}
            l_sims = l_info[1].split('>')
            size = len(l_sims)
            for i in range(0, size):
                tuple = l_sims[i].split(',')
                exc_id = tuple[0]
                rank = tuple[1]
                self.voc_dict_ranks[curr_exam][exc_id] = rank

    def filter_results(self):
        for this_course, tuple_data in self.dict_exc_rank.items():
            tuple_results = sorted(tuple_data, key=lambda kv: kv[1], reverse=True)
            # if len(tuple_results) > 20:
            #     tuple_results = tuple_results[0:20]
            self.hash_results[this_course] = tuple_results

    def rank(self):
        self.load_similar_exams()
        self.load_exc_in_exams()
        self.load_words_in_exams()
        try:
            self.ranker = Ranker(self.vocabulary)
            for this_course, l_exams in self.voc_exc_in_exam.items():  # loop runs over all the courses
                self.dict_exc_rank[this_course] = []
                for this_exercise in l_exams:  # loops runs over all the exercises in this course
                    if len(self.voc_words_in_exc[this_exercise]) > 1:
                        self.ranker.set_curr_exam(self.voc_words_in_exc[this_exercise], this_exercise)
                l_sim = self.voc_sim_exams[this_course]
                this_rank = 0
                for other_course in l_sim:  # loops over all other exercises
                    for other_exercise in self.voc_exc_in_exam[other_course]:
                        try:
                            if len(self.voc_words_in_exc[other_exercise]) > 1:
                                this_rank = self.ranker.rank(self.voc_words_in_exc[other_exercise], other_exercise)
                            self.dict_exc_rank[this_course].append([other_exercise, float("{0:.2f}".format(this_rank))])
                        except TypeError:
                            a = 0
                # self.ranker.reset()
            # print('done')
            self.filter_results()
            self.indexer.write_dict_ranks(self.hash_results)
        except KeyError:
            print('no similar courses found')
