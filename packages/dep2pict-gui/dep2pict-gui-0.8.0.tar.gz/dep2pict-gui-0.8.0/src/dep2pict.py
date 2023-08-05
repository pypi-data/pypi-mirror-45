#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import subprocess
from json2html import *

# 2 next lines: quit on Ctrl-C in terminal (stackoverflow.com/questions/4938723)
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from src import conll

from PyQt5.QtWidgets import (
    qApp, QWidget, QPushButton, QSlider, QSplitter, QAbstractItemView,
    QLabel, QHBoxLayout, QVBoxLayout, QApplication, QScrollArea,
    QTreeView, QAction, QMainWindow, QFileDialog,QMessageBox, QLineEdit
)

from PyQt5 import QtWebEngineWidgets

from PyQt5.QtCore import QUrl, Qt, QFileSystemWatcher, pyqtSignal, QObject, QRegExp, QSortFilterProxyModel
from PyQt5.QtGui import *


# create a new signal [treeview_change] for connection of arrow navigation in the treeview
class Communicate(QObject):
    treeview_change = pyqtSignal()

# a new TreeView widget is needed for redefinition of [currentChanged]
class TreeViewWithReactiveArrows(QTreeView):
    current_index = None
    def currentChanged(self,x,y):
        self.current_index = x
        self.c.treeview_change.emit()

class Dep2pict(QMainWindow):
    def __init__(self, screen, parent = None):
        super(Dep2pict, self).__init__(parent)

        # Set the flag d2p to True iff the external program dep2pict is installed.
        d2p = True
        try:
            sub=subprocess.run (["dep2pict", "--check"])
            if sub.returncode != 0:
                d2p = False
        except:
            d2p = False

        self.current_sent_id = None
        self.sent_id_list = []
        self.sentence_offset_dict = dict()
        self.conll_file = None
        self.scroll_pos = None

        self.init_menu()
        self.init_watcher()
        self.build_widgets()

        if d2p:
            self.setWindowTitle('Dep2pict')

            self.setGeometry(0, 0, screen.width(), screen.height()/2)
            self.show()

            if len(sys.argv) > 1:
                self.open_new_file(sys.argv[1])
        else:
            self.message("The Dep2pict application requires the 'dep2pict' command\nSee http://dep2pict.loria.fr/installation for install instructions")
            qApp.quit()

# -------------------------------------------------------------------------------------------
    def message(self,text):
        msgBox = QMessageBox(self.main_vbox_w)
        msgBox.setText(text)
        msgBox.exec_()

# -------------------------------------------------------------------------------------------
    def init_watcher(self):
        self.watcher = QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.watcher_action)

# -------------------------------------------------------------------------------------------
    def update_watcher(self):
        if self.watcher.files() != []:
            self.watcher.removePaths (self.watcher.files());
        if self.conll_file:
            self.watcher.addPath(self.conll_file);

# -------------------------------------------------------------------------------------------
    def watcher_action(self):
        qpoint = self.web_view.page().scrollPosition()
        self.scroll_pos = (qpoint.x(), qpoint.y())
        self.data_refresh()

# -------------------------------------------------------------------------------------------
    def build_widgets(self):
        self.main_vbox_w = QWidget()
        self.setCentralWidget(self.main_vbox_w)

        # The [main_vbox] covering the whole interface
        main_vbox = QVBoxLayout()
        self.main_vbox_w.setLayout(main_vbox)

        # Horizontal [splitter]
        splitter = QSplitter(Qt.Horizontal)
        main_vbox.addWidget(splitter)

        # [left_vbox]: left side of the [splitter]
        left_vbox_w = QWidget()
        splitter.addWidget(left_vbox_w)
        left_vbox = QVBoxLayout()
        left_vbox_w.setLayout(left_vbox)

        # [right_vbox]: right side of the [splitter]
        right_vbox_w = QWidget()
        splitter.addWidget(right_vbox_w)
        right_vbox = QVBoxLayout()
        right_vbox_w.setLayout(right_vbox)

        splitter.setStretchFactor(1, 10)


        # a treeview [self.corpus] in [left_vbox]
        self.corpus = TreeViewWithReactiveArrows()
        self.corpus.setEditTriggers(QAbstractItemView.NoEditTriggers)
        left_vbox.addWidget(self.corpus)

        # Add the home-made treeview_change event and bind it
        self.corpus.c = Communicate()
        self.corpus.c.treeview_change.connect(self.item_change)

        # build [self.model] and bind it to [self.corpus]
        self.model = QSortFilterProxyModel(self)
        self.model.setSourceModel(QStandardItemModel(0, 1, self))
        self.model.setHeaderData(0, Qt.Horizontal, "Sent_id")
        self.corpus.setModel(self.model)

        # The [self.regexp] LineEdit in [left_vbox]
        self.regexp = QLineEdit()
        self.regexp.setClearButtonEnabled(True)
        left_vbox.addWidget(self.regexp)
        self.regexp.textChanged.connect(self.regexp_change)

        # [self.text_label] for sentence display in [right_vbox]
        self.text_label = QLabel("")
        self.text_label.setFont(QFont('SansSerif', 24))
        self.text_label.setHidden(True)
        self.text_label.setWordWrap(True);
        right_vbox.addWidget(self.text_label)

        # [right_hbox] for sentence + slider
        right_hbox = QHBoxLayout()
        right_hbox.setContentsMargins(0,0,0,0) #(left, top, right, bottom)
        right_vbox.addLayout(right_hbox)

        # [self.web_view] for dependency display
        self.web_view = QtWebEngineWidgets.QWebEngineView(self)
        right_hbox.addWidget(self.web_view)
        self.web_view.loadFinished.connect(self.post_draw) #keep scroll position

        # add [slider] and connect it to [self.web_view]
        slider = QSlider(Qt.Vertical)
        slider.setMaximum(300)
        slider.setMinimum(50)
        slider.setValue(100)
        slider.valueChanged.connect(lambda v:self.web_view.setZoomFactor(v/100))
        right_hbox.addWidget(slider)
    # END build_widgets

