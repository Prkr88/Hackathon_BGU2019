'''
Main file to control program sequance.

Flow:
1. Create data from pdfs supplied
2. Map pdfs to separate questions
3. Index Data
'''

from mainUI import Ui_Prepary
from Parser.ReadFile import ReadFile
from Parser.Parser import Parser
from Parser.Indexer import Indexer
from Parser.Ranker import Ranker

if __name__ == '__main__':
    rf = ReadFile()
    rf.start_evaluating_exam()
    rf.load_main_vocabulary()
    rf.rank()
    rf.load_dict_rank()
    Ui_Prepary = Ui_Prepary()
    Ui_Prepary.show_gui()
    # TODO
    # call DataCreator main function
    # call ParaCut main function
    # call EngineIndexer Main Function


