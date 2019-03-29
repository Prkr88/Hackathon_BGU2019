# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prepary.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import random


class Ui_Prepary(object):

    def setupUi(self, Prepary):
        Prepary.setObjectName("Prepary")
        Prepary.resize(1299, 968)
        Prepary.setStyleSheet("")
        self.result_list = []
        self.file_map = {}
        self.png_win = QtWidgets.QScrollArea()
        self.centralwidget = QtWidgets.QWidget(Prepary)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(3, -48, 1291, 1061))
        self.label.setStyleSheet("background-image: url(resources//exam_multiplechoice.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.uplaod_pic = QtWidgets.QTabWidget(self.centralwidget)
        self.uplaod_pic.setGeometry(QtCore.QRect(260, 40, 1021, 301))
        self.uplaod_pic.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.uplaod_pic.setAutoFillBackground(False)
        self.uplaod_pic.setStyleSheet("QTabWidget{\n"
                                      "    font: 10pt \"RelishPro 2\";\n"
                                      "    color: #BEBEBE;\n"
                                      "    border: 2px solid #555;\n"
                                      "    border-radius: 20px;\n"
                                      "    border-style: outset;\n"
                                      "    padding: 5px;\n"
                                      "}\n"
                                      "")
        self.uplaod_pic.setObjectName("uplaod_pic")
        self.course_num = QtWidgets.QWidget()
        self.course_num.setObjectName("course_num")
        self.cn_comboBox = QtWidgets.QComboBox(self.course_num)
        self.cn_comboBox.setGeometry(QtCore.QRect(630, 110, 351, 61))
        self.cn_comboBox.setStyleSheet("QComboBox {\n"
                                       "\n"
                                       " color: #BEBEBE; \n"
                                       "border: 2px solid #cccccc;\n"
                                       "border-radius: 10px;\n"
                                       "    font: 12pt \"MS Shell Dlg 2\";\n"
                                       "\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "\n"
                                       "QComboBox::drop-down {\n"
                                       "color: #BEBEBE; \n"
                                       "border: 2px solid #cccccc;\n"
                                       "border-radius: 10px;\n"
                                       "background-image: url(:/back1/icon_in_the_input_box_drop_down_arrow_511486.png);\n"
                                       "}\n"
                                       "\n"
                                       "")
        self.cn_comboBox.setObjectName("cn_comboBox")
        self.cn_comboBox.addItem("")
        self.cn_comboBox.addItem("")
        self.Search = QtWidgets.QPushButton(self.course_num)
        self.Search.setGeometry(QtCore.QRect(160, 110, 187, 57))
        self.Search.setStyleSheet("QPushButton {\n"
                                  "    font: 10pt \"RelishPro 2\";\n"
                                  "    color: #F5F5F5;\n"
                                  "    border: 2px solid #555;\n"
                                  "    border-radius: 20px;\n"
                                  "    border-style: outset;\n"
                                  "    background: qradialgradient(\n"
                                  "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                  "        radius: 1.35, stop: 0     #ff920c, stop: 1 #db6008\n"
                                  "        );\n"
                                  "    padding: 5px;\n"
                                  "    }\n"
                                  "\n"
                                  "QPushButton:hover {\n"
                                  "    background: qradialgradient(\n"
                                  "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                  "        radius: 1.35, stop: 0 #ffa62b, stop: 1 #ff920c\n"
                                  "        );\n"
                                  "    }\n"
                                  "\n"
                                  "QPushButton:pressed {\n"
                                  "    border-style: inset;\n"
                                  "    background: qradialgradient(\n"
                                  "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                  "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
                                  "        );\n"
                                  "    }")
        self.Search.setObjectName("Search")
        self.uplaod_pic.addTab(self.course_num, "")
        self.free_text = QtWidgets.QWidget()
        self.free_text.setObjectName("free_text")
        self.uplaod_pic.addTab(self.free_text, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.uplaod_pic.addTab(self.tab, "")
        self.listWidget_results = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_results.setGeometry(QtCore.QRect(870, 400, 411, 551))
        self.listWidget_results.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidget_results.setStyleSheet("QListWidget{\n"
                                              "    font: 10pt \"RelishPro 2\";\n"
                                              "    color: #BEBEBE;\n"
                                              "    border: 2px solid #555;\n"
                                              "    border-radius: 20px;\n"
                                              "    border-style: outset;\n"
                                              "    background: #F5F5F5;\n"
                                              "    padding: 5px;\n"
                                              "\n"
                                              "}")
        self.listWidget_results.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listWidget_results.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget_results.setObjectName("listWidget_results")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.listWidget_results.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.listWidget_results.addItem(item)
        self.show_png = QtWidgets.QPushButton(self.centralwidget)
        self.show_png.setGeometry(QtCore.QRect(650, 620, 187, 57))
        self.show_png.setStyleSheet("QPushButton {\n"
                                    "    font: 10pt \"RelishPro 2\";\n"
                                    "    color: #F5F5F5;\n"
                                    "    border: 2px solid #555;\n"
                                    "    border-radius: 20px;\n"
                                    "    border-style: outset;\n"
                                    "    background: qradialgradient(\n"
                                    "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                    "        radius: 1.35, stop: 0     #68abfd, stop: 1 #157efb\n"
                                    "        );\n"
                                    "    padding: 5px;\n"
                                    "    }\n"
                                    "\n"
                                    "QPushButton:hover {\n"
                                    "    background: qradialgradient(\n"
                                    "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                    "        radius: 1.35, stop: 0 #cde3fe, stop: 1 #68abfd\n"
                                    "        );\n"
                                    "    }\n"
                                    "\n"
                                    "QPushButton:pressed {\n"
                                    "    border-style: inset;\n"
                                    "    background: qradialgradient(\n"
                                    "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                    "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
                                    "        );\n"
                                    "    }")
        self.show_png.setObjectName("show_png")
        Prepary.setCentralWidget(self.centralwidget)

        self.retranslateUi(Prepary)
        self.uplaod_pic.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Prepary)
        # Set functionality
        self.show_png.clicked.connect(self.open_png_in_new_window)
        self.Search.clicked.connect(self.get_questions)

    def retranslateUi(self, Prepary):
        _translate = QtCore.QCoreApplication.translate
        Prepary.setWindowTitle(_translate("Prepary", "Prepary | How you Learn"))
        self.cn_comboBox.setItemText(0, _translate("Prepary", "367.1.2131"))
        self.cn_comboBox.setItemText(1, _translate("Prepary", "362.1.2241"))
        self.Search.setText(_translate("Prepary", "חפש"))
        self.uplaod_pic.setTabText(self.uplaod_pic.indexOf(self.course_num), _translate("Prepary", "מספר קורס"))
        self.uplaod_pic.setTabText(self.uplaod_pic.indexOf(self.free_text), _translate("Prepary", "טקסט חופשי"))
        self.uplaod_pic.setTabText(self.uplaod_pic.indexOf(self.tab), _translate("Prepary", "העלה תמונה"))
        __sortingEnabled = self.listWidget_results.isSortingEnabled()
        self.listWidget_results.setSortingEnabled(False)
        # item = self.listWidget_results.item(0)
        # item.setText(_translate("Prepary", "20119571.2014A.PDF_1"))
        # item = self.listWidget_results.item(1)
        # item.setText(_translate("Prepary", "20119571.2014C.PDF_1"))
        self.listWidget_results.setSortingEnabled(__sortingEnabled)
        self.show_png.setText(_translate("Prepary", "הצג"))

    def open_png_in_new_window(self):
        try:
            self.png_win = QtWidgets.QScrollArea()
            selected = self.listWidget_results.selectedItems()
            item = selected[0]
            to_show = self.file_map[item.text()]
            print(to_show)
            hbox = QtWidgets.QHBoxLayout()
            pixmap = QtGui.QPixmap(to_show)
            lbl = QtWidgets.QLabel()
            lbl.setPixmap(pixmap)
            hbox.addWidget(lbl)
            self.png_win.setLayout(hbox)
            self.png_win.move(300, 200)
            self.png_win.setWindowTitle(item.text())
            self.png_win.show()
        except Exception as e:
            print(e)

    def get_questions(self):
        self.result_list = []
        self.file_map = {}
        cid = str(self.cn_comboBox.currentText())
        cid = cid.replace('.', '')
        print(cid)
        self.get_file_list(cid)
        self.feed_listWidget()

    def get_file_list(self, cid):
        local_file_list = []
        for root, dirs, files in os.walk("resources\\questions_separated"):
            for file in files:
                if cid not in file:
                    file_path = os.path.join(root, file)
                    self.result_list.append(file)
                    self.file_map[file] = file_path
        random.shuffle(self.result_list)
        print(self.result_list)


    def feed_listWidget(self):
        _translate = QtCore.QCoreApplication.translate
        self.listWidget_results.clear()
        for ex_id in self.result_list:
            item = QtWidgets.QListWidgetItem()
            self.listWidget_results.addItem(item)
            # item = self.listWidget_results.item(idx)
            # if to_add == 'Query_ID:':
            #     to_add = to_add + ' ' + str(doc[1])
            #     item.setBackground(QtGui.QColor("black"))
            item.setText(_translate("Prepary", ex_id))

    def show_gui(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Prepary = QtWidgets.QMainWindow()
        ui = Ui_Prepary()
        ui.setupUi(Prepary)
        Prepary.show()
        sys.exit(app.exec_())
