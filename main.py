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
import client
import tarfile
import glob
import helper

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
        #  , [sg.Output(key='output', size=(80,10))]
        , [sg.Submit(), sg.Exit()]
        ]

def draw_canvas(canvas, imgpath):
    global img_
    global w_, h_
    img_ = PIL.ImageTk.PhotoImage(PIL.Image.open(imgpath).resize((w_,h_)))
    canvas.TKCanvas.create_image(0, 0, anchor=TK.NW ,image=img_)

def display_results(bzfile, window):
    cwd = os.path.dirname(bzfile)
    print( "[INFO ] Result are saved to %s" % bzfile )
    with tarfile.open(bzfile, 'r') as f:
        f.extractall(path=cwd)
    toShow = helper.find_images(cwd)
    draw_canvas(window.FindElement('canvas'), toShow[0])

def main(args):
    window = sg.Window('MOOSE').Layout(layout).Finalize()
    if args['server']:
        window.FindElement('server').Update(args['server'])
    if args['input']:
        window.FindElement('main_file').Update(args['input'])
    draw_canvas( window.FindElement('canvas' )
            , os.path.join(sdir_, './assests/moose_icon_large.png' )
            )
    while True:                 # Event Loop  
        event, values = window.Read()  
        print(event, values)
        if event is None or event == 'Exit':  
            break  
        if event == 'Submit':  
            response = client.submit_job(values)
            if response is None:
                print( "[INFO ] Failed to recieve any data." )
            else:
                print( "[INFO ] All done. Viewing data..." )
                data, bzfile = response
                display_results( bzfile, window )
        else:
            print( 'Unsupported event' )

        for x in ['server', 'main_file', 'other_files']:
            window.FindElement(x).Update(values.get(x,''))

    window.Close()

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''GUI client for MOOSE.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', '-i', type=str
        , required = False, help = 'Input file'
        )
    parser.add_argument('--server', '-s'
        , required = False, default = 'ghevar.ncbs.res.in:31417'
        , help = 'MOOSE Server'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main(vars(args))
