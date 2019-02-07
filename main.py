# -*- coding: utf-8 -*-
from __future__ import division, print_function
    
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
import time
import screeninfo

if sys.version_info[0] >= 3:  
    import tkinter as TK
else:
    import Tkinter as TK

if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
else:  
    import PySimpleGUI27 as sg  

sdir_ = os.path.dirname( __file__ )

# set resolution.
try:
    from screeninfo import get_monitors
    m = get_monitors()[0]
    w_, h_ = int(m.width//1.2), int(m.height//1.5)
except Exception as e:
    w_, h_ = 1200, 900

# need a global because we don't want img_ to be garbage collected.
img_   = None

layout = [ 
        [sg.Text('Server Adress', size=(15,1))
            , sg.InputText('ghevar.ncbs.res.in:31417', key='server')]
        , [sg.Text('Main file'), sg.Input(key='main_file'), sg.FileBrowse()
            , sg.Checkbox('Upload directory?', key='upload_directory')
            ]
        , [sg.Text('Other files'), sg.Input(key='other_files'), sg.FilesBrowse()]
        , [sg.Canvas(size=(w_,h_), key='canvas')]
        # Output size is in chars x line 
        #, [sg.Output(key='output', size=(120,8))]
        , [sg.Submit(), sg.Exit()]
        ]

def draw_canvas(canvas, imgs):
    global img_
    global w_, h_
    if not isinstance(imgs, list):
        imgs = [ imgs ]
    for img in imgs:
        img_ = PIL.ImageTk.PhotoImage(img.resize((w_,h_)))
        canvas.TKCanvas.create_image(0, 0, anchor=TK.NW ,image=img_)
        time.sleep(1)

def display_results(bzfile, window):
    helper.log( "Displaying results saved in %s" % bzfile )
    cwd = os.path.dirname(bzfile)
    with tarfile.open(bzfile, 'r') as f:
        f.extractall(path=cwd)
    images = helper.find_images_pil(cwd)
    if len(images) > 0:
        draw_canvas(window.FindElement('canvas'), images)
    else:
        helper.log( "No images were returned by the server." )
        

def main(args):
    global sdir_
    global h_, w_
    window = sg.Window('MOOSE').Layout(layout).Finalize()

    if args['server']:
        window.FindElement('server').Update(args['server'])
    if args['input']:
        window.FindElement('main_file').Update(args['input'])

    draw_canvas( window.FindElement('canvas' )
            , PIL.Image.open(os.path.join(sdir_, './assests/moose_icon_large.png'))
            )

    while True:
        event, values = window.Read()  
        print(event, values)
        if event is None or event == 'Exit':  
            break  
        if event == 'Submit':  
            response = client.submit_job(values)
            if response is None:
                helper.log( "[INFO ] Failed to recieve any data." )
            else:
                data, bzfile = response
                helper.log( "All done. Recieved %s bytes of data." % len(data) )
                display_results( bzfile, window )
        else:
            helper.log( 'Unsupported event' )

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
