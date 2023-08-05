from collections import OrderedDict, Counter

import re

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QPushButton, QDialogButtonBox, QAbstractItemView, QMessageBox)

from plover.gui_qt.tool import Tool

from plover_dictionary_builder.dictionary_builder_ui import Ui_DictionaryBuilder

SORT_FREQUENCY, SORT_APPEARANCE, SORT_ALPHABETICAL = range(3)


class OrderedCounter(Counter, OrderedDict):
    pass


class DictionaryBuilder(Tool, Ui_DictionaryBuilder):

    TITLE = 'Dictionary Builder'
    ICON = ':/dictionary_builder/icon.svg'
    ROLE = 'builder'
    SHORTCUT = 'Ctrl+B'

    def __init__(self, engine):
        super(DictionaryBuilder, self).__init__(engine)
        self.setupUi(self)
        self._engine = engine
        self._current_word = 0
        self._undo_button = None

        self._operations = []

        self.user_input = None
        self.builder = None

        self._word_lists = None

        self.order_combo.currentIndexChanged.connect(self.set_sort_order)
        self.word_list_widget.currentItemChanged.connect(self.word_list_changed)

        self.input_buttons()

        self.installEventFilter(self)

        self.restore_state()
        self.finished.connect(self.save_state)

    def word_list_changed(self, item):
        if item is not None:
            self._current_word = self.word_list_widget.row(item)
            self.set_word(item.text())

    def set_word(self, word=None):
        if word is None:
            word = self.word_list_widget.item(self._current_word).text()
        self.add_translation.translation.setText(word)
        self.add_translation.on_translation_edited()
        fmt = 'Defining word {current} of {total}: {word}'
        info = fmt.format(current=self._current_word + 1,
                          total=len(self._word_lists[0]),
                          word=word
                          )
        self.label.setText(info)

    def set_sort_order(self, index=None):
        if index is None:
            index = self.order_combo.currentIndex()
        self._current_word = 0
        self.word_list_widget.clear()
        self.word_list_widget.addItems(self._word_lists[index])
        self.set_list_index(0)
        self.set_word(self._word_lists[index][0])

    def input_buttons(self):
        self.button_box.clear()
        button = QPushButton('&Quit', self)
        button.setToolTip('Exit the Dictionary Builder')
        button.setShortcut(Qt.CTRL + Qt.Key_W)
        self.button_box.addButton(button, QDialogButtonBox.RejectRole)
        button = QPushButton('&Start Building', self)
        button.setToolTip('Analyse the current text and start building')
        self.button_box.addButton(button, QDialogButtonBox.AcceptRole)

    def builder_buttons(self):
        self.button_box.clear()

        def set_tooltip_with_shortcut(button, tooltip):
            button.setToolTip('%s (%s)' %
                              (tooltip, button.shortcut().toString(
                                  QKeySequence.NativeText
                              )))

        button = QPushButton('&Add', self)
        button.setShortcut(Qt.Key_Return)
        set_tooltip_with_shortcut(button, 'Add the current stroke')
        button.setDefault(True)
        self.button_box.addButton(button, QDialogButtonBox.AcceptRole)

        button = QPushButton('&Previous', self)
        button.clicked.connect(self.on_previous)
        button.setShortcut(QKeySequence.MoveToPreviousLine)
        set_tooltip_with_shortcut(button,
                                  'Go back to the previous word')
        self.button_box.addButton(button, QDialogButtonBox.ActionRole)

        button = QPushButton('&Next', self)
        button.clicked.connect(self.on_next)
        button.setShortcut(QKeySequence.MoveToNextLine)
        set_tooltip_with_shortcut(button,
                                  'Skip the current word and go to the next')
        self.button_box.addButton(button, QDialogButtonBox.ActionRole)

        button = QPushButton('A&dd and Next', self)
        button.clicked.connect(self.on_add_and_next)
        button.setShortcut(Qt.CTRL + Qt.Key_S)
        set_tooltip_with_shortcut(
            button,
            'Add the current stroke and move to the next word'
        )
        self.button_box.addButton(button, QDialogButtonBox.DestructiveRole)

        button = QPushButton('&Undo', self)
        button.setShortcut(Qt.CTRL + Qt.Key_U)
        button.setEnabled(False)
        button.clicked.connect(self.on_undo)
        set_tooltip_with_shortcut(button, 'Undo the last addition')
        self._undo_button = button
        self.button_box.addButton(button, QDialogButtonBox.DestructiveRole)

        button = QPushButton('&Back to Input', self)
        button.setShortcut(Qt.CTRL + Qt.Key_W)
        set_tooltip_with_shortcut(button, 'Back to word list')

        button.clicked.connect(self.reject)
        self.button_box.addButton(button, QDialogButtonBox.ApplyRole)

    def make_word_list(self):
        user_text = self.text_box.toPlainText()

        transformation = self.combo_text_transformation.currentText().lower()
        if transformation == 'uppercase':
            user_text = user_text.upper()
        elif transformation == 'lowercase':
            user_text = user_text.lower()

        translations_by_line = self.check_line_translations.isChecked()

        # Need to match:
        #  - {#things}, {PLOVER:}, it's, with-hyphen, word. (not including .)
        #  - free2play, 4life
        # Need to avoid:
        #  - Pure numbers, e.g. 2, 1234
        #  - [2]
        words = (
            list(filter(None, user_text.split('\n')))
            if translations_by_line else
            re.findall(
                r'([\w\-_\'’]*[^\d\s\W]+[\w\-_\'’]*|{[^\s]*})',
                user_text
            )
        )
        if words:
            word_list = OrderedCounter(words)
            if not self.check_include_words.isChecked():
                # User only wants undefined words:
                for word in tuple(word_list.keys()):
                    if self._engine.casereverse_lookup(word.lower()):
                        del word_list[word]
            if word_list:
                # Create the three word list orders that we offer.
                self._word_lists = [None] * 3
                self._word_lists[SORT_FREQUENCY] = (
                    list(word for (word, _) in word_list.most_common())
                )
                self._word_lists[SORT_APPEARANCE] = (
                    tuple(word_list.keys())
                )
                self._word_lists[SORT_ALPHABETICAL] = (
                    sorted(list(word_list.keys()), key=lambda w: (w.lower(), w))
                )

    def on_previous(self):
        self.set_list_index(self._current_word - 1)

    def on_next(self):
        self.set_list_index(self._current_word + 1)

    def set_list_index(self, row_index):
        if 0 <= row_index < len(self._word_lists[0]):
            self._current_word = row_index
            item = self.word_list_widget.item(row_index)
            item.setSelected(True)
            self.word_list_widget.scrollToItem(item, QAbstractItemView.PositionAtCenter)
            self.set_word(item.text())
            self.focus_strokes()

    def reject(self):
        if self.pages.currentIndex() == 1:
            self.pages.setCurrentIndex(0)
            self.input_buttons()
        else:
            super(DictionaryBuilder, self).reject()

    def on_add(self):
        # Save entry and add to undo stack
        addition = self.add_translation.save_entry()
        if addition:
            # For the operation we save the translation change
            # and the builder's word for restoring the state.
            self._operations.append(
                (addition,
                 self.word_list_widget.item(
                    self._current_word
                 ).text()
                )
            )
            self._undo_button.setEnabled(True)
        # Queue lookup of translation for newly saved entry
        self.add_translation.on_translation_edited()
        # Clear strokes box and focus
        self.add_translation.strokes.setText('')
        self.add_translation.on_strokes_edited()
        self.focus_strokes()

    def focus_strokes(self):
        self.add_translation.strokes.setFocus()
        self.add_translation._focus_strokes()

    def on_add_and_next(self):
        self.on_add()
        self.on_next()

    def on_undo(self):
        last_operation, word = self._operations.pop()
        if not self._operations:
            self._undo_button.setEnabled(False)
        dictionary, strokes, old_translation, new_translation = last_operation
        if old_translation is None:
            self.delete_translation(strokes, dictionary)
        else:
            self._engine.add_translation(strokes, old_translation,
                                         dictionary_path=dictionary.path)
        items = self.word_list_widget.findItems(word, Qt.MatchExactly)
        if items:
            item = items[0]
            self.word_list_widget.setCurrentItem(item)
            self.word_list_changed(item)
            self.add_translation.translation.setText(new_translation)
            self.add_translation.strokes.setText(' '.join(strokes))
            self.add_translation.strokes.selectAll()
            self.add_translation.on_strokes_edited()
            self.add_translation.on_translation_edited()

    def delete_translation(self, strokes, dictionary):
        with self._engine:
            if strokes in dictionary:
                del dictionary[strokes]
                self._engine._dictionaries.save(path_list=(dictionary.path,))

    def accept(self):
        if self.pages.currentIndex() == 0:
            # Get user input.
            self.make_word_list()
            if self._word_lists:
                self.pages.setCurrentIndex(1)
                self.builder_buttons()
                self.add_translation.strokes.setFocus()
                self.set_sort_order()
            else:
                QMessageBox(
                    QMessageBox.Warning,
                    'No words found',
                    'Please enter text to build your dictionaries with.',
                    QMessageBox.Ok,
                    self
                ).exec()
        else:
            # Default action during editing.
            self.on_add()
