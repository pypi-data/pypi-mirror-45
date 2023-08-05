# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plover_dictionary_builder\dictionary_builder.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DictionaryBuilder(object):
    def setupUi(self, DictionaryBuilder):
        DictionaryBuilder.setObjectName("DictionaryBuilder")
        DictionaryBuilder.resize(536, 441)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DictionaryBuilder.sizePolicy().hasHeightForWidth())
        DictionaryBuilder.setSizePolicy(sizePolicy)
        DictionaryBuilder.setStyleSheet("QDialog {\n"
"margin: -6;\n"
"}")
        DictionaryBuilder.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DictionaryBuilder)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pages = QtWidgets.QStackedWidget(DictionaryBuilder)
        self.pages.setObjectName("pages")
        self.input = QtWidgets.QWidget()
        self.input.setObjectName("input")
        self.vlayout = QtWidgets.QVBoxLayout(self.input)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setObjectName("vlayout")
        self.intro_label = QtWidgets.QLabel(self.input)
        self.intro_label.setWordWrap(True)
        self.intro_label.setObjectName("intro_label")
        self.vlayout.addWidget(self.intro_label)
        self.text_box = QtWidgets.QPlainTextEdit(self.input)
        self.text_box.setTabChangesFocus(True)
        self.text_box.setObjectName("text_box")
        self.vlayout.addWidget(self.text_box)
        self.check_line_translations = QtWidgets.QCheckBox(self.input)
        self.check_line_translations.setObjectName("check_line_translations")
        self.vlayout.addWidget(self.check_line_translations)
        self.check_include_words = QtWidgets.QCheckBox(self.input)
        self.check_include_words.setObjectName("check_include_words")
        self.vlayout.addWidget(self.check_include_words)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_text_transformation = QtWidgets.QLabel(self.input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_text_transformation.sizePolicy().hasHeightForWidth())
        self.label_text_transformation.setSizePolicy(sizePolicy)
        self.label_text_transformation.setObjectName("label_text_transformation")
        self.horizontalLayout.addWidget(self.label_text_transformation)
        self.combo_text_transformation = QtWidgets.QComboBox(self.input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_text_transformation.sizePolicy().hasHeightForWidth())
        self.combo_text_transformation.setSizePolicy(sizePolicy)
        self.combo_text_transformation.setObjectName("combo_text_transformation")
        self.combo_text_transformation.addItem("")
        self.combo_text_transformation.addItem("")
        self.combo_text_transformation.addItem("")
        self.horizontalLayout.addWidget(self.combo_text_transformation)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.vlayout.addLayout(self.horizontalLayout)
        self.pages.addWidget(self.input)
        self.builder = QtWidgets.QWidget()
        self.builder.setObjectName("builder")
        self.glayout = QtWidgets.QGridLayout(self.builder)
        self.glayout.setContentsMargins(0, 0, 0, 0)
        self.glayout.setObjectName("glayout")
        self.add_translation = AddTranslationWidget(self.builder)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_translation.sizePolicy().hasHeightForWidth())
        self.add_translation.setSizePolicy(sizePolicy)
        self.add_translation.setObjectName("add_translation")
        self.glayout.addWidget(self.add_translation, 2, 0, 1, 1)
        self.order_combo = QtWidgets.QComboBox(self.builder)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.order_combo.sizePolicy().hasHeightForWidth())
        self.order_combo.setSizePolicy(sizePolicy)
        self.order_combo.setObjectName("order_combo")
        self.order_combo.addItem("")
        self.order_combo.addItem("")
        self.order_combo.addItem("")
        self.glayout.addWidget(self.order_combo, 0, 1, 1, 1)
        self.word_list_widget = QtWidgets.QListWidget(self.builder)
        self.word_list_widget.setObjectName("word_list_widget")
        self.glayout.addWidget(self.word_list_widget, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.builder)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.glayout.addWidget(self.label, 0, 0, 1, 1)
        self.pages.addWidget(self.builder)
        self.verticalLayout.addWidget(self.pages)
        self.button_box = QtWidgets.QDialogButtonBox(DictionaryBuilder)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.NoButton)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(DictionaryBuilder)
        self.pages.setCurrentIndex(0)
        self.button_box.accepted.connect(DictionaryBuilder.accept)
        self.button_box.rejected.connect(DictionaryBuilder.reject)
        QtCore.QMetaObject.connectSlotsByName(DictionaryBuilder)
        DictionaryBuilder.setTabOrder(self.text_box, self.check_include_words)
        DictionaryBuilder.setTabOrder(self.check_include_words, self.order_combo)

    def retranslateUi(self, DictionaryBuilder):
        _translate = QtCore.QCoreApplication.translate
        DictionaryBuilder.setWindowTitle(_translate("DictionaryBuilder", "Plover: Dictionary Builder"))
        self.intro_label.setText(_translate("DictionaryBuilder", "To start building your dictionaries, please enter the text you would like to analyze for words. Text can be anything from articles to lists."))
        self.check_line_translations.setText(_translate("DictionaryBuilder", "Treat each line as one translation (for phrases, word lists, etc.)"))
        self.check_include_words.setText(_translate("DictionaryBuilder", "Include words that are already defined in my dictionaries"))
        self.label_text_transformation.setText(_translate("DictionaryBuilder", "Text transformation:"))
        self.combo_text_transformation.setItemText(0, _translate("DictionaryBuilder", "None"))
        self.combo_text_transformation.setItemText(1, _translate("DictionaryBuilder", "UPPERCASE"))
        self.combo_text_transformation.setItemText(2, _translate("DictionaryBuilder", "lowercase"))
        self.order_combo.setItemText(0, _translate("DictionaryBuilder", "Frequency"))
        self.order_combo.setItemText(1, _translate("DictionaryBuilder", "Order of Appearance"))
        self.order_combo.setItemText(2, _translate("DictionaryBuilder", "Alphabetical"))
        self.label.setText(_translate("DictionaryBuilder", "Defining word {current} of {total}: {word}"))

from plover.gui_qt.add_translation_widget import AddTranslationWidget
from . import resources_rc
