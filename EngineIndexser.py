# from wand.image import Image as Img
import os

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from Parser.ReadFile import ReadFile
from Parser.Ranker import Ranker

'''
#                 ######    ######          
#                 #::::#    #::::#          
#                 #::::#    #::::#          
#            ######::::######::::######     
#            #::::::::::::::::::::::::#     ██╗  ██╗ █████╗ ███████╗██╗  ██╗████████╗ █████╗  ██████╗         ██████╗ ██╗███████╗ ██████╗██╗   ██╗██╗████████╗███████╗
#            ######::::######::::######     ██║  ██║██╔══██╗██╔════╝██║  ██║╚══██╔══╝██╔══██╗██╔════╝         ██╔══██╗██║██╔════╝██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
#                 #::::#    #::::#          ███████║███████║███████╗███████║   ██║   ███████║██║  ███╗        ██████╔╝██║███████╗██║     ██║   ██║██║   ██║   ███████╗
#                 #::::#    #::::#          ██╔══██║██╔══██║╚════██║██╔══██║   ██║   ██╔══██║██║   ██║        ██╔══██╗██║╚════██║██║     ██║   ██║██║   ██║   ╚════██║
#            ######::::######::::######     ██║  ██║██║  ██║███████║██║  ██║   ██║   ██║  ██║╚██████╔╝        ██████╔╝██║███████║╚██████╗╚██████╔╝██║   ██║   ███████║
#            #::::::::::::::::::::::::#     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝         ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝
#            ######::::######::::######     
#                 #::::#    #::::#             
#                 #::::#    #::::#             
#                 ######    ######
'''


def convert(self):
    i=1
    pages = convert_from_path('pdfs/sample.pdf', 500)

    for page in pages:
        page.save('outputs/page_'+str(i)+'.png', 'PNG')
        i+=1

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    # with Img(filename='file_name.pdf', resolution=300) as img:
    #     img.compression_quality = 99
    #     img.save(filename='image_name.jpg')
    for j in range(1,i):
        text = pytesseract.image_to_string(Image.open('outputs/page_'+str(j)+'.png'),lang='heb')
        with open("texts/text_"+str(j)+".txt", "w", encoding="utf-8") as out:
            out.write(text)


if __name__ == '__main__':
    rf = ReadFile()
    # rf.start_evaluating_exam()
    s_course_id = '20119571'
    ranker = Ranker()
    rf.start(s_course_id)
    # ranker.start_rank(s_course_id)
