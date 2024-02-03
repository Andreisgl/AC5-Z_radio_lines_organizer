# This file contains classes for the tkinter menus and custom widgets

import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkwidgets.autocomplete import *
#from tkinter.messagebox import showinfo

def center_window(window):
    # This function automatically centers the window passed as parameter.
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    

    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()


    # Calculate the x and y coordinates for centering the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window's geometry to center it on the screen
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

class RadioboxFrame():
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
            entry = ttk.Radiobutton(
            self.frame1,
            text=value,
            variable=self.value,
            value=value
            )
            #entry.grid(row=index, column=0) # Put them side by side.
            entry.pack(anchor=tk.W)
    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
    def pack(self, **kwargs):
        self.frame1.pack(**kwargs)
        
    def get_value(self):
        project_choice = self.value.get()
        return project_choice

class ProjectMetaPromptFrame():
    # Options must be formatted as such:
    # ( (field1, (option1, option2)), (field2, (option1, option2)) )
    def __init__(self, parent, name, frame_text, fields):
        self.parent  = parent
        self.name = name
        
        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
        )

        self.field_widgets = []
        for field in fields:
            aux = RadioboxFrame(parent, field[0], field[0], field[1])
            self.field_widgets.append(aux)
        
        for field in self.field_widgets:
            field.pack()
            pass

    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
    def pack(self, **kwargs):
        self.frame1.pack(**kwargs)
    
    def get_value(self):
        # Returns values as:
        # ((FIELD_NAME1, VALUE), (FIELD_NAME2, VALUE))
        results = []
        for field in self.field_widgets:
            results.append((field.name, field.get_value()))
        return tuple(results)
    
class ChooseProjectFrame():
    def __init__(self, parent, name, frame_text, project_list, action):
        self.parent  = parent
        self.name = name
        
        

        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
        )   

        # Create GUI for project choosing
        self.project_var = tk.StringVar()
        self.project_prompt = ttk.Combobox(
            self.frame1,
            values = project_list,
            textvariable=self.project_var
        )

        self.project_prompt.pack()

        

    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
    def pack(self, **kwargs):
        self.frame1.pack(**kwargs)
    
    def get_value(self):
        project_choice = self.project_var.get()
        return project_choice

class LineEntryItem():
    '''
    This class represents a single line entry
    for each line that is contained in the lines folder
    '''
    # Data to be present in each entry:
    # 1 - index
    # 2 - File name
    # 3 - Text
    # 4 - Play button

    def __init__(self, parent, name, index_text, filename_text, line_text):
        self.parent  = parent
        self.name = name
        
        def set_styles():
            std_text_style = ttk.Style()
            std_text_style.configure('std.TLabel', font=("sans_serif", "9"), padding=(10, 0))

            std_btn_style = ttk.Style()
            std_btn_style.configure('std.TButton', font=("sans_serif", "5"))

            test_style = ttk.Style()
            test_style.configure('test.TFrame', background='blue')
            test_style = ttk.Style()
            test_style.configure('done.TFrame', background='green')

        def play_track():
            print('PLAY TRACK!!!\t Index: {} - Filename: {} - Line: {}'.format(
                index_text, filename_text, line_text
            ))
            pass

        set_styles()

        self.frame1 = ttk.Frame(
            parent,
            style='test.TFrame',
            relief="ridge",
            borderwidth=2
        )
        self.frame1.pack(fill="x", expand=True)
        self.frame1.configure(style='done.TFrame')

        track_index = ttk.Label(
            self.frame1, text=index_text)
        track_index.grid(column=0, row=0)

        track_name = ttk.Label(
            self.frame1, text=filename_text, style='std.TLabel')
        track_name.grid(column=1, row=0)

        track_text = ttk.Label(
            self.frame1, text=line_text, style='std.TLabel')
        track_text.grid(column=2, row=0)

        play_track = ttk.Button(
            self.frame1, text='PLAY', style='std.TButton', command=play_track)
        play_track.grid(column=3, row=0)
        
        
    
    
    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
    def pack(self, **kwargs):
        self.frame1.pack(**kwargs)

class LineManipulationFrame():
    '''
    This class contains the list that allows the user to browse all line files
    '''
    # MAYBE THESE COMMENTS COVER SOMETHING I FORGOT. WON'T ERASE UNTIL I'M SURE THEY ARE BOGUS
        # Options must be formatted as such:
        # ( (field1, (option1, option2)), (field2, (option1, option2)) )
    
    def __init__(self, parent, name, lines_data):
        self.parent  = parent
        self.name = name
        
        # Create a canvas to hold the LineEntryItem widgets
        canvas = tk.Canvas(self.parent)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar and attach it to the canvas
        vsb = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the LineEntryItem widgets
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        
        for index, i in enumerate(lines_data):
            full_line = i[1]
            item = LineEntryItem(
                frame,
                name=f"Item {i}",
                index_text=f"Index: {index}",
                filename_text=f"{i[0]}",
                line_text=f"{full_line[:20]}..." # Crop text to keep reasonable length
            )
            item.pack(fill="x")

        # Bind the canvas to respond to changes in the frame size
        def configure_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", configure_frame)
    
class EmptyProjectFrame():
    def __init__(self, parent, name, frame_text, action):
        self.parent  = parent
        self.name = name
        
        

        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
        )  

        warning_label = ttk.Label(
            self.frame1, text='aaaaaaa', style='std.TLabel')

        # Create GUI for project choosing
        self.project_var = tk.StringVar()
        self.project_prompt = ttk.Combobox(
            self.frame1,
            #values = project_list,
            textvariable=self.project_var
        )

        self.project_prompt.pack()

        

    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
    def pack(self, **kwargs):
        self.frame1.pack(**kwargs)
    
    def get_value(self):
        project_choice = self.project_var.get()
        return project_choice