# -------------------------------------------------------------------------------------------
    def init_menu(self):
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.triggered[QAction].connect(self.menu_file_action)

        open_ = QAction("Open",self)
        open_.setShortcut("Ctrl+O")
        file.addAction(open_)

        quit = QAction("Quit",self)
        quit.setShortcut("Ctrl+Q")
        file.addAction(quit)

# -------------------------------------------------------------------------------------------
    def menu_file_action(self, q):
        action=q.text()
        if action == "Quit":
            qApp.quit()
        if action == "Open":
            self.open_dialog()

# -------------------------------------------------------------------------------------------
    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        if fname[0]:
            self.open_new_file(fname[0])

# -------------------------------------------------------------------------------------------
    def item_change(self):
        index = self.corpus.current_index
        sent_id = index.data()
        if sent_id is not None:
            if self.current_sent_id != sent_id:
                self.current_sent_id = sent_id
                self.scroll_pos = None
            self.draw()

# -------------------------------------------------------------------------------------------
    def draw (self):
        if self.current_sent_id is not None:
            try:
                (sentence,offset) = self.sentence_offset_dict[self.current_sent_id]
            except KeyError:
                self.message('Cannot find sent_id: %s' % self.current_sent_id)
                self.current_sent_id = self.sent_id_list[0]
                (sentence,offset) = self.sentence_offset_dict[self.current_sent_id]
            reply = conll.to_svg (sentence)
            if os.path.isfile(reply):
                self.web_view.setUrl(QUrl("file://"+reply))
            else:
                err = json.loads(reply)
                err["file"] = self.conll_file
                if "line" in err:
                    err["line"] = err["line"] + offset
                html = json2html.convert(json = err)
                self.web_view.setHtml("<h1>Error in CoNLL data:</h1>\n"+html)
            text = conll.get_text(sentence)
            if text is None:
                self.text_label.setHidden(True)
            else:
                self.text_label.setHidden(False)
                self.text_label.setText(text)

# -------------------------------------------------------------------------------------------
    def post_draw(self):
        if self.scroll_pos != None:
            self.web_view.page().runJavaScript("window.scrollTo(%g, %g);" % self.scroll_pos)

# -------------------------------------------------------------------------------------------
    def open_new_file(self, filename):
        self.conll_file = filename
        self.setWindowTitle('Dep2pict -- '+filename)
        self.current_sent_id = None
        self.scroll_pos = None
        self.update_watcher()
        self.data_refresh()

# -------------------------------------------------------------------------------------------
    def empty(self):
        self.web_view.setHtml("<h1>No graph</h1>")
        self.text_label.setHidden(True)

# -------------------------------------------------------------------------------------------
    def data_refresh(self):
        old_regexp = self.regexp.text()
        self.regexp.setText("")
        if self.conll_file:
            # Remove the current rows in self.model
            self.model.removeRows(0,self.model.rowCount ())
            try:
                (self.sent_id_list, self.sentence_offset_dict) = conll.load_conll(self.conll_file)
                # Fill list
                pos=0
                for s in self.sent_id_list:
                    self.model.insertRow(pos)
                    self.model.setData(self.model.index(pos, 0), s)
                    pos += 1

                if self.sent_id_list == []:
                    self.empty()
                    self.message('The file "%s" is empty' % self.conll_file)
                else:
                    if self.current_sent_id in self.sent_id_list:
                        self.draw()
                        self.regexp.setText(old_regexp)
                    else:
                        self.current_sent_id = self.sent_id_list[0]
                        self.draw()
            except FileNotFoundError:
                self.empty()
                self.message('File not found: "%s"' % self.conll_file)

# -------------------------------------------------------------------------------------------
    def regexp_change(self):
        regExp = QRegExp(self.regexp.text(), True, QRegExp.RegExp)
        self.model.setFilterRegExp(regExp)

# ===========================================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    screen = app.desktop().screenGeometry()
    Dep2pict(screen)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
