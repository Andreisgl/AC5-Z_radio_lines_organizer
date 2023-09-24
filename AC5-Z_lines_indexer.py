from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCompleter
from PyQt5.QtCore import pyqtSignal


import sys



words = ['apple', 'banana', 'cherry', 'grape', 'kiwi', 'orange', 'pear', 'strawberry']

# Each entry is a tuple. First item in the tuple is the criterion name,
# second is a list with autocomplete values
INDEXING_CRITERIA = (('CHARACTER', []),
                     ('TEXT', []),
                     ('MISSION', []),
                     ('ACE_STYLE', ['MERCENARY', 'SOLDIER', 'KNIGHT'])
                     )


