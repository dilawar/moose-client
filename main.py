"""main.py: 
Python3 UI.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import re
import socket
import PIL.ImageTk 
import PIL.Image

try:
    import tkinter as TK
except ImportError as e:
    import Tkinter as TK

if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
else:  
    import PySimpleGUI27 as sg  

sdir_ = os.path.dirname( __file__ )
w_, h_ = 400, 300

# need a global because we don't want img_ to be garbage collected.
img_   = None

layout = [ 
        [sg.Text('Server Adress', size=(15,1))
            , sg.InputText('ghevar.ncbs.res.in:31417', key='server')]
        , [sg.Text('Main file'), sg.Input(key='main_file'), sg.FileBrowse()]
        , [sg.Text('Other files'), sg.Input(key='other_files'), sg.FilesBrowse()]
        , [sg.Canvas(size=(w_,h_), key='canvas')]
        # Output size is in chars x line 
        , [sg.Output(key='output', size=(80,4))]
        , [sg.Submit(), sg.Exit()]
        ]

def draw_canvas( canvas, imgpath ):
    global img_
    global w_, h_
    img_ = PIL.ImageTk.PhotoImage(PIL.Image.open(imgpath).resize((w_,h_)))
    canvas.TKCanvas.create_image(0, 0, anchor=TK.NW ,image=img_)

def main():
    window = sg.Window('MOOSE').Layout(layout).Finalize()
    draw_canvas( window.FindElement('canvas' )
            , os.path.join(sdir_, './assests/moose_icon_large.png' )
            )
    while True:                 # Event Loop  
        event, values = window.Read()  
        print(event, values)
        if event is None or event == 'Exit':  
            break  
        if event == 'Submit':  
            pass
        else:
            print( 'Unsupported event' )
        for x in ['server', 'main_file', 'other_files']:
            window.FindElement(x).Update(values.get(x,''))
    window.Close()

if __name__ == '__main__':
    main()
