"""layout.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
    import tkinter as TK
else:  
    import PySimpleGUI27 as sg  
    import Tkinter as TK

import pathlib
import config
import PIL.ImageTk 
import PIL.Image
import time

# tabbed layout. One tab of interative window. Other for returned artifacts.
artifactTab = sg.Tab('Results From Server', [[sg.Canvas(size=(config.w_,config.h_), key='results')]])
currentTab = sg.Tab('Live Stream', [[sg.Canvas(size=(config.w_,config.h_), key='canvas')]])

layout = [ 
        [sg.Text('Server Adress', size=(15,1))
            , sg.InputText('ghevar.ncbs.res.in:31417', key='server')]
        , [sg.Text('Main file'), sg.Input(key='main_file'), sg.FileBrowse()
            , sg.Checkbox('Upload directory?', key='upload_directory')
            ]
        , [sg.Text('Other files'), sg.Input(key='other_files'), sg.FilesBrowse()]
        , [sg.TabGroup([[currentTab, artifactTab]])]
        # Output size is in chars x line 
        #, [sg.Output(key='output', size=(120,8))]
        , [sg.Submit(), sg.Exit()]
        ]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = { }

def draw_canvas(canvas, imgs):
    global images_
    if not isinstance(imgs, list):
        imgs = [ imgs ]
    for img in imgs:
        images_[canvas] = im = PIL.ImageTk.PhotoImage(img.resize((config.w_,config.h_)))
        canvas.TKCanvas.create_image(0, 0, anchor=TK.NW ,image=im)
        time.sleep(1)


mainWindow = sg.Window('MOOSE').Layout(layout).Finalize()
mooseLogoPath = pathlib.Path(pathlib.Path(__file__)).parent / pathlib.Path('./assests/moose_icon_large.png')

draw_canvas(mainWindow.FindElement('canvas'), PIL.Image.open(mooseLogoPath))
draw_canvas(mainWindow.FindElement('results'), PIL.Image.open(mooseLogoPath))

