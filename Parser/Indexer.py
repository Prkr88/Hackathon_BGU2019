import os
import copy
import shutil
import multiprocessing
import pickle

########################################################################################################################
# Indexer Class                                                                                                        #
#                                                                                                                      #
# writes dictionary of exercises and dictionary of exams to txt files                                                  #
#                                                                                                                      #
########################################################################################################################


class Indexer:

    # constructor #

    def __init__(self, user_path):
        self.posting_path = user_path
        self.file_path0 = self.posting_path + '\\dict_exc.txt'
        self.file_path1 = self.posting_path + '\\dict_exc_in_exams.txt'
        self.file_path2 = self.posting_path + '\\dict_words.txt'
        self.file_path3 = self.posting_path + '\\dict_ranks.txt'
        # self.init_folders()

    # main function writes dictionaries to the temporary posting files #

    def write_dict_exc(self, hash_exc):
        with open(self.file_path0, 'a', encoding='utf-8') as curr_file:
            try:
                for ikey, ival in hash_exc.items():
                    words = ''
                    for jkey, jval in ival.items():
                            words += jkey + ','
                    words = words[:-1]
                    str_data = ikey + '|' + words + '\n'
                    curr_file.write(str_data)
            except Exception:
                a = 0
        curr_file.close()

    def write_dict_exc_in_exams(self, hash_exc_in_exams):
        with open(self.file_path1, 'a', encoding='utf-8') as curr_file:
            try:
                for ikey, ival in hash_exc_in_exams.items():
                    lists = ''
                    for element in ival:
                        lists += ','.join(map(str, element)) + '>'
                    lists = lists[:-1]
                    str_data = ikey + '|' + lists + '\n'
                    curr_file.write(str_data)
            except Exception:
                a = 0
        curr_file.close()

    def write_dict_words(self, hash_voc):
        with open(self.file_path2, 'a', encoding='utf-8') as curr_file:
            try:
                for ikey, ival in hash_voc.items():
                    lists = ''
                    for element in ival:
                        lists += ','.join(map(str, element)) + '>'
                    lists = lists[:-1]
                    str_data = ikey + '|' + lists + '\n'
                    curr_file.write(str_data)
            except Exception:
                a = 0
        curr_file.close()

    def write_dict_ranks(self, hash_res):
        with open(self.file_path3, 'a', encoding='utf-8') as curr_file:
            try:
                for ikey, ival in hash_res.items():
                    lists = ''
                    for element in ival:
                        lists += ','.join(map(str, element)) + '>'
                    lists = lists[:-1]
                    str_data = ikey + '|' + lists + '\n'
                    curr_file.write(str_data)
            except Exception:
                a = 0
        curr_file.close()

    def init_folders(self):
        open(self.file_path0, 'w').close()
        open(self.file_path1, 'w').close()
        open(self.file_path2, 'w').close()
        open(self.file_path3, 'w').close()

    def reset_posting_files(self):
        if self.posting_path is not None:
            if os.path.exists(self.posting_path):
                shutil.rmtree(self.posting_path)
