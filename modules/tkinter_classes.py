# This file contains classes for the tkinter menus and custom widgets

import tkinter as tk
#from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkwidgets.autocomplete import *
#from tkinter.messagebox import showinfo

class ComboboxFrame():
    # This widget prompts the user to input data from a tuple of fields.
    # Fields must be formatted as such:
    # (option1, option2)

    def __init__(self, parent, name, frame_text, fields):
        self.parent  = parent
        self.name = name
        
        self.fields = fields

        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
            #width=60,
            #fg = '#AAAAAA',
            #bg = '#AAAAAA'
        )

        self.value = tk.StringVar()

        for index, value in enumerate(fields):
            self.entry = ttk.Radiobutton(
            self.frame1,
            text=value,
            variable=self.value,
            value=value
            )
            self.entry.grid(row=index, column=0) # Put them side by side.
    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)

class ProjectMetaPrompt():
    # Options must be formatted as such:
    # ( (field1, (option1, option2)), (field2, (option1, option2)) )
    def __init__(self, parent, name, frame_text, fields):
        self.parent  = parent
        self.name = name
        
        self.fields = fields # DO I NEED THIS??????????????????????
        
        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
            #width=60,
            #fg = '#AAAAAA',
            #bg = '#AAAAAA'
        )

        # Create GUI for project metadata if project is new
        game = ComboboxFrame(self.frame1, 'game_frame', 'Choose the game', ('AC5', 'ACZ'))
        game.grid(row=0, column=0)

        # Create GUI for project choosing
        track_type = ComboboxFrame(self.frame1, 'track_frame', 'What type of audio tracks?', ('BGM', 'RADIO'))
        track_type.grid(row=0, column=1)
    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)