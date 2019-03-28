# from wand.image import Image as Img
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


class Data_Creator():

    def __init__(self, project_path):
        self.project_path = project_path
        self.file_list = []
        self.file_png_list = []
        self.file_text_list = []

    def get_file_list(self, offset):
        local_file_list = []
        for root, dirs, files in os.walk(self.project_path + offset):
            for file in files:
                file_path = os.path.join(root, file)
                path_split = file_path.split('\\')
                dest_directory_name = path_split[-3] + '\\' + path_split[-2]
                course_id = path_split[-2].split('.')
                course_id = ''.join(course_id[-3] + course_id[-2] + course_id[-1])
                file_id = course_id + '.' + str(path_split[-1])
                local_file_list.append([file_path, file_id, dest_directory_name])
        return local_file_list

    def create_working_directories(self):
        local_file_list = self.file_list
        for file in local_file_list:
            # course_name = file[1].split('^')[0]
            # departament_and_course_id = file[1].split('^')[1]
            # concat_names = "\\" + course_name + "\\"+departament_and_course_id
            dest_dir = file[2]
            dir_name = self.project_path + "\\pngs\\" + dest_dir
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            dir_name = self.project_path + "\\texts\\" + dest_dir
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

    def convert_pdf_to_png(self):
        local_file_list = self.file_list
        for file in local_file_list:
            print(file)
            i = 1
            pages = convert_from_path(file[0], 300)
            for page in pages:
                page.save(self.project_path + "\\pngs\\" + file[2] + "\\" + file[1] + '_' + str(i) + '.png', 'PNG')
                i += 1


    def extract_text_from_pngs(self):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        # # with Img(filename='file_name.pdf', resolution=300) as img:
        # #     img.compression_quality = 99
        # #     img.save(filename='image_name.jpg')
        # for j in range(1, i):
        #     text = pytesseract.image_to_string(Image.open('outputs/page_' + str(j) + '.png'), lang='heb')
        #     with open("texts/text_" + str(j) + ".txt", "w", encoding="utf-8") as out:
        #         out.write(text)
        local_png_list = self.file_png_list
        prev_file_name = ""
        to_write = ""
        for png in local_png_list:
            file_name = png[0].split('\\')[-1].split('_')[0]
            if ".PDF" in file_name or ".pdf" in file_name:
                file_name = file_name.replace(".PDF",'')
                file_name = file_name.replace(".pdf",'')
            text = pytesseract.image_to_string(Image.open(png[0]), lang='heb')
            if (file_name == prev_file_name or prev_file_name == "") and png != local_png_list[-1]:
                to_write = to_write + text
            else:
                with open(self.project_path + "\\texts\\" + png[2] + "\\" + file_name + ".txt", "w",
                          encoding="utf-8") as out:
                    if png == local_png_list[-1]:
                        to_write = to_write + text
                    to_write = self.clean_text(to_write)
                    out.write(to_write)
                    print(file_name)
                to_write = text
            prev_file_name = file_name

    def clean_text(self,to_clean):
        list_punc = ['', "\"", '\"', "\\", '\\\\', ',', '"', '|' '?', '-', '--', '_', '*', '"', '`', ':', '.', '/',
                     ';', "'", '[', ']', '(', ')', '{', "}", '<', '>', '~', '%', '^', '?', '&', '!', "=", '+', "#"]
        format_text = []
        relevant_text = []
        q_counter = 1
        for char in list_punc:
            to_clean = to_clean.replace(char,'')
        format_text = to_clean.split("שאלה")
        format_text = format_text[1:]
        for potential_q in format_text:
            if "פתרון" not in potential_q and "הנקודות" not in potential_q:
                relevant_text.append("<Q>\n")
                relevant_text.append("<NUM>"+str(q_counter)+"</NUM>\n")
                relevant_text.append(potential_q)
                relevant_text.append("</Q>\n")
                q_counter+=1
        relevant_text = ''.join(relevant_text)
        return relevant_text

if __name__ == "__main__":
    dc = Data_Creator("C:\\Users\\Prkr_Xps\\PycharmProjects\\tesseract_test")
    dc.file_list = dc.get_file_list("\\pdfs")
    dc.create_working_directories()
    dc.convert_pdf_to_png()
    dc.file_png_list = dc.get_file_list("\\pngs")
    dc.extract_text_from_pngs()
    # dc.file_text_list = dc.get_file_list("\\texts")
    # for file in dc.file_text_list:
    #     with open(file[0], "r+",encoding="utf-8") as f_in:
    #         to_clean = f_in.read()
    #         to_write = dc.clean_text(to_clean)
    #     with open(file[0], "w", encoding="utf-8") as out:
    #         out.write(to_write)
    print(dc.file_list)
