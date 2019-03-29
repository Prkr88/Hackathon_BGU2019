import copy
from random import randint

########################################################################################################################
# Parser Class                                                                                                         #
#                                                                                                                      #
# (1) analyzes exercise by exercise                                                                                    #
# (2) creates hash_exc: <key: exam_id_exc_id, val: { key: word | val: null } }>                                        #
# note: nested dict used for faster searching                                                                          #
# (3) creates hash_exc_in_exams: <key: course_id, val: [exc_id,year,moed]>                                             #
########################################################################################################################


class Parser:

    # initializes strings

    s_exc = ""
    s_exc_id = ""
    s_txt = ""
    s_course_id = ""
    s_year = ""
    s_moed = ""

    # initializes dictionaries

    hash_exc = {}  # hash dictionary of exercises->words
    hash_stopwords = {}  # hash dictionary of stopwords
    hash_punc = {}  # hash dictionary of punctuations
    hash_exc_in_exams = {}  # hash dictionary of courses->exercises
    hash_temp_words = {}

    # initializes lists

    list_tokens = []  # list of the exams tokens

    # global vars

    global_line_counter = 0  # global line counter in file
    line_in_exam_counter = 0  # global line counter in exam
    word_in_line_counter = 0  # global line word counter in lines
    exam_counter = 0  # counts exams in file
    ord_heb_to_eng = 1423

    # constructor #

    def __init__(self, hash_stopwords, hash_punc):
        self.hash_exc = {}
        self.hash_exc_in_exams = {}
        self.hash_temp_words = {}
        self.hash_stopwords = hash_stopwords
        self.hash_punc = hash_punc

    # main function receives a token term and inserts it appropriately to the set of hash terms #
    # hash_exc FORMAT: { key: exercise_id |  #

    def term_filter(self, other_term):
        try:
            if other_term not in self.hash_temp_words:
                nested_hash = ({'df': 1, 'hash_exc': {self.s_exc_id: {'tf_d': 1}}})
                self.hash_temp_words[other_term] = nested_hash
            else:
                self.hash_temp_words[other_term]['hash_exc'][self.s_exc_id]['tf_d'] += 1
            if other_term not in self.hash_exc[self.s_exc_id]:
                self.hash_exc[self.s_exc_id][other_term] = ""
        except Exception:
            a = 0

    # main function filters regular terms of unnecessary punctuations #

    def cut_term(self, term):
        try:
            if term != '':
                size = len(term) - 1
                last = term[size]
                first = term[0]
                while term != '' and (size > 0 and last != '') and (last in self.hash_punc or '\"' in last or "\\\\" in last):
                    term = term[:-1]
                    size -= 1
                    if size > 0:
                        last = term[size]
                while term != '' and (size > 0 and first != '') and (first in self.hash_punc or '\"' in first or "\\\\" in first):
                    term = term[1:]
                    size -= 1
                    if size > 0:
                        first = term[0]
                if term != '' and len(term) > 1 and self.clean_term(term) and self.valid_range(term):
                    self.term_filter(term)
        except Exception:
            print("MotherFucking Term : " + term)

    # function checks if the given term contains a number #

    def contains_number(self, term):
        all_numbers = any(char.isdigit() for char in term)
        return all_numbers

    # function formats asterisks that are replacing '/n' #

    def ignore_asterisk_back_mode(self, index):
        index -= 1
        while index > 0 and self.list_tokens[index] == '*':
            index -= 1
        return index

    # function formats asterisks that are replacing '/n' #

    def ignore_asterisk_front_mode(self, index):
        index += 1
        while index < len(self.list_tokens) - 2 and self.list_tokens[index] == '*':
            index += 1
        return index

    # function checks if the given term contains hebrew #

    def contains_heb(self, term):
        return any(self.valid_range(char) for char in term)

    # function checks if the given exam contains moed and adds otherwise #

    def contains_moed(self, term):
        if term[-1:].isdigit():
            term = term + 'A'
        return term

    # function validates hebrew unicode of the term #

    def valid_range(self, term):
        try:
            ch = ord(term[0])
            return 1488 <= ch <= 1514  # alef = 1488, taf = 1514
        except Exception:
            return False

    # function checks if the term is clean #

    def clean_term(self, term):
        try:
            if term != '' and 'NUM' not in term and 'Q' not in term \
                    and term not in self.hash_stopwords and term not in self.hash_punc:
                return True
            else:
                return False
        except Exception:
            return

    # function checks converts hebrew to english #

    def convert_heb_to_eng(self, s_exam_id):
        i = 0
        temp = s_exam_id
        if 'מועד' in temp:
            temp = temp.replace('מועד','')
        for ch in temp:
            if 1488 <= ord(ch) <= 1514:
                temp = temp[:i] + chr(ord(ch) - self.ord_heb_to_eng) + temp[i + 1:]
            i += 1
        temp = temp.replace(' ', '')
        return temp

    # main function of the parsing sequence. receives a long string and divides it to tokens #

    def start_parse(self, s_exc, s_exam_id):
        if s_exc:
            self.s_txt = s_exc
        s_exam_id = self.contains_moed(s_exam_id)
        if self.contains_heb(s_exam_id):
            s_exam_id = self.convert_heb_to_eng(s_exam_id)
        self.exam_counter = (self.s_txt.split("</NUM>", 1)[0]).split("<NUM>")[1].strip()
        self.s_course_id = s_exam_id.split('.')[0]
        self.s_year = s_exam_id.split('.')[1][:-1]
        if self.s_year == '':
            self.s_year = '2019'
        self.s_moed = s_exam_id.split('.')[1][-1:]
        self.s_exc_id = self.s_course_id + '.' + self.s_year + self.s_moed + '_' + self.exam_counter
        self.hash_exc[self.s_exc_id] = {}
        if self.s_course_id in self.hash_exc_in_exams:
            self.hash_exc_in_exams[self.s_course_id].append([self.s_exc_id, self.s_year, self.s_moed])
        else:
            self.hash_exc_in_exams[self.s_course_id] = [[self.s_exc_id, self.s_year, self.s_moed]]
        self.s_txt = self.s_txt.replace('*', '')
        self.s_txt = self.s_txt.replace('\n', ' * ')
        self.list_tokens = self.s_txt.split()
        index = 0
        self.list_tokens.append('עקומות')
        for term in self.list_tokens:
            try:
                if term != '' and not self.contains_number(term):
                    if term == '*':
                        self.line_in_exam_counter += 1
                        self.global_line_counter += 1
                        self.word_in_line_counter = 0
                    else:
                        if ',' in term:
                            term = term.replace(',', '')
                            self.list_tokens[index] = term
                        if self.clean_term(term):
                            self.cut_term(term)
                            self.word_in_line_counter += 1
                index += 1
            except Exception:
                a = 0
