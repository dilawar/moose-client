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
import tkinter as TK
if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
else:  
    import PySimpleGUI27 as sg  

sdir_ = os.path.dirname( __file__ )
w_, h_ = 400, 300

layout = [      
        [sg.Text('MOOSE Server')],      
        [sg.Text('Server Adress', size=(15,1)), sg.InputText('ghevar.ncbs.res.in:31417')],      
        [sg.Text('Main file'), sg.Input(), sg.FileBrowse()],
        [sg.Text('Other files'), sg.Input(), sg.FilesBrowse()],
        [sg.Canvas(size=(w_,h_), key='canvas')],
        [sg.Output(key='output') ],
        [sg.Submit(), sg.Exit()]      
        ]

def draw_canvas( canvas, fig ):
    #  tkCanvas.create_oval(50, 50, 100, 100)
    #  photo = tkinter.PhotoImage( file=fig, width=800, height=500 )
    #  print( photo.width(), photo.height() )
    photo = TK.PhotoImage(file=fig, width=500, height=500)
    image = canvas.TKCanvas.create_image(100, 100, anchor=TK.NW ,image=photo)
    #  image.pack()
    #  tkCanvas.create_image(0, 0, image=img, anchor=tkinter.NW)

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
          # change the "output" element to be the value of "input" element  
          #  window.FindElement('_OUTPUT_').Update(values['_IN_'])
          pass
      else:
          print( 'Unsupported event' )
    window.Close()

if __name__ == '__main__':
    main()
