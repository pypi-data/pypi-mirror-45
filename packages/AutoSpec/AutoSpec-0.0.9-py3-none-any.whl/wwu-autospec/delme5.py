#The controller runs the main thread controlling the program.
#It creates and starts a View object, which extends Thread and will show a pygame window.

dev=True
test=True
online=False
computer='new'

import os
import sys
import platform

from tkinter import *
from tkinter import messagebox
importlib=True
try:
    import importlib
except:
    importlib=False
import tkinter as tk
from tkinter import ttk
#import pygame
# try:
#     import pexpect
# except:
#     os.system('python -m pip install pexpect')
    
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import time
from threading import Thread
from tkinter.filedialog import *


import http.client as httplib

#Which computer are you using? This should probably be new. I don't know why you would use the old one.
computer='new'

#Figure out where this file is hanging out and tell python to look there for custom modules. This will depend on what operating system you are using.

global opsys
opsys=platform.system()
if opsys=='Darwin': opsys='Mac' #For some reason Macs identify themselves as Darwin. I don't know why but I think this is more intuitive.

global package_loc
package_loc=''

global CMDNUM
CMDNUM=0

global INTERVAL
INTERVAL=0.25

if opsys=='Windows':
    #If I am running this script from my IDE, __file__ is not defined. In that case, I'll get an exception, and I'll go with my own hard-coded file location instead.
    try:
        rel_package_loc='\\'.join(__file__.split('\\')[:-1])+'\\'
        if 'C:' in rel_package_loc:
            package_loc=rel_package_loc
        else: package_loc=os.getcwd()+'\\'+rel_package_loc
    except:
        print('Developer mode!')
        dev=True
        package_loc='C:\\Users\\hozak\\Python\\autospectroscopy\\'

elif opsys=='Linux':
    #If I am running this script from my IDE, __file__ is not defined. In that case, I'll get an exception, and I'll go with my own hard-coded file location instead.
    try:
        rel_package_loc='/'.join(__file__.split('/')[:-1])+'/'
        if rel_package_loc[0]=='/':
            package_loc=rel_package_loc
        else: package_loc=os.getcwd()+'/'+rel_package_loc
    except:
        print('Developer mode!')
        dev=True
        package_loc='/home/khoza/Python/WWU-AutoSpec/wwu-autospec/'
elif opsys=='Mac':
    try:
        rel_package_loc='/'.join(__file__.split('/')[:-1])+'/'
        if rel_package_loc[0]=='/':
            package_loc=rel_package_loc
        else: package_loc=os.getcwd()+'/'+rel_package_loc
    except:
        print('Developer mode!')
        dev=True
        package_loc='/home/khoza/Python/WWU-AutoSpec/wwu-autospec/'
    
sys.path.append(package_loc)

import goniometer_model
import goniometer_view
import plotter

#This is needed because otherwise changes won't show up until you restart the shell. Not needed if you aren't changing the modules.
if dev:
    try:
        importlib.reload(goniometer_model)
        from goniometer_model import Model
        importlib.reload(goniometer_view)
        from goniometer_view import View
        from goniometer_view import TestView
        importlib.reload(plotter)
        from plotter import Plotter
    except:
        print('Not reloading modules')
#Server and share location. Can change if spectroscopy computer changes.
server=''
global NUMLEN
global tk_master
tk_master=None

NUMLEN=500
if computer=='old':
    #Number of digits in spectrum number for spec save config
    NUMLEN=3
    #Time added to timeouts to account for time to read/write files
    BUFFER=15
    server='melissa' #old computer
elif computer=='new':
    #Number of digits in spectrum number for spec save config
    NUMLEN=5
    #Time added to timeouts to account for time to read/write files
    BUFFER=10
    server='geol-chzc5q2' #new computer

command_share='specshare'
command_share_Mac='SpecShare'
data_share='users' #Not used. Maybe later?
data_share_Mac='Users'

if opsys=='Linux':
    command_share_loc='/run/user/1000/gvfs/smb-share:server='+server+',share='+command_share+'/'
    data_share_loc='/run/user/1000/gvfs/smb-share:server='+server+',share='+data_share+'/'
    delimiter='/'
    write_command_loc=command_share_loc+'commands/from_control/'
    read_command_loc=command_share_loc+'commands/from_spec/'
    config_loc=package_loc+'config/'
    log_loc=package_loc+'log/'
elif opsys=='Windows':
    command_share_loc='\\\\'+server.upper()+'\\'+command_share+'\\'
    data_share_loc='\\\\'+server.upper()+'\\'+data_share+'\\'
    write_command_loc=command_share_loc+'commands\\from_control\\'
    read_command_loc=command_share_loc+'commands\\from_spec\\'
    config_loc=package_loc+'config\\'
    log_loc=package_loc+'log\\'
elif opsys=='Mac':
    command_share_loc='/Volumes/'+command_share_Mac+'/'
    data_share_loc='/Volumes/'+data_share_Mac+'/'
    delimiter='/'
    write_command_loc=command_share_loc+'commands/from_control/'
    read_command_loc=command_share_loc+'commands/from_spec/'
    config_loc=package_loc+'config/'
    log_loc=package_loc+'log/'
    
if not os.path.isdir(config_loc):
    print(config_loc)
    os.mkdir(config_loc)

def donothing():
    pass
def exit_func():
    print('exit!')
    exit()
    
def retry_func():
     os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
     
 

class ConnectionChecker():
    def __init__(self,dir,thread,controller=None, func=None):
        self.thread=thread
        self.dir=dir
        self.controller=controller
        self.func=func
        self.busy=False
    def alert_lost_connection(self, signum=None, frame=None):
        buttons={
            'retry':{
                self.release:[],
                self.check_connection:[False]
                },
            'exit':{
                exit_func:[]
            }
        }
        dialog=ErrorDialog(controller=self.controller, title='Lost Connection',label='Error: Lost connection with server.\n\nCheck you and the spectrometer computer are\nboth on the correct WiFi network and the\nserver is mounted on your computer',buttons=buttons)

    def alert_not_connected(self, signum=None, frame=None):
        buttons={
            'retry':{
                self.release:[],
                self.check_connection:[True]
                
                },
            'exit':{
                exit_func:[]
            }
        }
        dialog=Dialog(controller=self.controller, title='Not Connected',label='Error: No connection with server.\n\nCheck you and the spectrometer computer are\nboth on the correct WiFi network and the\nserver is mounted on your computer',buttons=buttons)
    def have_internet(self):
        conn = httplib.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def check_connection(self,firstconnection, attempt=0):
        if self.busy:
            return

            
        self.busy=True
        connected=True
        if self.have_internet()==False:
            connected=False
        else: 
            connected=os.path.isdir(self.dir)
        
        # This code doesn't work on windows.
        # if self.thread=='main':
        #     signal.signal(signal.SIGALRM, self.alert_not_connected)
        #     signal.alarm(2)
        #     # This may take a while to complete
        #     connected = os.path.isdir(self.dir)
        #     signal.alarm(0)          # Disable the alarm

        #   else:
        #     if self.have_internet()==False:
        #         connected=False
        #     else: 
        #         connected=os.path.isdir(self.dir)
                
        if connected==False:
            #For some reason reconnecting only seems to work on the second attempt. This seems like a pretty poor way to handle that, but I just call check_connection twice if it fails the first time.
            if attempt>0 and firstconnection==True:
                self.alert_not_connected(None, None)
            elif attempt>0 and firstconnection==False:
                self.alert_lost_connection(None, None)
            else:
                time.sleep(0.5)
                self.release()
                self.check_connection(firstconnection, attempt=1)
        else:
            if self.func !=None:
                self.func()
            self.release()
            return True
    def release(self):
        self.busy=False

def main():
    #Check if you are connected to the server. 
    connection_checker=ConnectionChecker(read_command_loc, thread='main', func=None)
    connection_checker.check_connection(True)

    #Clean out your read and write directories for commands. Prevents confusion based on past instances of the program.
    delme=os.listdir(write_command_loc)
    for file in delme:
        os.remove(write_command_loc+file)
    delme=os.listdir(read_command_loc)
    for file in delme:
        os.remove(read_command_loc+file)
    
    #Create a listener, which listens for commands, and a controller, which manages the model (which writes commands) and the view.
    spec_listener=SpecListener(read_command_loc)
    
    icon_loc=package_loc+'exception'#test_icon.xbm'
    control=Controller(spec_listener, command_share_loc, read_command_loc,write_command_loc, config_loc,data_share_loc,opsys, icon_loc)

class Controller():
    def __init__(self, spec_listener, command_share_loc, read_command_loc, write_command_loc, config_loc, data_share_loc,opsys,icon):
        self.listener=spec_listener
        self.listener.set_controller(self)
        self.listener.start()
        
        self.data_share_loc=data_share_loc
        self.read_command_loc=read_command_loc
        self.command_share_loc=command_share_loc
        self.write_command_loc=write_command_loc
        self.remote_directory_worker=RemoteDirectoryWorker(self.read_command_loc, self.write_command_loc, self.listener)
        
        self.config_loc=config_loc
        self.opsys=opsys
        self.log_filename=None
        
        #These will get set via user input.
        self.spec_save_path=''
        self.spec_basename=''
        self.spec_num=None
        self.spec_config_count=None
        self.take_spectrum_with_bad_i_or_e=False
        self.wr_time=None
        self.opt_time=None
        self.angles_change_time=None
        self.i=None
        self.e=None
        
        #Tkinter notebook GUI
        self.master=Tk()
        
        #view_frame=Frame(self.master)
        test_view=TestView(self.master)
        # frame=Frame(self.master)
        # frame.pack(side=RIGHT)
        # button=Button(frame, text=':D',command=test.draw_circle)
        # button.pack()
        
        self.tk_master=self.master
        self.notebook=ttk.Notebook(self.master)
        
        #The plotter, surprisingly, plots things.
        self.plotter=Plotter(self.master)
        
        #The view displays what the software thinks the goniometer is up to.
        self.view=View(self.master)
        self.view.start()
    
        #The model keeps track of the goniometer state and sends commands to the raspberry pi and spectrometer
        self.model=Model(self.view, self.plotter, self.write_command_loc, False, False)
        
        #Yay formatting. Might not work for Macs.
        self.bg='#555555'
        self.textcolor='light gray'
        self.buttontextcolor='white'
        bd=2
        padx=3
        pady=3
        border_color='light gray'
        button_width=15
        self.buttonbackgroundcolor='#888888'
        self.highlightbackgroundcolor='#222222'
        self.entry_background='light gray'
        self.listboxhighlightcolor='white'
        self.selectbackground='#555555'
        self.selectforeground='white'
        self.check_bg='#444444'
        
        self.master.configure(background = self.bg)
        self.master.title('Control')

        # img = PhotoImage(file=icon)
        # print(type(img))
        # self.master.tk.call('wm', 'iconphoto', self.master._w, img)
        try:
            self.master.wm_iconbitmap('@'+icon)
        except:
            pass

    
        #If the user has saved spectra with this program before, load in their previously used directories.
        input_dir=''
        output_dir=''
        try:
            with open(self.config_loc+'process_directories.txt','r') as process_config:
                input_dir=process_config.readline().strip('\n')
                output_dir=process_config.readline().strip('\n')
        except:
            with open(self.config_loc+'process_directories.txt','w+') as f:
                f.write('C:\\Users\n')
                f.write('C:\\Users\n')

            input_dir='C:\\Users'
            output_dir='C:\\Users'
    
        try:
            with open(self.config_loc+'spec_save.txt','r') as spec_save_config:
                self.spec_save_path=spec_save_config.readline().strip('\n')
                self.spec_basename=spec_save_config.readline().strip('\n')
                self.spec_startnum=str(int(spec_save_config.readline().strip('\n'))+1)
                while len(self.spec_startnum)<NUMLEN:
                    self.spec_startnum='0'+self.spec_startnum
        except:
            with open(self.config_loc+'spec_save.txt','w+') as f:
                f.write('C:\\Users\n')
                f.write('basename\n')
                f.write('-1\n')

                self.spec_save_path='C:\\Users'
                self.spec_basename='basename'
                self.spec_startnum='0'
                while len(self.spec_startnum)<NUMLEN:
                    self.spec_startnum='0'+self.spec_startnum

        self.control_frame=Frame(self.notebook, bg=self.bg)
        self.control_frame.pack()
        self.save_config_frame=Frame(self.control_frame,bg=self.bg,highlightthickness=1)
        self.save_config_frame.pack(fill=BOTH,expand=True)
        self.spec_save_label=Label(self.save_config_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Spectra save configuration:')
        self.spec_save_label.pack(pady=(15,5))
        self.spec_save_path_label=Label(self.save_config_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Directory:')
        self.spec_save_path_label.pack(padx=padx)
        
        self.spec_save_dir_frame=Frame(self.save_config_frame,bg=self.bg)
        self.spec_save_dir_frame.pack()
        
        self.spec_save_dir_browse_button=Button(self.spec_save_dir_frame,text='Browse',command=self.choose_spec_save_dir)
        self.spec_save_dir_browse_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.spec_save_dir_browse_button.pack(side=RIGHT, padx=padx)
        
        self.spec_save_dir_var = StringVar()
        self.spec_save_dir_var.trace('w', self.validate_spec_save_dir)
        self.spec_save_dir_entry=Entry(self.spec_save_dir_frame, width=50,bd=bd,bg=self.entry_background, selectbackground=self.selectbackground,selectforeground=self.selectforeground,textvariable=self.spec_save_dir_var)
        self.spec_save_dir_entry.insert(0, self.spec_save_path)
        self.spec_save_dir_entry.pack(padx=padx, pady=pady, side=RIGHT)
        self.spec_save_frame=Frame(self.save_config_frame, bg=self.bg)
        self.spec_save_frame.pack()
        
        self.spec_basename_label=Label(self.spec_save_frame,pady=pady,bg=self.bg,fg=self.textcolor,text='Base name:')
        self.spec_basename_label.pack(side=LEFT,pady=(5,15),padx=(0,0))
        
        self.spec_basename_var = StringVar()
        self.spec_basename_var.trace('w', self.validate_basename)
        self.spec_basename_entry=Entry(self.spec_save_frame, width=10,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground,textvariable=self.spec_basename_var)
        self.spec_basename_entry.pack(side=LEFT,padx=(5,5), pady=pady)
        self.spec_basename_entry.insert(0,self.spec_basename)
        

        
        self.spec_startnum_label=Label(self.spec_save_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Number:')
        self.spec_startnum_label.pack(side=LEFT,pady=pady)
        
        self.startnum_var = StringVar()
        self.startnum_var.trace('w', self.validate_startnum)
        self.spec_startnum_entry=Entry(self.spec_save_frame, width=10,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground,textvariable=self.startnum_var)
        self.spec_startnum_entry.insert(0,self.spec_startnum)
        self.spec_startnum_entry.pack(side=RIGHT, pady=pady)      
        

            
        self.log_frame=Frame(self.control_frame, bg=self.bg,highlightthickness=1)
        self.log_frame.pack(fill=BOTH,expand=True)
        self.logfile_label=Label(self.log_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Log file:')
        self.logfile_label.pack(padx=padx,pady=(10,0))
        self.logfile_entry_frame=Frame(self.log_frame, bg=self.bg)
        self.logfile_entry_frame.pack()
        
        self.logfile_var = StringVar()
        self.logfile_var.trace('w', self.validate_logfile)
        self.logfile_entry=Entry(self.logfile_entry_frame, width=50,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground,textvariable=self.logfile_var)
        self.logfile_entry.pack(padx=padx, pady=(5,15))
        self.logfile_entry.enabled=False
        

        
        self.select_logfile_button=Button(self.logfile_entry_frame, fg=self.textcolor,text='Select existing',command=self.chooselogfile, width=13, height=1,bg=self.buttonbackgroundcolor)
        self.select_logfile_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor)
        self.select_logfile_button.pack(side=LEFT,padx=(50,5), pady=(0,10))
        
        self.new_logfile_button=Button(self.logfile_entry_frame, fg=self.textcolor,text='New log file',command=self.newlog, width=13, height=1)
        self.new_logfile_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.new_logfile_button.pack(side=LEFT,padx=padx, pady=(0,10))
        
        self.spec_save_config=IntVar()
        self.spec_save_config_check=Checkbutton(self.save_config_frame, fg=self.textcolor,text='Save file configuration', bg=self.bg, pady=pady,highlightthickness=0, variable=self.spec_save_config, selectcolor=self.check_bg)
        #self.spec_save_config_check.pack(pady=(0,5))
        self.spec_save_config_check.select()
        
        self.spectrum_settings_frame=Frame(self.control_frame,bg=self.bg, highlightcolor="green", highlightthickness=1)
        self.spectrum_settings_frame.pack(fill=BOTH,expand=True)
        self.spec_settings_label=Label(self.spectrum_settings_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Settings for this spectrum:')
        self.spec_settings_label.pack(padx=padx,pady=(10,0))
        
        
        self.instrument_config_frame=Frame(self.spectrum_settings_frame, bg=self.bg, highlightthickness=1)
        self.spec_settings_label=Label(self.instrument_config_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Instrument Configuration:')
        self.spec_settings_label.pack(padx=padx,pady=(10,0))
        self.instrument_config_frame.pack(pady=(15,15), fill=BOTH, expand=True)
        self.instrument_config_label=Label(self.instrument_config_frame, fg=self.textcolor,text='Number of spectra to average:', bg=self.bg)
        self.instrument_config_label.pack(side=LEFT)
        self.instrument_config_entry=Entry(self.instrument_config_frame, width=10, bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.instrument_config_entry.insert(0, 5)
        self.instrument_config_entry.pack(side=LEFT)

        
        self.spectrum_angles_frame=Frame(self.spectrum_settings_frame, bg=self.bg)
        self.spectrum_angles_frame.pack()
        self.man_incidence_label=Label(self.spectrum_angles_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Incidence angle:')
        self.man_incidence_label.pack(side=LEFT, padx=padx,pady=(0,8))
        self.man_incidence_entry=Entry(self.spectrum_angles_frame, width=10, bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.man_incidence_entry.pack(side=LEFT)
        self.man_emission_label=Label(self.spectrum_angles_frame, padx=padx,pady=pady,bg=self.bg, fg=self.textcolor,text='Emission angle:')
        self.man_emission_label.pack(side=LEFT, padx=(10,0))
        self.man_emission_entry=Entry(self.spectrum_angles_frame, width=10, bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.man_emission_entry.pack(side=LEFT, padx=(0,20))
        

        self.label_label=Label(self.spectrum_settings_frame, padx=padx,pady=pady,bg=self.bg, fg=self.textcolor,text='Label:')
        self.label_label.pack()
        self.label_entry=Entry(self.spectrum_settings_frame, width=50, bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.label_entry.pack(pady=(0,15))
        
        self.top_frame=Frame(self.control_frame,padx=padx,pady=pady,bd=2,highlightbackground=border_color,highlightcolor=border_color,highlightthickness=0,bg=self.bg)
        #self.top_frame.pack()
        self.light_frame=Frame(self.top_frame,bg=self.bg)
        self.light_frame.pack(side=LEFT)
        self.light_label=Label(self.light_frame,padx=padx, pady=pady,bg=self.bg,fg=self.textcolor,text='Light Source')
        self.light_label.pack()
        
        light_labels_frame = Frame(self.light_frame,bg=self.bg,padx=padx,pady=pady)
        light_labels_frame.pack(side=LEFT)
        
        light_start_label=Label(light_labels_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Start:')
        light_start_label.pack(pady=(0,8))
        #light_end_label=Label(light_labels_frame,bg=self.bg,padx=padx,pady=pady,fg=self.textcolor,text='End:',fg='lightgray')
        #light_end_label.pack(pady=(0,5))
    
        #light_increment_label=Label(light_labels_frame,bg=self.bg,padx=padx,pady=pady,fg=self.textcolor,text='Increment:',fg='lightgray')
       # light_increment_label.pack(pady=(0,5))
    
        
        light_entries_frame=Frame(self.light_frame,bg=self.bg,padx=padx,pady=pady)
        light_entries_frame.pack(side=RIGHT)
        
        light_start_entry=Entry(light_entries_frame,width=10, bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        light_start_entry.pack(padx=padx,pady=pady)
        light_start_entry.insert(0,'10')
        
        light_end_entry=Entry(light_entries_frame,width=10, highlightbackground='white', bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        light_end_entry.pack(padx=padx,pady=pady)    
        light_increment_entry=Entry(light_entries_frame,width=10,highlightbackground='white', bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        light_increment_entry.pack(padx=padx,pady=pady)
        
        detector_frame=Frame(self.top_frame,bg=self.bg)
        detector_frame.pack(side=RIGHT)
        
        detector_label=Label(detector_frame,padx=padx, pady=pady,bg=self.bg,fg=self.textcolor,text='Detector')
        detector_label.pack()
        
        detector_labels_frame = Frame(detector_frame,bg=self.bg,padx=padx,pady=pady)
        detector_labels_frame.pack(side=LEFT)
        
        detector_start_label=Label(detector_labels_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Start:')
        detector_start_label.pack(pady=(0,8))
        #detector_end_label=Label(detector_labels_frame,bg=self.bg,padx=padx,pady=pady,fg=self.textcolor,text='End:',fg='lightgray')
        #detector_end_label.pack(pady=(0,5))
    
        #detector_increment_label=Label(detector_labels_frame,bg=self.bg,padx=padx,pady=pady,fg=self.textcolor,text='Increment:',fg='lightgray')
        #detector_increment_label.pack(pady=(0,5))
    
        
        detector_entries_frame=Frame(detector_frame,bg=self.bg,padx=padx,pady=pady)
        detector_entries_frame.pack(side=RIGHT)
        detector_start_entry=Entry(detector_entries_frame,bd=bd,width=10,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        detector_start_entry.pack(padx=padx,pady=pady)
        detector_start_entry.insert(0,'0')
        
        detector_end_entry=Entry(detector_entries_frame,bd=bd,width=10,highlightbackground='white',bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        detector_end_entry.pack(padx=padx,pady=pady)
        
        detector_increment_entry=Entry(detector_entries_frame,bd=bd,width=10, highlightbackground='white',bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        detector_increment_entry.pack(padx=padx,pady=pady)
        
        self.auto_check_frame=Frame(self.control_frame, bg=self.bg)
        self.auto_process=IntVar()
        self.auto_process_check=Checkbutton(self.auto_check_frame, fg=self.textcolor,text='Process data', bg=self.bg, highlightthickness=0,selectcolor=self.check_bg)
        self.auto_process_check.pack(side=LEFT)
        
        self.auto_plot=IntVar()
        self.auto_plot_check=Checkbutton(self.auto_check_frame, fg=self.textcolor,text='Plot spectra', bg=self.bg, highlightthickness=0,selectcolor=self.check_bg)
        self.auto_plot_check.pack(side=LEFT)
        
        self.gen_frame=Frame(self.control_frame, bg=self.bg,highlightthickness=1)
        self.gen_frame.pack(fill=BOTH,expand=True)
        self.action_button_frame=Frame(self.gen_frame, bg=self.bg)
        self.action_button_frame.pack()
        
        button_width=20
        self.opt_button=Button(self.action_button_frame, fg=self.textcolor,text='Optimize', padx=padx, pady=pady,width=button_width, bg='light gray', command=self.opt, height=2)
        self.opt_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.opt_button.pack(padx=padx,pady=pady, side=LEFT)
        self.wr_button=Button(self.action_button_frame, fg=self.textcolor,text='White Reference', padx=padx, pady=pady, width=button_width, bg='light gray', command=self.wr, height=2)
        self.wr_button.pack(padx=padx,pady=pady, side=LEFT)
        self.wr_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
    
        self.go_button=Button(self.action_button_frame, fg=self.textcolor,text='Take Spectrum', padx=padx, pady=pady, width=button_width,height=2,bg='light gray', command=self.go)
        self.go_button.pack(padx=padx,pady=pady, side=LEFT)
        self.go_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        
        #***************************************************************
        # Frame for settings
        
        self.dumb_frame=Frame(self.notebook, bg=self.bg, pady=2*pady)
        self.dumb_frame.pack()
        # entries_frame=Frame(man_frame, bg=self.bg)
        # entries_frame.pack(fill=BOTH, expand=True)
        # man_light_label=Label(entries_frame,padx=padx, pady=pady,bg=self.bg,fg=self.textcolor,text='Instrument positions:')
        # man_light_label.pack()
        # man_light_label=Label(entries_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Incidence:')
        # man_light_label.pack(side=LEFT, padx=(30,5),pady=(0,8))
        # man_light_entry=Entry(entries_frame, width=10)
        # man_light_entry.insert(0,'10')
        # man_light_entry.pack(side=LEFT)
        # man_detector_label=Label(entries_frame, padx=padx,pady=pady,bg=self.bg, fg=self.textcolor,text='Emission:')
        # man_detector_label.pack(side=LEFT, padx=(10,0))
        # man_detector_entry=Entry(entries_frame, width=10,fg=self.textcolor,text='0')
        # man_detector_entry.insert(0,'10')
        # man_detector_entry.pack(side=LEFT)

        # self.instrument_config_title_frame=Frame(self.dumb_frame, bg=self.bg)
        # self.instrument_config_title_frame.pack(pady=pady)
        # self.instrument_config_label0=Label(self.instrument_config_title_frame, fg=self.textcolor,text='Instrument Configuration:                                ', bg=self.bg)
        # self.instrument_config_label0.pack(side=LEFT)

        
        self.automation_title_frame=Frame(self.dumb_frame, bg=self.bg)
        self.automation_title_frame.pack(pady=pady)
        self.automation_label0=Label(self.automation_title_frame, fg=self.textcolor,text='Automation:                                               ', bg=self.bg)
        self.automation_label0.pack(side=LEFT)
        
        
        self.auto_check_frame=Frame(self.dumb_frame, bg=self.bg)
        self.auto_check_frame.pack()
        self.auto=IntVar()
        self.auto_check=Checkbutton(self.auto_check_frame, fg=self.textcolor,text='Automatically iterate through viewing geometries', bg=self.bg, pady=pady,highlightthickness=0, variable=self.auto, command=self.auto_cycle_check,selectcolor=self.check_bg)
        self.auto_check.pack(side=LEFT, pady=pady)
        
        self.timer_title_frame=Frame(self.dumb_frame, bg=self.bg)
        self.timer_title_frame.pack(pady=(10,0))
        self.timer_label0=Label(self.timer_title_frame, fg=self.textcolor,text='Timer:                                                   ', bg=self.bg)
        self.timer_label0.pack(side=LEFT)
        self.timer_frame=Frame(self.dumb_frame, bg=self.bg, pady=pady)
        self.timer_frame.pack()
        self.timer_check_frame=Frame(self.timer_frame, bg=self.bg)
        self.timer_check_frame.pack(pady=pady)
        self.timer=IntVar()
        self.timer_check=Checkbutton(self.timer_check_frame, fg=self.textcolor,text='Collect sets of spectra using a timer           ', bg=self.bg, pady=pady,highlightthickness=0, variable=self.timer,selectcolor=self.check_bg)
        self.timer_check.pack(side=LEFT, pady=pady)
        
        self.timer_duration_frame=Frame(self.timer_frame, bg=self.bg)
        self.timer_duration_frame.pack()
        self.timer_spectra_label=Label(self.timer_duration_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Total duration (min):')
        self.timer_spectra_label.pack(side=LEFT, padx=padx,pady=(0,8))
        self.timer_spectra_entry=Entry(self.timer_duration_frame, bd=1,width=10,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.timer_spectra_entry.pack(side=LEFT)
        self.filler_label=Label(self.timer_duration_frame,bg=self.bg,fg=self.textcolor,text='              ')
        self.filler_label.pack(side=LEFT)
        
        self.timer_interval_frame=Frame(self.timer_frame, bg=self.bg)
        self.timer_interval_frame.pack()
        self.timer_interval_label=Label(self.timer_interval_frame, padx=padx,pady=pady,bg=self.bg, fg=self.textcolor,text='Interval (min):')
        self.timer_interval_label.pack(side=LEFT, padx=(10,0))
        self.timer_interval_entry=Entry(self.timer_interval_frame,bd=bd,width=10,fg=self.textcolor,text='0',bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
    # self.timer_interval_entry.insert(0,'-1')
        self.timer_interval_entry.pack(side=LEFT, padx=(0,20))
        self.filler_label=Label(self.timer_interval_frame,bg=self.bg,fg=self.textcolor,text='                   ')
        self.filler_label.pack(side=LEFT)
        
        self.failsafe_title_frame=Frame(self.dumb_frame, bg=self.bg)
        self.failsafe_title_frame.pack(pady=(10,0))
        self.failsafe_label0=Label(self.failsafe_title_frame, fg=self.textcolor,text='Failsafes:                                              ', bg=self.bg)
        self.failsafe_label0.pack(side=LEFT)
        self.failsafe_frame=Frame(self.dumb_frame, bg=self.bg, pady=pady)
        self.failsafe_frame.pack(pady=pady)

        
        self.wrfailsafe=IntVar()
        self.wrfailsafe_check=Checkbutton(self.failsafe_frame, fg=self.textcolor,text='Prompt if no white reference has been taken.    ', bg=self.bg, pady=pady,highlightthickness=0, variable=self.wrfailsafe,selectcolor=self.check_bg)
        self.wrfailsafe_check.pack()#side=LEFT, pady=pady)
        self.wrfailsafe_check.select()
        
        self.wr_timeout_frame=Frame(self.failsafe_frame, bg=self.bg)
        self.wr_timeout_frame.pack(pady=(0,10))
        self.wr_timeout_label=Label(self.wr_timeout_frame, fg=self.textcolor,text='Timeout (minutes):', bg=self.bg)
        self.wr_timeout_label.pack(side=LEFT, padx=(10,0))
        self.wr_timeout_entry=Entry(self.wr_timeout_frame, bd=bd,width=10,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.wr_timeout_entry.pack(side=LEFT, padx=(0,20))
        self.wr_timeout_entry.insert(0,'8')
        self.filler_label=Label(self.wr_timeout_frame,bg=self.bg,fg=self.textcolor,text='              ')
        self.filler_label.pack(side=LEFT)
        
        
        self.optfailsafe=IntVar()
        self.optfailsafe_check=Checkbutton(self.failsafe_frame, fg=self.textcolor,text='Prompt if the instrument has not been optimized.', bg=self.bg, pady=pady,highlightthickness=0,selectcolor=self.check_bg, variable=self.optfailsafe)
        self.optfailsafe_check.pack()#side=LEFT, pady=pady)
        self.optfailsafe_check.select()
        
        self.opt_timeout_frame=Frame(self.failsafe_frame, bg=self.bg)
        self.opt_timeout_frame.pack()
        self.opt_timeout_label=Label(self.opt_timeout_frame, fg=self.textcolor,text='Timeout (minutes):', bg=self.bg)
        self.opt_timeout_label.pack(side=LEFT, padx=(10,0))
        self.opt_timeout_entry=Entry(self.opt_timeout_frame,bd=bd, width=10,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.opt_timeout_entry.pack(side=LEFT, padx=(0,20))
        self.opt_timeout_entry.insert(0,'60')
        self.filler_label=Label(self.opt_timeout_frame,bg=self.bg,fg=self.textcolor,text='              ')
        self.filler_label.pack(side=LEFT)
        
        self.anglesfailsafe=IntVar()
        self.anglesfailsafe_check=Checkbutton(self.failsafe_frame, fg=self.textcolor,text='Check validity of emission and incidence angles.', bg=self.bg, pady=pady,highlightthickness=0,selectcolor=self.check_bg, variable=self.anglesfailsafe)
        self.anglesfailsafe_check.pack(pady=(6,5))#side=LEFT, pady=pady)
        self.anglesfailsafe_check.select()
        
        self.labelfailsafe=IntVar()
        self.labelfailsafe_check=Checkbutton(self.failsafe_frame, fg=self.textcolor,text='Require a label for each spectrum.', bg=self.bg, pady=pady,highlightthickness=0, selectcolor=self.check_bg,variable=self.labelfailsafe)
        self.labelfailsafe_check.pack(pady=(6,5))#side=LEFT, pady=pady)
        self.labelfailsafe_check.select()
        
        self.anglechangefailsafe=IntVar()
        self.anglechangefailsafe_check=Checkbutton(self.failsafe_frame, selectcolor=self.check_bg,fg=self.textcolor,text='Remind me to check the goniometer if\nincidence and/or emission angles change.', bg=self.bg, pady=pady,highlightthickness=0, variable=self.anglechangefailsafe)
        self.anglechangefailsafe_check.pack(pady=(6,5))#side=LEFT, pady=pady)
        self.anglechangefailsafe_check.select()
        
        self.wr_anglesfailsafe=IntVar()
        self.wr_anglesfailsafe_check=Checkbutton(self.failsafe_frame,selectcolor=self.check_bg, fg=self.textcolor,text='Require a new white reference at each viewing geometry', bg=self.bg, pady=pady, highlightthickness=0, variable=self.wr_anglesfailsafe)
        self.wr_anglesfailsafe_check.pack(pady=(6,5))
        self.wr_anglesfailsafe_check.select()
        
        
        # check_frame=Frame(man_frame, bg=self.bg)
        # check_frame.pack()
        # process=IntVar()
        # process_check=Checkbutton(check_frame, fg=self.textcolor,text='Process data', bg=self.bg, pady=pady,highlightthickness=0)
        # process_check.pack(side=LEFT, pady=(5,15))
        # 
        # plot=IntVar()
        # plot_check=Checkbutton(check_frame, fg=self.textcolor,text='Plot spectrum', bg=self.bg, pady=pady,highlightthickness=0)
        # plot_check.pack(side=LEFT, pady=(5,15))
    
        #   move_button=Button(man_frame, fg=self.textcolor,text='Move', padx=padx, pady=pady, width=int(button_width*1.6),bg='light gray', command=go)
        # move_button.pack(padx=padx,pady=pady, side=LEFT)
        # spectrum_button=Button(man_frame, fg=self.textcolor,text='Collect data', padx=padx, pady=pady, width=int(button_width*1.6), bg='light gray', command=take_spectrum)
        # spectrum_button.pack(padx=padx,pady=pady, side=LEFT)
        
    
        #********************** Process frame ******************************
    
        self.process_frame=Frame(self.notebook, bg=self.bg, pady=2*pady)
        self.process_frame.pack()

        self.input_dir_label=Label(self.process_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Input directory:')
        self.input_dir_label.pack(padx=padx,pady=pady)
        
        self.input_frame=Frame(self.process_frame, bg=self.bg)
        self.input_frame.pack()
        
        self.process_input_browse_button=Button(self.input_frame,text='Browse',command=self.choose_process_input_dir)
        self.process_input_browse_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.process_input_browse_button.pack(side=RIGHT, padx=padx)
        
        
        self.input_dir_var = StringVar()
        self.input_dir_var.trace('w', self.validate_input_dir)
         
        self.input_dir_entry=Entry(self.input_frame, width=50,bd=bd, textvariable=self.input_dir_var,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.input_dir_entry.insert(0, input_dir)
        self.input_dir_entry.pack(side=RIGHT,padx=padx)
        

        self.output_dir_label=Label(self.process_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Output directory:')
        self.output_dir_label.pack(padx=padx,pady=pady)
        
        self.output_frame=Frame(self.process_frame, bg=self.bg)
        self.output_frame.pack()
        self.process_output_browse_button=Button(self.output_frame,text='Browse',command=self.choose_process_output_dir)
        self.process_output_browse_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.process_output_browse_button.pack(side=RIGHT, padx=padx)
        
        self.output_dir_entry=Entry(self.output_frame, width=50,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.output_dir_entry.insert(0, output_dir)
        self.output_dir_entry.pack(side=RIGHT,padx=padx)
        
        self.output_file_frame=Frame(self.process_frame, bg=self.bg)
        self.output_file_frame.pack()
        self.output_file_label=Label(self.process_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Output file name:')
        self.output_file_label.pack(padx=padx,pady=pady)
        self.output_file_entry=Entry(self.process_frame, width=50,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.output_file_entry.pack()
        
        
        self.process_check_frame=Frame(self.process_frame, bg=self.bg)
        self.process_check_frame.pack(pady=(15,5))
        self.process_save_dir=IntVar()
        self.process_save_dir_check=Checkbutton(self.process_check_frame, selectcolor=self.check_bg,fg=self.textcolor,text='Save file configuration', bg=self.bg, pady=pady,highlightthickness=0, variable=self.process_save_dir)
        self.process_save_dir_check.pack(side=LEFT, pady=(5,15))
        self.process_save_dir_check.select()
        # self.process_plot=IntVar()
        # self.process_plot_check=Checkbutton(self.process_check_frame, fg=self.textcolor,text='Plot spectra', bg=self.bg, pady=pady,highlightthickness=0)
        # self.process_plot_check.pack(side=LEFT, pady=(5,15))
        
        self.process_button=Button(self.process_frame, fg=self.textcolor,text='Process', padx=padx, pady=pady, width=int(button_width*1.6),bg='light gray', command=self.process_cmd)
        self.process_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.process_button.pack()
        
        # 
        # #********************** Goniometer control frame ******************************
        # 
        # self.gon_control_frame=Frame(self.notebook, bg=self.bg, pady=2*pady)
        # self.gon_control_frame.pack()
        # 
        # self.plot_title_label=Label(self.plot_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Plot title:')
        # self.plot_title_label.pack(padx=padx,pady=(15,5))
        # self.plot_title_entry=Entry(self.plot_frame, width=50,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        # self.plot_title_entry.pack(pady=(5,20))
        
        #********************** Plot frame ******************************
        
        self.plot_frame=Frame(self.notebook, bg=self.bg, pady=2*pady)
        self.plot_frame.pack()
        
        self.plot_title_label=Label(self.plot_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Plot title:')
        self.plot_title_label.pack(padx=padx,pady=(15,5))
        self.plot_title_entry=Entry(self.plot_frame, width=50,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.plot_title_entry.pack(pady=(5,20))


        
        self.local_remote_frame=Frame(self.plot_frame, bg=self.bg)
        self.local_remote_frame.pack()
        
        self.plot_input_dir_label=Label(self.local_remote_frame,padx=padx,pady=pady,bg=self.bg,fg=self.textcolor,text='Path to .tsv file:')
        self.plot_input_dir_label.pack(side=LEFT,padx=padx,pady=pady)
        
        self.local=IntVar()
        self.local_check=Checkbutton(self.local_remote_frame, fg=self.textcolor,text=' Local',selectcolor=self.check_bg, bg=self.bg, pady=pady, variable=self.local,highlightthickness=0, highlightbackground=self.bg,command=self.local_plot_cmd)
        self.local_check.pack(side=LEFT,pady=(5,5),padx=(5,5))

        
        self.remote=IntVar()
        self.remote_check=Checkbutton(self.local_remote_frame, fg=self.textcolor,text=' Remote', bg=self.bg, pady=pady,highlightthickness=0, variable=self.remote, command=self.remote_plot_cmd,selectcolor=self.check_bg)
        self.remote_check.pack(side=LEFT, pady=(5,5),padx=(5,5))
        self.remote_check.select()
        

        self.plot_file_frame=Frame(self.plot_frame, bg=self.bg)
        self.plot_file_frame.pack(pady=(5,10))
        self.plot_file_browse_button=Button(self.plot_file_frame,text='Browse',command=self.choose_plot_file)
        self.plot_file_browse_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.plot_file_browse_button.pack(side=RIGHT, padx=padx)
        
        self.plot_input_dir_entry=Entry(self.plot_file_frame, width=50,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.plot_input_dir_entry.insert(0, input_dir)
        self.plot_input_dir_entry.pack(side=RIGHT)
        
        # self.no_wr_frame=Frame(self.plot_frame, bg=self.bg)
        # self.no_wr_frame.pack()

        

                
        self.load_labels_frame=Frame(self.plot_frame, bg=self.bg)
        self.load_labels_frame.pack()
        self.load_labels=IntVar()
        self.load_labels_check=Checkbutton(self.load_labels_frame, selectcolor=self.check_bg,fg=self.textcolor,text='Load labels from log file', bg=self.bg, pady=pady,highlightthickness=0, variable=self.load_labels, command=self.load_labels_cmd)
        self.load_labels_check.pack(pady=(5,5))
        
        self.plot_logfile_frame=Frame(self.plot_frame, bg=self.bg)
        self.plot_logfile_frame.pack()
        self.select_plot_logfile_button=Button(self.plot_logfile_frame, fg=self.textcolor,text='Browse',command=self.chooseplotlogfile, height=1,bg=self.buttonbackgroundcolor)
        self.select_plot_logfile_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor)
        self.plot_logfile_entry=Entry(self.plot_logfile_frame, width=50,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        
        self.no_wr=IntVar()
        self.no_wr_check=Checkbutton(self.plot_frame,selectcolor=self.check_bg, fg=self.textcolor,text='Exclude white references', bg=self.bg, pady=pady,highlightthickness=0, variable=self.no_wr, command=self.no_wr_cmd)
        self.no_wr_check.pack(pady=(5,5))
        self.no_wr_check.select()
        

        
        
        #self.load_labels_entry.pack()
        
        
        # pr_check_frame=Frame(self.process_frame, bg=self.bg)
        # self.process_check_frame.pack(pady=(15,5))
        # self.process_save_dir=IntVar()
        # self.process_save_dir_check=Checkbutton(self.process_check_frame, fg=self.textcolor,text='Save file configuration', bg=self.bg, pady=pady,highlightthickness=0, variable=self.process_save_dir)
        # self.process_save_dir_check.pack(side=LEFT, pady=(5,15))
        # self.process_save_dir_check.select()
        # self.process_plot=IntVar()
        # self.process_plot_check=Checkbutton(self.process_check_frame, fg=self.textcolor,text='Plot spectra', bg=self.bg, pady=pady,highlightthickness=0)
        # self.process_plot_check.pack(side=LEFT, pady=(5,15))
        
        self.plot_button=Button(self.plot_frame, fg=self.textcolor,text='Plot', padx=padx, pady=pady, width=int(button_width*1.6),bg='light gray', command=self.plot)
        self.plot_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.plot_button.pack(pady=(20,20))
    
        #************************Console********************************
        self.console_frame=Frame(self.notebook, bg=self.bg)
        self.console_frame.pack(fill=BOTH, expand=True)
        self.text_frame=Frame(self.console_frame)
        self.scrollbar = Scrollbar(self.text_frame)
        self.notebook_width=self.notebook.winfo_width()
        self.notebook_height=self.notebook.winfo_width()
        self.console_log = Text(self.text_frame, width=self.notebook_width,bg=self.bg, fg=self.textcolor)
        self.scrollbar.pack(side=RIGHT, fill=Y)
    
        self.scrollbar.config(command=self.console_log.yview)
        self.console_log.configure(yscrollcommand=self.scrollbar.set)
        self.console_entry=Entry(self.console_frame, width=self.notebook_width,bd=bd,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.console_entry.bind("<Return>",self.run)
        self.console_entry.bind('<Up>',self.run)
        self.console_entry.bind('<Down>',self.run)
        self.console_entry.pack(fill=BOTH, side=BOTTOM)
        self.text_frame.pack(fill=BOTH, expand=True)
        self.console_log.pack(fill=BOTH,expand=True)
        self.console_entry.focus()
    
        self.notebook.add(self.control_frame, text='Spectrometer control')
        self.notebook.add(self.dumb_frame, text='Settings')
        self.notebook.add(self.process_frame, text='Data processing')
        self.notebook.add(self.plot_frame, text='Plot')
        self.notebook.add(self.console_frame,text='Console')
        #self.notebook.add(val_frame, fg=self.textcolor,text='Validation tools')
        #checkbox: Iterate through a range of geometries
        #checkbox: Choose a single geometry
        #checkbox: Take one spectrum
        #checkbox: Use a self.timer to collect a series of spectra
        #self.timer interval: 
        #Number of spectra to collect:
        self.notebook.pack(fill=BOTH, expand=True)
        

        #test=TestView(self.master)
        frame=Frame(self.control_frame)
        frame.pack()
        button=Button(frame, text=':D',command=test_view.draw_circle)
        button.pack()
        test_view.run()
        
        #self.view.join()
    def local_plot_cmd(self):
        if self.local.get() and not self.remote.get():
            return
        elif self.remote.get() and not self.local.get():
            return
        elif not self.remote.get():
            self.remote_check.select()
        else:
            self.remote_check.deselect()
        
    def remote_plot_cmd(self):
        if self.local.get() and not self.remote.get():
            return
        elif self.remote.get() and not self.local.get():
            return
        elif not self.local.get():
            self.local_check.select()
        else:
            self.local_check.deselect()
        
    def no_wr_cmd(self):
        pass
        
    def load_labels_cmd(self):
        if self.load_labels.get():
            self.select_plot_logfile_button.pack(side=RIGHT,padx=(5,2), pady=(0,0))
            self.plot_logfile_entry.pack(side=RIGHT)

            if self.plot_logfile_entry.get()=='':
                try:
                    self.plot_logfile_entry.insert(0,self.log_filename)
                except:
                    print('no log file')
        else:
            self.plot_logfile_entry.pack_forget()
            self.select_plot_logfile_button.pack_forget()

    def chooseplotlogfile(self):
        filename = askopenfilename(initialdir=log_loc,title='Select log file to load labels from')
        self.plot_logfile_entry.delete(0,'end')
        self.plot_logfile_entry.insert(0, filename)  
        

              
    def chooselogfile(self):
        self.log_filename = askopenfilename(initialdir=log_loc,title='Select existing log file to append to')
        self.logfile_entry.delete(0,'end')
        self.logfile_entry.insert(0, self.log_filename)

        # with open(self.log_filename,'w+') as log:
        #     log.write(str(datetime.datetime.now())+'\n')
        
    def newlog(self):
        try:
            log = asksaveasfile(mode='w', defaultextension=".txt",title='Create a new log file')
        except:
            pass
        if log is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.log_filename=log.name
        log.write(str(datetime.datetime.now())+'\n')
        self.logfile_entry.delete(0,'end')
        self.logfile_entry.insert(0, self.log_filename)
        
    def go(self):    
        if not self.auto.get():
            self.take_spectrum()

        else:
            incidence={'start':-1,'end':-1,'increment':-1}
            emission={'start':-1,'end':-1,'increment':-1}
            try:
                incidence['start']=int(light_start_entry.get())
                incidence['end']=int(light_end_entry.get())
                incidence['increment']=int(light_increment_entry.get())
                
                emission['start']=int(detector_start_entry.get())
                emission['end']=int(detector_end_entry.get())
                emission['increment']=int(detector_increment_entry.get())
            except:
                print('Invalid input')
                return
            self.model.go(incidence, emission)
        
            if self.spec_save_config.get():
                print('writing to spec_save')
                file=open('spec_save.txt','w')
                file.write(self.spec_save_dir_entry.get()+'\n')
                file.write(self.spec_basename_entry.get()+'\n')
                file.write(self.spec_startnum_entry.get()+'\n')
             
    #If the user has failsafes activated, check that requirements are met. Always require a valid number of spectra.
    def input_check(self, func, args=[]):
            label=''
            now=int(time.time())
            incidence=self.man_incidence_entry.get()
            emission=self.man_emission_entry.get()
      
            if self.optfailsafe.get():
                try:
                    opt_limit=int(float(self.opt_timeout_entry.get()))*60
                except:
                    opt_limit=sys.maxsize
                if self.opt_time==None:
                    label+='The instrument has not been optimized.\n\n'
                elif now-self.opt_time>opt_limit: 
                    minutes=str(int((now-self.opt_time)/60))
                    seconds=str((now-self.opt_time)%60)
                    if int(minutes)>0:
                        label+='The instrument has not been optimized for '+minutes+' minutes '+seconds+' seconds.\n\n'
                    else: label+='The instrument has not been optimized for '+seconds+' seconds.\n\n'
                
            if self.wrfailsafe.get() and func!=self.wr:

                try:
                    wr_limit=int(float(self.wr_timeout_entry.get()))*60
                except:
                    wr_limit=sys.maxsize
                if self.wr_time==None:
                    label+='No white reference has been taken.\n\n'
                elif self.opt_time!=None and self.opt_time>self.wr_time:
                        label+='No white reference has been taken since the instrument was optimized.\n\n'
                elif int(self.instrument_config_entry.get()) !=int(self.spec_config_count):
                    label+='No white reference has been taken while averaging this number of spectra.\n\n'
                elif self.spec_config_count==None:
                    label+='No white reference has been taken while averaging this number of spectra.\n\n'
                elif now-self.wr_time>wr_limit: 
                    minutes=str(int((now-self.wr_time)/60))
                    seconds=str((now-self.wr_time)%60)
                    if int(minutes)>0:
                        label+=' No white reference has been taken for '+minutes+' minutes '+seconds+' seconds.\n\n'
                    else: label+=' No white reference has been taken for '+seconds+' seconds.\n\n'
            if self.wr_anglesfailsafe.get() and func!=self.wr:

                if self.angles_change_time!=None and self.wr_time!=None:
                    if self.angles_change_time>self.wr_time+1:
                        label+=' No white reference has been taken at this viewing geometry.\n\n'
                    elif emission!=self.e or incidence!=self.i:
                        label+=' No white reference has been taken at this viewing geometry.\n\n'
                    
            if self.anglesfailsafe.get():
                valid_i=validate_int_input(incidence,-90,90)
                valid_e=validate_int_input(emission,-90,90)
                if not valid_i and not valid_e:
                    label+='The emission and incidence angles are invalid.\n\n'
                elif not valid_i:
                    label+='The incidence angle is invalid.\n\n'
                elif not valid_e:
                    label+='The emission angle is invalid.\n\n'
                    
            if self.anglechangefailsafe.get():
                anglechangealert=False
                if self.angles_change_time==None and emission!='' and incidence !='':
                    label+='This is the first time emission and incidence angles are being set,\n'
                    anglechangealert=True
                elif self.e==None and emission!='':
                    label+='This is the first time the emission angle is being set,\n'
                    anglechangealert=True
                    if incidence!=self.i and incidence!='':
                        label+='and the incidence angle has changed since last spectrum,\n'
                    anglechangealert=True
                elif self.i==None and incidence!='':
                    label+='This is the first time the incidence angle is being set,\n'
                    anglechangealert=True
                    if emission!=self.e and emission !='':
                        label+='and the emission angle has changed since last spectrum,\n' 
                    anglechangealert=True
                if anglechangealert==False and emission!=self.e and emission !='' and incidence !=self.i and incidence!='':
                    if self.e!=None and self.i!=None:
                        label+='The emission and incidence angles have changed since last spectrum,\n'
                        anglechangealert=True
                elif anglechangealert==False and emission!=self.e and emission !='':
                    label+='The emission angle has changed since last spectrum,\n'
                    anglechangealert=True
                elif anglechangealert==False and incidence!=self.i and incidence!='':
                    label+='The incidence angle has changed since last spectrum,\n' 
                    anglechangealert=True
                    
                if anglechangealert:#and onlyanglechange:
                   label+='so the goniometer arm(s) may need to change to match.\n\n'
                   pass
                   
            if self.labelfailsafe.get():
                if self.label_entry.get()=='':
                    label +='This spectrum has no label.\n\n'

            if label !='': #if we came up with errors
                title='Warning!'
                
                buttons={
                    'yes':{
                        #if the user says they want to continue anyway, run take spectrum again but this time with override=True
                        func:args
                    },
                    'no':{}
                }
                label='Warning!\n\n'+label
                label+='\nDo you want to continue?'
                dialog=Dialog(self,title,label,buttons)
                return False
            else: #if there were no errors
                return True
              
    #If the user didn't choose a log file, make one in working directory
    def check_logfile(self):
        def inner_mkdir(new):
            try:
                os.makedirs(new)
            except:
                dialog=ErrorDialog(self, title='Error',label='Error: failed to create log directory.\n Creating new log file in current working directory.',topmost=False)
                self.logfile_entry.delete(0,'end')
                dialog.top.lower()
                dialog.top.tkraise(self.master)
            self.check_logfile()

        if self.logfile_entry.get()=='':
            self.log_filename='log_'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')+'.txt'
            with open(self.log_filename,'w+') as log:
                log.write(str(datetime.datetime.now())+'\n')
            if opsys=='Linux':
                self.logfile_entry.insert(0,os.getcwd()+'/'+self.log_filename)
            elif opsys=='Windows':
                self.logfile_entry.insert(0,os.getcwd()+'\\'+self.log_filename)
            elif opsys=='Mac':
                self.logfile_entry.insert(0,os.getcwd()+'/'+self.log_filename)


        elif self.logfile_entry.get()!=self.log_filename:
            dir=None
            if opsys=='Linux':
                if '/' in self.logfile_entry.get()[1:]:
                    dir='/'.join(self.logfile_entry.get().split('/')[:-1])
                else:
                    self.logfile_entry.insert(0,os.getcwd()+'/')
            elif opsys=='Windows':
                if '\\' in self.logfile_entry.get()[1:]:
                    dir='\\'.join(self.logfile_entry.get().split('\\')[:-1])
                else:
                    self.logfile_entry.insert(0,os.getcwd()+'\\')
            elif opsys=='Mac':
                if '/' in self.logfile_entry.get()[1:]:
                    dir='/'.join(self.logfile_entry.get().split('/')[:-1])
                else:
                    self.logfile_entry.insert(0,os.getcwd()+'/')
            if dir!=None:
                if not os.path.isdir(dir):
                    print('making log directory')
                    inner_mkdir(dir)
                    return
                # buttons={
                #     'yes':{
                #         mkdir:[dir]
                #     },
                #     'no':{}
                # }
                # dialog=ErrorDialog(self,label=dir+'\ndoes not exist. Do you want to create this directory?',buttons=buttons)
            

            if not os.path.isfile(self.logfile_entry.get()):
                try:
                    if '.' not in self.logfile_entry.get():
                        self.logfile_entry.insert('end','.txt')
                    with open(self.logfile_entry.get(),'w+') as log:
                        log.write(str(datetime.datetime.now())+'\n')
                    self.log_filename=self.logfile_entry.get()

                except:
                    dialog=ErrorDialog(self,label='Error: Could not open log file for writing.\nCreating new log file in current working directory', topmost=False)
                    dialog.top.lower()
                    dialog.top.tkraise(self.master)

                    self.logfile_entry.delete(0,'end')
                    self.check_logfile()
            else:
                self.log_filename=self.logfile_entry.get()

            
            
        
            
    def wr(self, override=False):

        #Label this as a white reference for the log file
        if self.label_entry.get()!='' and 'White reference' not in self.label_entry.get():
            self.label_entry.insert(0, 'White reference: ')
        elif self.label_entry.get()=='':
            self.label_entry.insert(0,'White reference')
            
        try:
            new_spec_config_count=int(self.instrument_config_entry.get())
            if new_spec_config_count<1 or new_spec_config_count>32767:
                raise(Exception)
        except:
            dialog=ErrorDialog(self,label='Error: Invalid number of spectra to average.\nEnter a value from 1 to 32767')
            return 
            

        save_config_status=self.check_save_config()
        if save_config_status=='invalid':
            dialog=ErrorDialog(self,label='Error: Please enter a valid save configuration.')

            return
            
        valid_input=True #We'll check this in a moment if override=False

        if not override:
            valid_input=self.input_check(self.wr,[True])
            
        #If the input wasn't valid, we popped up an error dialog and now will exit. If the user clicks continue, wr will be called again with override=True
        if not valid_input:
            return
        else:
            pass
            
        #If the user specified a log file to use, use it. If not, make a new one in the current working directory
        self.check_logfile()

        
        if save_config_status=='not_set':
            self.set_save_config(self.wr, [override])
            return
            
        if self.spec_config_count==None or str(new_spec_config_count) !=str(self.spec_config_count):
            
            #This is a bit weird because these aren't actually buttons. Probably could be written better. 
            buttons={
                'success':{
                    self.wr:[override]
                }
            }
            
            self.configure_instrument(buttons)
            return

        self.model.white_reference()
        
        #Not actually buttons, but functions to be executed if the white reference is successful.
        #In this case, save a spectrum with override=True
        buttons={
            'success':{
            
                self.take_spectrum:[True]
            }
        }
        waitdialog=WaitForWRDialog(self, buttons=buttons)
            
    def opt(self):
        try:
            new_spec_config_count=int(self.instrument_config_entry.get())
            if new_spec_config_count<1 or new_spec_config_count>32767:
                raise(Exception)
        except:
            dialog=ErrorDialog(self,label='Error: Invalid number of spectra to average.\nEnter a value from 1 to 32767')
            return 
        if self.spec_config_count==None or str(new_spec_config_count) !=str(self.spec_config_count):
            #Not actually buttons, but functions to be executed if the configuration is successful.
            buttons={
                'success':{
                    self.opt:[]
                }
            }
            
            self.configure_instrument(buttons)
            return
            
        self.check_logfile()
        self.model.opt()
        waitdialog=WaitForOptDialog(self)

    def test(self,arg=False):
        print(arg)
        
    #Check whether the current save configuration is different from the last one saved. If it is, send commands to the spec compy telling it so.
    def check_save_config(self):
        new_spec_save_dir=self.spec_save_dir_entry.get()
        new_spec_basename=self.spec_basename_entry.get()
        try:
            new_spec_num=int(self.spec_startnum_entry.get())
        except:
            return 'invalid'
 

        if new_spec_save_dir=='' or new_spec_basename=='' or new_spec_num=='':
            return 'invalid'
        
        if new_spec_save_dir != self.spec_save_path or new_spec_basename != self.spec_basename or self.spec_num==None or new_spec_num!=self.spec_num:
            return 'not_set'
        else:
            return 'set'
            
    def take_spectrum(self, override=False):
        
        incidence=self.man_incidence_entry.get()
        emission=self.man_emission_entry.get()
        
        save_config_status=self.check_save_config()
        if save_config_status=='invalid':
            dialog=ErrorDialog(self,label='Error: Please enter a valid save configuration.')
            return
            
        
        #If the user hasn't already said they want to override input checks 1) ask whether the user has input checkboxes selected in the Settings tab and then 2)if they do, see if the inputs are valid. If they aren't all valid, create one dialog box that will list everything wrong.
        valid_input=True
        if not override:  
            valid_input=self.input_check(self.take_spectrum,[True])
            
            
        #If input isn't valid and the user asks to continue, take_spectrum will be called again with override set to True
        if not valid_input:
            return

        try:
            new_spec_num=int(self.spec_startnum_entry.get())
        except:
            dialog=ErrorDialog(self,'Error: Invalid spectrum number')
            return
            
        try:
            new_spec_config_count=int(self.instrument_config_entry.get())
            if new_spec_config_count<1 or new_spec_config_count>32767:
                raise(Exception)
        except:
            dialog=ErrorDialog(self,label='Error: Invalid number of spectra to average.\nEnter a value from 1 to 32767')
            return    
        self.check_logfile()

        if self.check_save_config()=='not_set':
            self.set_save_config(self.take_spectrum,[True])
            return
            
        if self.spec_config_count==None or str(new_spec_config_count) !=str(self.spec_config_count):
            buttons={
                'success':{
                    self.take_spectrum:[override]
                }
            }
            self.configure_instrument(buttons)
            return
            

        startnum_str=str(self.spec_startnum_entry.get())
        while len(startnum_str)<NUMLEN:
            startnum_str='0'+startnum_str
        
        
        if self.i!=incidence or self.e!=emission:
            self.angles_change_time=time.time()
        self.i=incidence
        self.e=emission

        self.model.take_spectrum(self.man_incidence_entry.get(), self.man_emission_entry.get(),self.spec_save_path, self.spec_basename, startnum_str)
        
        if self.spec_save_config.get():
            file=open(self.config_loc+'spec_save.txt','w')
            file.write(self.spec_save_dir_entry.get()+'\n')
            file.write(self.spec_basename_entry.get()+'\n')
            file.write(self.spec_startnum_entry.get()+'\n')

            self.input_dir_entry.delete(0,'end')
            self.input_dir_entry.insert(0,self.spec_save_dir_entry.get())
            
        wait_dialog=WaitForSpectrumDialog(self)

        return wait_dialog
    
    def check_connection(self):
        self.connection_checker.check_connection(False)
    
    def configure_instrument(self,buttons):
        self.model.configure_instrument(self.instrument_config_entry.get())
        
        #This is a bit weird because the buttons here aren't actually buttons, they are functions to be executed.
        waitdialog=WaitForConfigDialog(self, buttons=buttons)
        
    def set_save_config(self, func, args):
        print('hi!')
        def inner_mkdir(dir):
            status=self.remote_directory_worker.mkdir(dir)
            if status=='mkdirsuccess':
                self.set_save_config(func, args)
            elif status=='mkdirfailedfileexists':
                dialog=ErrorDialog(self,title='Error',label='Could not create directory:\n\n'+dir+'\n\nFile exists.')
            elif status=='mkdirfailed':
                dialog=ErrorDialog(self,title='Error',label='Could not create directory:\n\n'+dir)

        status=self.remote_directory_worker.get_dirs(self.spec_save_dir_entry.get())
        print(status)
        if status=='listdirfailed':
            buttons={
                'yes':{
                    inner_mkdir:[self.spec_save_dir_entry.get()]
                },
                'no':{
                }
            }
            dialog=ErrorDialog(self,title='Directory does not exist',label=self.spec_save_dir_entry.get()+'\ndoes not exist. Do you want to create this directory?',buttons=buttons)
            return
        elif status=='listdirfailedpermission':
            dialog=ErrorDialog(self,label='Error: Permission denied for\n'+self.spec_save_dir_entry.get())
            return
        
        elif status=='timeout':
            dialog=ErrorDialog(self, label='Error: Operation timed out.\nCheck connections.\nCheck that the automation script is running on the spectrometer computer\nand the spectrometer is connected.')
            return
            
        try:
            global CMDNUM
            filename=encrypt('checkwriteable',CMDNUM,parameters=[self.spec_save_dir_entry.get()])
            CMDNUM=CMDNUM+1
            
            with open(self.write_command_loc+filename,'w+') as f:
                pass
        except:
            pass
            
        t=2*BUFFER
        while t>0:
            if 'yeswriteable' in self.listener.queue:
                self.listener.queue.remove('yeswriteable')
                break
            elif 'notwriteable' in self.listener.queue:
                self.listener.queue.remove('notwriteable')
                dialog=ErrorDialog(self, label='Error: Permission denied.\nCannot write to specified directory.')
                return
            time.sleep(INTERVAL)
            t=t-INTERVAL
        if t<=0:
            dialog=ErrorDialog(self,label='TIMEOUT')
            return
        
        
        spec_num=self.spec_startnum_entry.get()
        while len(spec_num)<NUMLEN:
            spec_num='0'+spec_num
        
        self.model.set_save_path(self.spec_save_dir_entry.get(), self.spec_basename_entry.get(), self.spec_startnum_entry.get())
        buttons={
            'success':{
                func:args
            }
        }
        waitdialog=WaitForSaveConfigDialog(self, buttons=buttons)
            
            
    def increment_num(self):
        try:
            num=int(self.spec_startnum_entry.get())+1
            self.spec_startnum_entry.delete(0,'end')
            self.spec_startnum_entry.insert(0,str(num))
        except:
            return
    
    def move(self):
        try:
            incidence=int(man_light_entry.get())
            emission=int(man_detector_entry.get())
        except:
            print('Invalid input')
            return
        if incidence<0 or incidence>90 or emission<0 or emission>90:
            print('Invalid input')
            return
        self.model.move_light(i)
        self.model.move_detector(e)
        
    def process_cmd(self):
        output_file=self.output_file_entry.get()
        if output_file=='':
            dialog=ErrorDialog(self, label='Error: Enter an output file name')
            return
        if '.' not in output_file: output_file=output_file+'.tsv'
        error=self.model.process(self.input_dir_entry.get(), self.output_dir_entry.get(), output_file)
        if error!=None:
            dialog=ErrorDialog(self, label='Error sending process command:\n'+error.strerror)

        
        if self.process_save_dir.get():
            file=open(self.config_loc+'/process_directories','w')
            file.write(self.input_dir_entry.get()+'\n')
            file.write(self.output_dir_entry.get()+'\n')
            file.write(output_file+'\n')
            self.plot_input_dir_entry.delete(0,'end')
            plot_file=self.output_dir_entry.get()+'\\'+output_file
            self.plot_input_dir_entry.insert(0,plot_file)
            
        process_dialog=WaitForProcessDialog(self)
            
    def plot(self):
        filename=self.plot_input_dir_entry.get()
        # filename=filename.replace('C:\\SpecShare',self.command_share_loc)
        # filename=filename.replace('C:\\Users',self.data_share_loc)
        if self.opsys=='Windows' or self.remote.get(): filename=filename.replace('\\','/')
        
        if self.remote.get():
            print('hi!')
            global CMDNUM
            cmd_filename=encrypt('getdata',CMDNUM,parameters=[filename])
            print(cmd_filename)
            CMDNUM=CMDNUM+1
            try:
                with open(self.write_command_loc+cmd_filename,'w+') as f:
                    pass
            except:
                pass
            t=3*BUFFER
            while True:
                print('waiting!')
                if 'datacopied' in self.listener.queue:
                    self.listener.queue.remove('datacopied')
                    filename=self.command_share_loc+'temp.tsv'
                    break
                elif 'datafailure' in self.listener.queue:
                    self.listener.queue.remove('datafailure')
                    dialog=ErrorDialog(self,label='Error: Failed to acquire data.\nDoes the file exist? Do you have permission to use it?')
                    return
                time.sleep(INTERVAL)
                t=t-INTERVAL
        
        title=self.plot_title_entry.get()
        caption=''#self.plot_caption_entry.get()
        labels={}
        nextfile=None
        nextnote=None
        try:
            if self.load_labels.get():
                with open(self.plot_logfile_entry.get()) as log:
                    for line in log:
                        if 'filename' in line:
                            if '\\' in line:
                                line=line.split('\\')
                            else:
                                line=line.split('/')
                            nextfile=line[-1].strip('\n')
                            nextfile=nextfile.split('.')
                            nextfile=nextfile[0]+nextfile[1]
                            print(nextfile)
                        elif 'Label' in line:
                            nextnote=line.split('Label: ')[-1]
                            print(nextnote)
                        if nextfile != None and nextnote != None:
                            labels[nextfile]=nextnote.strip('\n')
                            nextfile=None
                            nextnote=None
                        
                    
        except:
            dialog=ErrorDialog(self, label='Error! File not found: '+self.load_labels_entry.get())
        try:
            self.plotter.plot_spectra(title,filename,caption,labels)
        except:
            dialog=Dialog(self, 'Plotting Error', 'Error: Plotting failed. Does file exist?',{'ok':{}})
    
    
    def auto_cycle_check(self):
        if self.auto.get():
            light_end_label.config(fg='black')
            detector_end_label.config(fg='black')
            light_increment_label.config(fg='black')
            detector_increment_label.config(fg='black')
            light_end_entry.config(bd=3)
            detector_end_entry.config(bd=3)
            light_increment_entry.config(bd=3)
            detector_increment_entry.config(bd=3)
        else:
            light_end_label.config(fg='lightgray')
            detector_end_label.config(fg='lightgray')
            light_increment_label.config(fg='lightgray')
            detector_increment_label.config(fg='lightgray')
            light_end_entry.config(bd=1)
            detector_end_entry.config(bd=1)
            light_increment_entry.config(bd=1)
            detector_increment_entry.config(bd=1)
        
    def run(self, keypress_event):
        global user_cmds
        global user_cmd_index
        if keypress_event.keycode==36:
            cmd=self.console_entry.get()
            if cmd !='':
                user_cmds.insert(0,cmd)
                user_cmd_index=-1
                self.console_log.insert(END,'>>> '+cmd+'\n')
                self.console_entry.delete(0,'end')
                
                params=cmd.split(' ')
                if params[0].lower()=='process':
                    try:
                        if params[1]=='--save_config':
                            self.process_save_dir_check.select()
                            params.pop(1)
                        self.input_dir_entry.delete(0,'end')
                        self.input_dir_entry.insert(0,params[1])
                        self.output_dir_entry.delete(0,'end')
                        self.output_dir_entry.insert(0,params[2]) 
                        self.output_file_entry.delete(0,'end')
                        self.output_file_entry.insert(0,params[3])
                        process_cmd()
                    except:
                        self.console_log.insert(END,'Error: Failed to process file.')
                elif params[0].lower()=='wr':
                    self.wr()
                elif params[0].lower()=='opt':
                    self.opt()
                elif params[0].lower()=='log':
                    logstring=''
                    for word in params:
                        logstring=logstring+word+' '
                    logstring=logstring+'\n'
                    with open('log.txt','a') as log:
                        log.write(logstring)
                    
            
        elif keypress_event.keycode==111:
            if len(user_cmds)>user_cmd_index+1 and len(user_cmds)>0:
                user_cmd_index=user_cmd_index+1
                last=user_cmds[user_cmd_index]
                self.console_entry.delete(0,'end')
                self.console_entry.insert(0,last)

        elif keypress_event.keycode==116:
            if user_cmd_index>0:
                user_cmd_index=user_cmd_index-1
                next=user_cmds[user_cmd_index]
                self.console_entry.delete(0,'end')
                self.console_entry.insert(0,next)
                
    def choose_spec_save_dir(self):
        r=RemoteFileExplorer(self,write_command_loc,label='Select a directory to save raw spectral data.\nThis must be to a drive mounted on the spectrometer control computer.\n E.g. R:\RiceData\MarsGroup\Kathleen\spectral_data', target=self.spec_save_dir_entry)
        
    def choose_process_input_dir(self):
        r=RemoteFileExplorer(self,write_command_loc,label='Select the directory containing the data you want to process.\nThis must be to a drive mounted on the spectrometer control computer.\n E.g. R:\RiceData\MarsGroup\Kathleen\spectral_data',target=self.input_dir_entry)
        
    def choose_process_output_dir(self):
        r=RemoteFileExplorer(self,write_command_loc,label='Select the directory where you want to save your processed data.\nThis must be to a drive mounted on the spectrometer control computer.\n E.g. R:\RiceData\MarsGroup\Kathleen\spectral_data',target=self.output_dir_entry)
    
    # def validate_basename(self,*args):
    #     basename=limit_len(self.spec_basename_entry.get())
    #     basename=rm_reserved_chars(basename)
    #     self.spec_basename_entry.set(basename)
    # 
    # def validate_startnum(self,*args):
    #     num=spec_startnum.get()
    #     valid=validate_int_input(num,999,0)
    #     if not valid:
    #         spec_startnum.set('')
    #     else:
    #         while len(num)<NUMLEN:
    #             num=0+num
    #     self.spec_startnum_entry.delete(0,'end')
    #     self.spec_startnum_entry.insert(0,num)
    
    def validate_input_dir(self,*args):
        pos=self.input_dir_entry.index(INSERT)
        input_dir=rm_reserved_chars(self.input_dir_entry.get())
        if len(input_dir)<len(self.input_dir_entry.get()):
            pos=pos-1
        self.input_dir_entry.delete(0,'end')
        self.input_dir_entry.insert(0,input_dir)
        self.input_dir_entry.icursor(pos)
        
    def validate_output_dir(self):
        pos=self.output_dir_entry.index(INSERT)
        output_dir=rm_reserved_chars(self.output_dir_entry.get())
        if len(output_dir)<len(self.output_dir_entry.get()):
            pos=pos-1
        self.output_dir_entry.delete(0,'end')
        self.output_dir_entry.insert(0,output_dir)
        self.output_dir_entry.icursor(pos)
        
    def validate_output_filename(self,*args):
        pos=self.output_filename_entry.index(INSERT)
        filename=rm_reserved_chars(self.spec_output_filename_entry.get())
        filename=filename.strip('/').strip('\\')
        self.output_filename_entry.delete(0,'end')
        self.output_filename_entry.insert(0,filename)
        self.output_filename_entry.icursor(pos)
        
    def validate_spec_save_dir(self,*args):
        pos=self.spec_save_dir_entry.index(INSERT)
        spec_save_dir=rm_reserved_chars(self.spec_save_dir_entry.get())
        if len(spec_save_dir)<len(self.spec_save_dir_entry.get()):
            pos=pos-1
        self.spec_save_dir_entry.delete(0,'end')
        self.spec_save_dir_entry.insert(0,spec_save_dir)
        self.spec_save_dir_entry.icursor(pos)
    
    def validate_logfile(self,*args):
        pos=self.logfile_entry.index(INSERT)
        logfile=rm_reserved_chars(self.logfile_entry.get())
        if len(logfile)<len(self.logfile_entry.get()):
            pos=pos-1
        self.logfile_entry.delete(0,'end')
        self.logfile_entry.insert(0,logfile)
        self.logfile_entry.icursor(pos)

    def validate_basename(self,*args):
        pos=self.spec_basename_entry.index(INSERT)
        basename=rm_reserved_chars(self.spec_basename_entry.get())
        basename=basename.strip('/').strip('\\')
        self.spec_basename_entry.delete(0,'end')
        self.spec_basename_entry.insert(0,basename)
        self.spec_basename_entry.icursor(pos)
        
    def validate_startnum(self,*args):
        pos=self.spec_startnum_entry.index(INSERT)
        num=numbers_only(self.spec_startnum_entry.get())
        if len(num)>NUMLEN:
            num=num[0:NUMLEN]
        if len(num)<len(self.spec_startnum_entry.get()):
            pos=pos-1
        self.spec_startnum_entry.delete(0,'end')
        self.spec_startnum_entry.insert(0,num)
        self.spec_startnum_entry.icursor(pos)
        
    def clear(self):
        self.man_incidence_entry.delete(0,'end')
        self.man_emission_entry.delete(0,'end')
        self.label_entry.delete(0,'end')
        
    def rm_current(self):
        filename=encrypt('rmfile',CMDNUM, parameters=[self.spec_save_dir_entry.get(),self.spec_basename_entry.get(),self.spec_startnum_entry.get()])
        try:
            with open(self.write_command_loc+filename,'w+') as f:
                pass
        except:
            pass

        t=BUFFER
        while t>0:
            if 'rmsuccess' in self.listener.queue:
                self.listener.queue.remove('rmsuccess')

                return True
            elif 'rmfailure' in self.listener.queue:
                self.listener.queue.remove('rmfailure')
                return False
            t=t-INTERVAL
            time.sleep(INTERVAL)
        return False
        
    def choose_plot_file(self):
        file=self.plot_input_dir_entry.get()
        if self.remote.get():
            plot_file_explorer=RemoteFileExplorer(self,self.write_command_loc, target=self.plot_input_dir_entry,title='Select a file',label='Select a file to plot',directories_only=False)
        else:
            if os.path.isdir(file):
                file = askopenfilename(initialdir=file,title='Select a file to plot')
            else:
                file=askopenfilename(initialdir=os.getcwd(),title='Select a file to plot')
            self.plot_input_dir_entry.delete(0,'end')
            self.plot_input_dir_entry.insert(0, file)
        

    
class Dialog:
    def __init__(self, controller, title, label, buttons, width=None, height=None,allow_exit=True, button_width=30, info_string=None, grab=True):
        
        self.controller=controller
        self.grab=grab
        
        try:
            self.textcolor=self.controller.textcolor
            self.bg=self.controller.bg
            self.buttonbackgroundcolor=self.controller.buttonbackgroundcolor
            self.highlightbackgroundcolor=self.controller.highlightbackgroundcolor
            self.entry_background=self.controller.entry_background
            self.buttontextcolor=self.controller.buttontextcolor
            self.console_log=self.controller.console_log
            self.listboxhighlightcolor=self.controller.listboxhighlightcolor
            self.selectbackground=self.controller.selectbackground
            self.selectforeground=self.controller.selectforeground
        except:
            self.textcolor='black'
            self.bg='white'
            self.buttonbackgroundcolor='light gray'
            self.highlightbackgroundcolor='white'
            self.entry_background='white'
            self.buttontextcolor='black'
            self.console_log=None
            self.listboxhighlightcolor='light gray'
            self.selectbackground='light gray'
            self.selectforeground='black'
            

        
        #If we are starting a new master, we'll need to start a new mainloop after settin everything up. 
        #If this creates a new toplevel for an existing master, we will leave it as False.
        start_mainloop=False
        if controller==None:
            self.top=Tk()
            start_mainloop=True
            #global tk_master
            #tk_master=self.top
            self.top.configure(background=self.bg)
        else:
            if width==None or height==None:
                self.top = tk.Toplevel(controller.master, bg=self.bg)
            else:
                self.top=tk.Toplevel(controller.master, width=width, height=height, bg=self.bg)
                self.top.pack_propagate(0)
                
            #self.controller.master.iconify() 
            if self.grab:
                try:
                    self.top.grab_set()
                except:
                    print('failed to grab')
        
        self.top.attributes('-topmost', 1)
        self.top.attributes('-topmost', 0)
                


        self.label_frame=Frame(self.top, bg=self.bg)
        self.label_frame.pack(side=TOP)
        self.label = tk.Label(self.label_frame, fg=self.textcolor,text=label, bg=self.bg)
        self.set_label_text(label, log_string=info_string)
        self.label.pack(pady=(10,10), padx=(10,10))
    
        self.button_width=button_width
        self.buttons=buttons
        self.set_buttons(buttons)

        self.top.wm_title(title)
        self.allow_exit=allow_exit
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        if start_mainloop:
            self.top.mainloop()
            
        if controller!=None and info_string!=None:
            self.log(info_string)
            
    def set_title(self, newtitle):
        self.top.wm_title(newtitle)
    def set_label_text(self, newlabel, log_string=None):
        self.label.config(fg=self.textcolor,text=newlabel)
        if log_string != None and self.controller!=None:
            self.log(log_string)
            #self.controller.console_log.insert(END, info_string)

    def log(self, info_string):
        datestring=''
        datestringlist=str(datetime.datetime.now()).split('.')[:-1]
        for d in datestringlist:
            datestring=datestring+d
            
        if info_string[-2:-1]!='\n':
            info_string+='\n'
        info_string=datestring+': '+info_string
        self.controller.console_log.insert(END,info_string+'\n')
        
    def set_buttons(self, buttons, button_width=None):
        self.buttons=buttons
        if button_width==None:
            button_width=self.button_width
        #Sloppy way to check if button_frame already exists and reset it if it does.
        try:
            self.button_frame.destroy()
        except:
            pass
        self.button_frame=Frame(self.top, bg=self.bg)
        self.button_frame.pack(side=BOTTOM)
        self.tk_buttons=[]

        for button in buttons:
            if 'ok' in button.lower():
                self.ok_button = Button(self.button_frame, fg=self.textcolor,text='OK', command=self.ok, width=button_width)
                self.tk_buttons.append(self.ok_button)
                self.ok_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
            elif 'yes' in button.lower():
                self.yes_button=Button(self.button_frame, fg=self.textcolor,text='Yes', bg='light gray', command=self.yes, width=button_width)
                self.tk_buttons.append(self.yes_button)
                self.yes_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
            elif 'no' in button.lower():
                self.no_button=Button(self.button_frame, fg=self.textcolor,text='No',command=self.no, width=button_width)
                self.no_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
                self.tk_buttons.append(self.no_button)
            elif 'cancel' in button.lower():
                self.cancel_button=Button(self.button_frame, fg=self.textcolor,text='Cancel',command=self.cancel, width=button_width)
                self.cancel_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
                self.tk_buttons.append(self.cancel_button)
            elif 'retry' in button.lower():
                self.retry_button=Button(self.button_frame, fg=self.textcolor,text='Retry',command=self.retry, width=button_width)
                self.retry_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
                self.tk_buttons.append(self.retry_button)
            elif 'exit' in button.lower():
                self.exit_button=Button(self.button_frame, fg=self.textcolor,text='Exit',command=self.exit, width=button_width)
                self.exit_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
                self.tk_buttons.append(self.exit_button)
            elif 'work offline' in button.lower():
                print('hi!')
                self.offline_button=Button(self.button_frame, fg=self.textcolor,text='Work offline',command=self.work_offline, width=button_width)
                self.offline_button.pack(side=LEFT, padx=(10,10), pady=(10,10))
                self.tk_buttons.append(self.offline_button)
                
            for button in self.tk_buttons:
                button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
            

            # else:
            #     #For each button, only handle one function with no arguments here 
            #     #the for loop is just a way to grab the function.
            #     #It would be cool to do better than this, but it will work for now.
            #     for func in buttons[button]:
            #         print(button)
            #         print(func)
            #         tk_buttons[button]=Button(self.button_frame, fg=self.textcolor,text=button,command=func)
            #         tk_buttons[button].pack(side=LEFT, padx=(10,10),pady=(10,10))
            
    def on_closing(self):
        if self.allow_exit:
            self.top.destroy()
    
    def retry(self):
        self.top.destroy()
        dict=self.buttons['retry']
        self.execute(dict,False)
        
    def exit(self):
        self.top.destroy()
        exit()

    def ok(self):
        dict=self.buttons['ok']
        self.execute(dict)
        
    def yes(self):
        dict=self.buttons['yes']
        self.execute(dict)
        
    def no(self):
        dict=self.buttons['no']
        self.execute(dict)
            
    def cancel(self):
        dict=self.buttons['cancel']
        self.execute(dict)
        
    def execute(self,dict,close=True):
        for func in dict:
            args=dict[func]
            func(*args)

        if close:
            self.top.destroy()
    
    def work_offline(self):
        dict=self.buttons['work offline']
        self.execute(dict)


class WaitDialog(Dialog):
    def __init__(self, controller, title='Working...', label='Working...', buttons={}, timeout=30):
        super().__init__(controller, title, label,buttons,width=400, height=150, allow_exit=False)
        self.listener=self.controller.listener
        
        #We'll keep track of elapsed time so we can cancel the operation if it takes too long
        self.t0=time.clock()
        self.t=time.clock()
        self.timeout_s=timeout
        
        #I think these three attributes are useless and should be deleted
        self.canceled=False
        self.interrupted=False
        self.fileexists=False
        
        self.frame=Frame(self.top, bg=self.bg, width=200, height=30)
        self.frame.pack()
  
        style=ttk.Style()
        style.configure('Horizontal.TProgressbar', background='white')
        self.pbar = ttk.Progressbar(self.frame, mode='indeterminate', name='pb2', style='Horizontal.TProgressbar' )
        self.pbar.start([10])
        self.pbar.pack(padx=(10,10),pady=(10,10))
        
        #A Listener object is always running a loop in a separate thread. It  listens for files dropped into a command folder and changes its attributes based on what it finds.
        self.listener=self.controller.listener
        self.timeout_s=timeout
        

        #Start the wait function, which will watch the listener to see what attributes change and react accordingly.
        thread = Thread(target =self.wait)
        thread.start()
        
    @property
    def timeout_s(self):
        return self.__timeout_s
        
    @timeout_s.setter
    def timeout_s(self, val):
        self.__timeout_s=val
        
    def wait(self):
        while True:
            print('waiting in super...')
            self.timeout_s-=1
            if self.timeout<0:
                self.timeout()
            time.sleep(1)
               
    def timeout(self, log_string=None):
        if log_string==None:
            self.set_label_text('Error: Operation timed out', log_string='Error: Operation timed out')
        else:
            self.set_label_text('Error: Operation timed out',log_string=log_string)
        self.pbar.stop()
        self.set_buttons({'ok':{}})
        
    def finish(self):
        self.top.destroy()
        
    def cancel(self):
        self.canceled=True
        
    def interrupt(self,label, info_string=None):
        self.allow_exit=True
        self.interrupted=True
        self.set_label_text(label)
        self.pbar.stop()
        self.set_buttons({'ok':{}})
        if info_string!=None:
            self.log(info_string)
                
    def send(self):
        global username
        username = self.myEntryBox.get()
        self.top.destroy()
        
    def remove_retry(self,func, args):
        print(func)
        print(args)
        removed=self.controller.rm_current()
        if removed: 
            self.log('Warning: overwriting data.')
            func(*args)
        else:
            dialog=ErrorDialog(self.controller,label='Error: Failed to remove file. Choose a different base name,\nspectrum number, or save directory and try again.')
            self.set_buttons({'ok':{}})

class WaitForConfigDialog(WaitDialog):
    def __init__(self, controller, title='Configuring instrument...', label='Configuring instrument...', buttons={}, timeout=20):
        super().__init__(controller, title, label,timeout=timeout)
        self.loc_buttons=buttons
        self.listener=self.controller.listener

    def wait(self):
        while self.timeout_s>0:
            if 'iconfigsuccess' in self.listener.queue:
                self.listener.queue.remove('iconfigsuccess')
                self.success()
                return
            elif 'iconfigfailure' in self.listener.queue:
                self.listener.queue.remove('iconfigfailure')
                self.failure()
                return
                
            time.sleep(INTERVAL)
            self.timeout_s-=INTERVAL
        self.timeout()
    def failure(self):
        self.interrupt('Error: Failed to configure instrument.')
        
    def success(self):
        self.controller.spec_config_count=self.controller.instrument_config_entry.get()
        datestring=''
        datestringlist=str(datetime.datetime.now()).split('.')[:-1]
        for d in datestringlist:
            datestring=datestring+d
        self.log('\n Instrument configured at '+datestring+ ' with '+str(self.controller.spec_config_count)+' spectra being averaged.')

        dict=self.loc_buttons['success']
        self.execute(dict)

class WaitForOptDialog(WaitDialog):
    def __init__(self, controller, title='Optimizing...', label='Optimizing...', buttons={'cancel':{}}):
        timeout=int(controller.spec_config_count)/9+10+BUFFER
        super().__init__(controller, title, label,timeout=2*timeout)
        
        if self.controller.spec_config_count!=None:
            self.timeout_s=int(self.controller.spec_config_count*2)
        else:
            self.timeout=1000

    def wait(self):
        while self.timeout_s>0:
            if 'nonumspectra' in self.controller.listener.queue:
                self.listener.queue.remove('nonumspectra')
                buttons={
                    'success':{
                        self.controller.opt:[]
                    }
                }
                
                self.controller.configure_instrument(buttons)
                self.finish()
                return
                
            if 'optsuccess' in self.controller.listener.queue:
                self.listener.queue.remove('optsuccess')
                self.success()
                return
            elif 'optfailure' in self.controller.listener.queue:
                self.listener.queue.remove('optfailure')
                self.interrupt('Error: There was a problem with\noptimizing the instrument.',info_string='Error: There was a problem with optimizing the instrument')
                return
            time.sleep(INTERVAL)
            self.timeout_s-=INTERVAL
        self.timeout()
                
    def success(self):
        self.controller.opt_time=int(time.time())
        datestring=''
        datestringlist=str(datetime.datetime.now()).split('.')[:-1]
        for d in datestringlist:
            datestring=datestring+d
        self.log('\n Instrument optimized at '+datestring+ '\n\ti='+self.controller.man_incidence_entry.get()+'\n\te='+self.controller.man_emission_entry.get())

        self.interrupt('Success!')
        
class WaitForWRDialog(WaitDialog):
    def __init__(self, controller, title='White referencing...',
    label='White referencing...', buttons={'cancel':{}}):
        timeout_s=int(controller.spec_config_count)/9+6+BUFFER
        super().__init__(controller, title, label,timeout=timeout_s)
        self.loc_buttons=buttons
        

    def wait(self):
        while self.timeout_s>0:
            if 'wrsuccess' in self.controller.listener.queue:
                self.listener.queue.remove('wrsuccess')
                self.success()
                return
            elif 'nonumspectra' in self.controller.listener.queue:
                self.listener.queue.remove('nonumspectra')
                buttons={
                    'success':{
                        self.controller.wr:[True]
                    }
                }
                
                self.controller.configure_instrument(buttons)
                self.finish()
                return
            elif 'noconfig' in self.controller.listener.queue:
                self.listener.queue.remove('noconfig')
                self.controller.set_save_config(self.controller.wr, [True])
                self.finish()
                return
                
            elif 'wrfailedfileexists' in self.listener.queue:
                self.listener.queue.remove('wrfailedfileexists')
                self.interrupt('Error: File exists.\nDo you want to overwrite this data?')
                dict=self.loc_buttons['success']
                func=None
                for f in dict:
                    args=dict[f]
                    func=f
                buttons={
                    'yes':{
                        self.remove_retry:[func,args]
                    },
                    'no':{
                    }
                }
                    
                self.set_buttons(buttons,button_width=20)
                return
            time.sleep(INTERVAL)
            self.timeout_s-=INTERVAL
        self.timeout()
                
    def success(self):
        self.controller.wr_time=int(time.time())
        datestring=''
        datestringlist=str(datetime.datetime.now()).split('.')[:-1]
        for d in datestringlist:
            datestring=datestring+d
        self.log('\n White reference saved at '+datestring+ '\n\ti='+self.controller.man_incidence_entry.get()+'\n\te='+self.controller.man_emission_entry.get())
        
        dict=self.loc_buttons['success']
        for func in dict:
            args=dict[func]
            func(*args)
        self.top.destroy()
            
            
class WaitForProcessDialog(WaitDialog):
    def __init__(self, controller, title='Processing...', label='Processing...', buttons={'cancel':{}}):
        super().__init__(controller, title, label,timeout=60+BUFFER)

    def wait(self):
        while self.timeout_s>0:
            if 'processsuccess' in self.listener.queue:
                self.listener.queue.remove('processsuccess')
                self.interrupt('Success!')
                return
                
            elif 'processerrorfileexists' in self.listener.queue:
                self.controller.listener.queue.remove('processerrorfileexists')
                self.interrupt('Error processing files: Output file already exists')
                return
                
            elif 'processerrorwropt' in self.listener.queue:
                self.listener.queue.remove('processerrorwropt')
                self.interrupt('Error processing files.\nDid you optimize and white reference before collecting data?')
                return
                
            elif 'processerror' in self.listener.queue:
                self.listener.queue.remove('processerror')
                self.interrupt('Error processing files.\nAre you sure directories exist?\n')
                return
                
            time.sleep(INTERVAL)
            self.timeout_s-=INTERVAL
        self.timeout()
        
        self.timeout()
        
class WaitForSaveConfigDialog(WaitDialog):
    def __init__(self, controller, title='Setting Save Configuration...', label='Setting save configuration...', buttons={'cancel':{}}, timeout=30):
        super().__init__(controller, title, label,timeout=timeout)
        self.keep_around=False
        self.loc_buttons=buttons
        self.unexpected_files=[]
        self.listener.new_dialogs=False
        self.timeout_s=20
        
    def wait(self):
        old_files=list(self.controller.listener.saved_files)
        t=30
        while 'donelookingforunexpected' not in self.listener.queue and t>0:
            t=t-INTERVAL
            time.sleep(INTERVAL)
        if t<=0:
            self.timeout()
            return
            
        if len(self.controller.listener.unexpected_files)>0:
            self.keep_around=True
            self.unexpected_files=list(self.listener.unexpected_files)
            self.listener.unexpected_files=[]
            
        self.listener.new_dialogs=True
        self.listener.queue.remove('donelookingforunexpected')
        
        while self.timeout_s>0:
            self.timeout_s-=INTERVAL
            if 'saveconfigsuccess' in self.listener.queue:
                self.listener.queue.remove('saveconfigsuccess')
                self.success()
                return
                
            elif 'saveconfigfailurefileexists' in self.listener.queue:
                self.listener.queue.remove('saveconfigfailurefileexists')
                self.interrupt('Error: File exists.\nDo you want to overwrite this data?')
                dict=self.loc_buttons['success']
                func=None
                for f in dict:
                    args=dict[f]
                    func=f
                    
                buttons={
                    'yes':{
                        self.remove_retry:[func,args]
                    },
                    'no':{
                    }
                }
                    
                self.set_buttons(buttons,button_width=20)
                return

            elif 'saveconfigfailure' in self.listener.queue:
                self.listener.queue.remove('saveconfigfailure')
                self.interrupt('Error: There was a problem with\nsetting the save configuration.\nIs the spectrometer connected?', info_string='Error: There was a problem with setting the save configuration\n')
                self.controller.spec_save_path=''
                self.controller.spec_basename=''
                self.controller.spec_num=None
                return
                
            time.sleep(INTERVAL)
            
        self.timeout(log_string='Error: Operation timed out while waiting to set save configuration.\n')
        

    def success(self):
        self.controller.spec_save_path=self.controller.spec_save_dir_entry.get()
        self.controller.spec_basename = self.controller.spec_basename_entry.get()
        spec_num=self.controller.spec_startnum_entry.get()
        self.controller.spec_num=int(spec_num)
        
        self.allow_exit=True
        dict=self.loc_buttons['success']
        self.log('\nSave configuration set.\n')
        if not self.keep_around:
            self.top.destroy()
        else:

            self.pbar.stop()
            
            self.top.geometry('400x300')
            self.set_label_text('Save configuration was set successfully,\nbut there are untracked files in the\ndata directory. Do these belong here?')
            self.log('Untracked files in data directory:\n'+'\n\t'.join(self.unexpected_files))
            listbox=ScrollableListbox(self.top,self.bg,self.entry_background, self.listboxhighlightcolor,)
            for file in self.unexpected_files:
                listbox.insert(END,file)
                
            listbox.config(height=1)

                
            
            self.set_buttons({'ok':{}})
            self.set_title('Warning: Untracked Files')
            
        for func in dict:
            args=dict[func]
            func(*args)
        

                
            
    
class WaitForSpectrumDialog(WaitDialog):
    def __init__(self, controller, title='Saving Spectrum...', label='Saving spectrum...', buttons={'cancel':{}}):
        timeout=int(controller.spec_config_count)/9+BUFFER
        super().__init__(controller, title, label, buttons={},timeout=timeout)
        
    def wait(self):
        old_files=list(self.controller.listener.saved_files)
        while self.timeout_s>0:
            #I took out the option to cancel because it was so dumb
            if self.canceled==True:
                self.interrupt("Operation canceled by user. Warning! This really\ndoesn't do anything except stop tkinter from waiting\n, you probably still saved a spectrum")
                return
                

            if 'failedtosavefile' in self.listener.queue:
                self.interrupt('Error: Failed to save file.\nAre you sure the spectrometer is connected?')
                self.listener.queue.remove('failedtosavefile')
                return

            elif 'noconfig' in self.listener.queue:
                self.listener.queue.remove('noconfig')
                self.controller.set_save_config(self.controller.take_spectrum, [True])
                self.finish()
                return
                
            elif 'nonumspectra' in self.controller.listener.queue:
                self.listener.queue.remove('nonumspectra')
                buttons={
                    'success':{
                        self.controller.take_spectrum:[True]
                    }
                }
                
                self.controller.configure_instrument(buttons)
                self.finish()
                return
            elif 'savedfile' in self.listener.queue:
                self.listener.queue.remove('savedfile')
                self.controller.spec_num+=1
                self.controller.spec_startnum_entry.delete(0,'end')
                spec_num_string=str(self.controller.spec_num)
                while len(spec_num_string)<NUMLEN:
                    spec_num_string='0'+spec_num_string
                self.controller.spec_startnum_entry.insert(0,spec_num_string)
                self.success()
                return
            elif 'savespecfailedfileexists' in self.listener.queue:
                self.listener.queue.remove('savespecfailedfileexists')
                self.interrupt('Error: File exists.\nDo you want to overwrite this data?')
                dict=self.loc_buttons['success']
                func=None
                for f in dict:
                    args=dict[f]
                    func=f
                buttons={
                    'yes':{
                        self.remove_retry:[func,args]
                    },
                    'no':{
                    }
                }
                    
                self.set_buttons(buttons,button_width=20)
                return
                
            time.sleep(INTERVAL)
            current_files=self.controller.listener.saved_files

                
            # if current_files==old_files:
            #     pass
            # else:
            #     for file in current_files:
            #         if file not in old_files:
            #             self.controller.spec_num+=1
            #             self.controller.spec_startnum_entry.delete(0,'end')
            #             spec_num_string=str(self.controller.spec_num)
            #             while len(spec_num_string)<NUMLEN:
            #                 spec_num_string='0'+spec_num_string
            #             self.controller.spec_startnum_entry.insert(0,spec_num_string)
            #             self.success()
            #             

            #               return
            time.sleep(INTERVAL)
            self.timeout_s-=INTERVAL
        self.timeout(log_string='Error: Operation timed out while waiting to save spectrum')

        
    def success(self):
        self.allow_exit=True
        numstr=str(self.controller.spec_num-1)
        while len(numstr)<NUMLEN:
            numstr='0'+numstr
        datestring=''
        datestringlist=str(datetime.datetime.now()).split('.')[:-1]
        for d in datestringlist:
            datestring=datestring+d
        info_string='\n Spectrum saved at '+datestring+ '\n\tNumber averaged: ' +str(self.controller.spec_config_count)+'\n\ti: '+self.controller.man_incidence_entry.get()+'\n\te: '+self.controller.man_emission_entry.get()+'\n\tfilename: '+self.controller.spec_save_path+'\\'+self.controller.spec_basename+numstr+'.asd'+'\n\tLabel: '+self.controller.label_entry.get()+'\n'
        
        self.console_log.insert(END,info_string)
        with open(self.controller.log_filename,'a') as log:
            log.write(info_string)
        self.controller.clear()

        self.interrupt('Success!')
        
class ErrorDialog(Dialog):
    def __init__(self, controller, title='Error', label='Error!', buttons={'ok':{}}, listener=None,allow_exit=False, info_string=None, topmost=True, button_width=30):
        self.listener=None
        if info_string==None:
            self.info_string=label+'\n'
        else:
            self.info_string=info_string
        super().__init__(controller, title, label,buttons,allow_exit=False, info_string=None, button_width=button_width)#self.info_string)
        if topmost==True:
            try:
                self.top.attributes("-topmost", True)
            except(Exception):
                print(str(Exception))

        


def limit_len(input, max):
    return input[:max]
    
def validate_int_input(input, min, max):
    try:
        input=int(input)
    except:
        return False
    if input>max: return False
    if input<min: return False
    
    return True
    

class RemoteFileExplorer(Dialog):
    def __init__(self,controller,write_command_loc, target=None,title='Select a directory',label='Select a directory',buttons={'ok':{},'cancel':{}}, directories_only=True):

        super().__init__(controller, title=title, buttons=buttons,label=label, button_width=20)
        
        self.timeout_s=BUFFER
        self.controller=controller
        self.remote_directory_worker=self.controller.remote_directory_worker
        self.listener=self.controller.listener
        self.write_command_loc=write_command_loc
        self.target=target
        self.current_parent=None
        self.directories_only=directories_only
        
        self.nav_frame=Frame(self.top,bg=self.bg)
        self.nav_frame.pack()
        self.new_button=Button(self.nav_frame, fg=self.textcolor,text='New Folder',command=self.askfornewdir, width=10)
        self.new_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.new_button.pack(side=RIGHT, pady=(5,5),padx=(0,10))

        self.path_entry_var = StringVar()
        self.path_entry_var.trace('w', self.validate_path_entry_input)
        self.path_entry=Entry(self.nav_frame, width=50,bg=self.entry_background,textvariable=self.path_entry_var,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.path_entry.pack(padx=(5,5),pady=(5,5),side=RIGHT)
        self.back_button=Button(self.nav_frame, fg=self.textcolor,text='<-',command=self.back,width=1)
        self.back_button.config(fg=self.buttontextcolor,highlightbackground=self.highlightbackgroundcolor,bg=self.buttonbackgroundcolor)
        self.back_button.pack(side=RIGHT, pady=(5,5),padx=(10,0))
        
        # self.scroll_frame=Frame(self.top,bg=self.bg)
        # self.scroll_frame.pack(fill=BOTH, expand=True)
        # self.scrollbar = Scrollbar(self.scroll_frame, orient=VERTICAL)
        # self.listbox = Listbox(self.scroll_frame,yscrollcommand=self.scrollbar.set, selectmode=SINGLE,bg=self.entry_background, selectbackground=self.listboxhighlightcolor, height=15)

        #   self.scrollbar.config(command=self.listbox.yview)
        # self.scrollbar.pack(side=RIGHT, fill=Y,padx=(0,10))
        # self.listbox.pack(side=LEFT,expand=True, fill=BOTH,padx=(10,0))
        self.listbox=ScrollableListbox(self.top,self.bg,self.entry_background, self.listboxhighlightcolor,)
        self.listbox.bind("<Double-Button-1>", self.expand)
        self.path_entry.bind('<Return>',self.go_to_path)
        
        if target.get()=='':
            self.expand(newparent='C:\\Users')
            self.current_parent='C:\\Users'
        else:
            if directories_only:
                self.expand(newparent=target.get().replace('/','\\'))
            else:
                path=target.get().replace('/','\\')
                if '\\' in path:
                    path_el=path.split('\\')
                    if '.' in path_el[-1]:
                        path='\\'.join(path_el[:-1])
                    self.expand(newparent=path)
                else:
                    self.expand(newparent=path)
            
    def validate_path_entry_input(self,*args):
        text=self.path_entry.get()
        text=rm_reserved_chars(text)

        self.path_entry.delete(0,'end')
        self.path_entry.insert(0,text)      
        
    def askfornewdir(self):
        input_dialog=InputDialog(self.controller, self)

    def mkdir(self, newdir):
        status=self.remote_directory_worker.mkdir(newdir)

        if status=='mkdirsuccess':
            self.expand(None,'\\'.join(newdir.split('\\')[0:-1]))
            self.select(newdir.split('\\')[-1])
        elif status=='mkdirfailedfileexists':
            dialog=ErrorDialog(self.controller,title='Error',label='Could not create directory:\n\n'+newdir+'\n\nFile exists.')
            self.expand(newparent=self.current_parent)
        elif status=='mkdirfailed':
            dialog=ErrorDialog(self.controller,title='Error',label='Could not create directory:\n\n'+newdir)
            self.expand(newparent=self.current_parent)
        
    def back(self):
        if len(self.current_parent)<4:
            return
        parent='\\'.join(self.current_parent.split('\\')[0:-1])
        self.expand(newparent=parent)
        
    def go_to_path(self, source):
        parent=self.path_entry.get().replace('/','\\')
        self.path_entry.delete(0,'end')
        self.expand(newparent=parent)
        
    
    def expand(self, source=None, newparent=None, buttons=None,select=None, timeout=5,destroy=False):
        global CMDNUM
        if newparent==None:
            index=self.listbox.curselection()[0]
            if self.listbox.itemcget(index, 'foreground')=='darkblue':
                return
            newparent=self.current_parent+'\\'+self.listbox.get(index)
        if newparent[1:2]!=':' or len(newparent)>2 and newparent[1:3]!=':\\':
            dialog=ErrorDialog(self.controller,title='Error: Invalid input',label='Error: Invalid input.\n\n'+newparent+'\n\nis not a valid filename.')
            return
        if newparent[-1]=='\\':
            newparent=newparent[:-1]
        #Send a command to the spec compy asking it for directory contents
        if self.directories_only==True:
            status=self.remote_directory_worker.get_contents(newparent)
        else:
            status=self.remote_directory_worker.get_contents(newparent)
        
        #if we succeeded, the status will be a list of the contents of the directory
        if type(status)==list:

            self.listbox.delete(0,'end')
            for dir in status:
                if dir[0:2]=='~:':
                    self.listbox.insert(END,dir[2:])
                    self.listbox.itemconfig(END, fg='darkblue')
                else:
                    self.listbox.insert(END,dir)

            self.current_parent=newparent
            
            self.path_entry.delete(0,'end')
            self.path_entry.insert('end',newparent)
            if select!=None:
                self.select(select)
            
            if destroy:
                self.top.destroy()

                
        elif status=='listdirfailed':
            if self.current_parent==None:
                self.current_parent='\\'.join(newparent.split('\\')[:-1])
                if self.current_parent=='':
                    self.current_parent='C:\\Users'
            if buttons==None:
                buttons={
                    'yes':{
                        self.mkdir:[newparent]
                    },
                    'no':{
                        self.expand:[None,self.current_parent]
                    }
                }
            dialog=ErrorDialog(self.controller,title='Error',label=newparent+'\ndoes not exist. Do you want to create this directory?',buttons=buttons)
        elif status=='listdirfailedpermission':
            dialog=ErrorDialog(self.controller,label='Error: Permission denied for\n'+newparent)
            return
        elif status=='timeout':
            dialog=ErrorDialog(self.controller, label='Error: Operation timed out.\nCheck that the automation script is running on the spectrometer computer.')
            
    def select(self,text):
        if '\\' in text:
            text=text.split('\\')[0]
            

        try:
            index = self.listbox.get(0, 'end').index(text)
        except:
            #time.sleep(0.5)
            print('except')
            #self.select(text)
            index=0

        self.listbox.selection_set(index)
        self.listbox.see(index)
        
    def ok(self):
        index=self.listbox.curselection()
        if len(index)>0 and self.directories_only:
            if self.listbox.itemcget(index[0], 'foreground')=='darkblue':
                index=[]
        elif len(index)==0 and not self.directories_only:
            return
                
        self.target.delete(0,'end')

        if self.directories_only:
            if len(index)>0 and self.path_entry.get()==self.current_parent:
    
                self.target.insert(0,self.current_parent+'\\'+self.listbox.get(index[0]))
                self.top.destroy()
            elif self.path_entry.get()==self.current_parent:
                self.target.insert(0,self.current_parent)
                self.top.destroy()
            else:
                buttons={
                    'yes':{
                        self.mkdir:[self.path_entry.get()],
                        self.expand:[None,'\\'.join(self.path_entry.get().split('\\')[0:-1])],
                        self.select:[self.path_entry.get().split('\\')[-1]],
                        self.ok:[]
                    },
                    'no':{
                    }
                }
                self.expand(newparent=self.path_entry.get(), buttons=buttons, destroy=True)
                self.target.insert(0,self.current_parent)
        else:
            if len(self.listbox.curselection())>0 and self.path_entry.get()==self.current_parent and  self.listbox.itemcget(index[0], 'foreground')=='darkblue':
    
                self.target.insert(0,self.current_parent+'\\'+self.listbox.get(index[0]))
                self.top.destroy()
            
class RemoteDirectoryWorker():
    def __init__(self, read_command_loc, write_command_loc,listener):
        self.write_command_loc=write_command_loc
        self.read_command_loc=read_command_loc
       
        self.listener=listener
        self.timeout_s=BUFFER
    
    def wait_for_contents(self,cmdfilename):
        #Wait to hear what the listener finds
        t=self.timeout_s
        print(cmdfilename)
        while t>0:
            #If we get a file back with a list of the contents, replace the old listbox contents with new ones.
            if cmdfilename in self.listener.queue:
                contents=[]
                with open(self.read_command_loc+cmdfilename,'r') as f:
                    next=f.readline().strip('\n')
                    while next!='':
                        contents.append(next)
                        next=f.readline().strip('\n')
                self.listener.queue.remove(cmdfilename)
                return contents
                
            elif 'listdirfailed' in self.listener.queue:
                self.listener.queue.remove('listdirfailed')
                return 'listdirfailed'
                
            elif 'listdirfailedpermission' in self.listener.queue:
                self.listener.queue.remove('listdirfailedpermission')
                return 'listdirfailedpermission'
            
            elif 'listfilesfailed' in self.listener.queue:
                self.listener.queue.remove('listfilesfailed')
                return 'listfilesfailed'
            
            time.sleep(INTERVAL)
            t-=INTERVAL 
            
        return 'timeout'
        
        
    #Assume parent has already been validated, but don't assume it exists
    def get_dirs(self,parent):
        global CMDNUM
        cmdfilename=encrypt('listdir',CMDNUM, parameters=[parent])
        CMDNUM=CMDNUM+1
        try:
            with open(self.write_command_loc+cmdfilename,'w+') as f:
                pass
        except:
                pass
        
        return self.wait_for_contents(cmdfilename)
                
    def get_contents(self,parent):
        global CMDNUM
        cmdfilename=encrypt('listcontents',CMDNUM, parameters=[parent])
        CMDNUM=CMDNUM+1
        try:
            with open(self.write_command_loc+cmdfilename,'w+') as f:
                pass
        except:
                pass
        
        return self.wait_for_contents(cmdfilename)
        
    def mkdir(self, newdir):
        global CMDNUM
        filename=encrypt('mkdir',CMDNUM, parameters=[newdir])

        CMDNUM=CMDNUM+1
        try:
            with open(self.write_command_loc+filename,'w+') as f:
                pass
        except:
                pass
                
        while True:
            if 'mkdirsuccess' in self.listener.queue:
                self.listener.queue.remove('mkdirsuccess')
                return 'mkdirsuccess'
            elif 'mkdirfailedfileexists' in self.listener.queue:
                self.listener.queue.remove('mkdirfailedfileexists')
                return 'mkdirfailedfileexists'
            elif 'mkdirfailed' in self.listener.queue:
                self.listener.queue.remove('mkdirfailed')
                return 'mkdirfailed'
                
        time.sleep(INTERVAL)

class ScrollableListbox(Listbox):
    def __init__(self, frame, bg, entry_background, listboxhighlightcolor):
        
        self.scroll_frame=Frame(frame,bg=bg)
        self.scroll_frame.pack(fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self.scroll_frame, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y,padx=(0,10))
        self.scrollbar.config(command=self.yview)
        
        super().__init__(self.scroll_frame,yscrollcommand=self.scrollbar.set, selectmode=SINGLE,bg=entry_background, selectbackground=listboxhighlightcolor, height=15)
        self.pack(side=LEFT,expand=True, fill=BOTH,padx=(10,0))

class ScrollableListboxBroken(ttk.Treeview):
    def __init__(self, frame, bg, entry_background, listboxhighlightcolor):
        
        self.scroll_frame=Frame(frame,bg=bg)
        self.scroll_frame.pack(fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self.scroll_frame, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y,padx=(0,10))
        self.scrollbar.config(command=self.yview)
        
        super().__init__(self.scroll_frame,yscrollcommand=self.scrollbar.set, selectmode='browse',  height=15)
        self.pack(side=LEFT,expand=True, fill=BOTH,padx=(10,0))
        
        # background=entry_background,
        # selectbackground=listboxhighlightcolor,


class InputDialog(Dialog):
    def __init__(self, controller, fexplorer,label='Enter input', title='Enter input'):
        super().__init__(controller,label=label,title=title, buttons={'ok':{self.get:[]},'cancel':{}},button_width=15)
        self.dir_entry=Entry(self.top,width=40,bg=self.entry_background,selectbackground=self.selectbackground,selectforeground=self.selectforeground)
        self.dir_entry.pack(padx=(10,10))
        self.listener=self.controller.listener


        self.fexplorer=fexplorer


    def get(self):
        subdir=self.dir_entry.get()
        if subdir[0:3]!='C:\\':
            self.fexplorer.mkdir(self.fexplorer.current_parent+'\\'+subdir) 
        else:self.fexplorer.mkdir(subdir)
        
        # while True:
        #     print(self.listener.queue)
        #     if 'mkdirsuccess' in self.listener.queue:
        #         self.listener.queue.remove('mkdirsuccess')
        #         self.log('Directory created:\n\t'+self.fexplorer.current_parent+'\\'+subdir)
        #         self.top.destroy()
        #         self.fexplorer.expand(newparent=self.fexplorer.current_parent, select=subdir)
        #         return True
        #     elif 'mkdirfailed' in self.listener.queue:
        #         print('fail!')
        #         self.listener.queue.remove('mkdirfailed')
        #         self.top.destroy()
        #         dialog=ErrorDialog(self.controller,label='Error: failed to create directory.\n'+self.fexplorer.current_parent+'\\'+subdir)
        #         return False
        #     time.sleep(0.2)
        # 
        # thread = Thread(target =self.wait)
        # thread.start()  
        
class Listener(Thread):
    def __init__(self, read_command_loc, test=False):
        Thread.__init__(self)
        self.read_command_loc=read_command_loc
        self.controller=None
        self.connection_checker=ConnectionChecker(read_command_loc,'not main',controller=self.controller, func=self.listen)
        self.queue=[]
        self.cmdfiles0=os.listdir(self.read_command_loc)

    def run(self):
        while True:
            #I think this calls listen if we are connected?
            connection=self.connection_checker.check_connection(False)
            time.sleep(INTERVAL)
            
    def listen(self):
        pass

    def set_controller(self,controller):
        self.controller=controller
        self.connection_checker.controller=controller
            

        

    
class PiListener(Listener):
    def __init__(self, read_command_loc, test=False):
        super().__init__(read_command_loc)

            
            
    def listen(self):
        self.cmdfiles=os.listdir(self.read_command_loc)  
        if self.cmdfiles==self.cmdfiles0:
            pass
        else:
            for cmdfile in self.cmdfiles:
                if cmdfile not in self.cmdfiles0:
                    cmd, params=decrypt(cmdfile)

                    print('Read command: '+cmd)
                    if 'savedfile' in cmd:
                        self.saved_files.append(params[0])
                        self.queue.append('savedfile')
                        
                        
class SpecListener(Listener):
    def __init__(self, read_command_loc):
        super().__init__(read_command_loc)
        self.unexpected_files=[]
        self.wait_for_unexpected_count=0

        self.alert_lostconnection=True
        self.new_dialogs=True
        
    def run(self):
        while True:
            connection=self.connection_checker.check_connection(False)
            time.sleep(INTERVAL)
            
    def listen(self):
        self.cmdfiles=os.listdir(self.read_command_loc)  
        if self.cmdfiles==self.cmdfiles0:
            pass
        else:
            for cmdfile in self.cmdfiles:
                if cmdfile not in self.cmdfiles0:
                    cmd, params=decrypt(cmdfile)

                    print('Read command: '+cmd)
                    if 'savedfile' in cmd:
                        self.saved_files.append(params[0])
                        self.queue.append('savedfile')
                        
                    elif 'failedtosavefile' in cmd:
                        self.queue.append('failedtosavefile')
                        
                    elif 'processsuccess' in cmd:
                        self.queue.append('processsuccess')
                        
                    elif 'processerrorfileexists' in cmd:
                        self.queue.append('processerrorfileexists')
                    
                    elif 'processerrorwropt' in cmd:
                        self.queue.append('processerrorwropt')
                    
                    elif 'processerror' in cmd:
                        self.queue.append('processerror')
                    
                    elif 'wrsuccess' in cmd:
                        self.queue.append('wrsuccess')
                    
                    elif 'donelookingforunexpected' in cmd:
                        self.queue.append('donelookingforunexpected')
                    
                    elif 'saveconfigerror' in cmd:
                        self.queue.append('saveconfigfailure')
                    
                    elif 'saveconfigsuccess' in cmd:
                        self.queue.append('saveconfigsuccess')
                    
                    elif 'noconfig' in cmd:
                        print("Spectrometer computer doesn't have a file configuration saved (python restart over there?). Setting to current configuration.")
                        self.queue.append('noconfig')
                    
                    elif 'nonumspectra' in cmd:
                        print("Spectrometer computer doesn't have an instrument configuration saved (python restart over there?). Setting to current configuration.")
                        self.queue.append('nonumspectra')
                    
                    elif 'saveconfigfailedfileexists' in cmd:
                        self.queue.append('saveconfigfailurefileexists')
                    elif 'savespecfailedfileexists' in cmd:
                        self.queue.append('savespecfailedfileexists')
                    
                    elif 'listdir' in cmd:
                        if 'listdirfailed' in cmd:
                            if 'permission' in cmd:
                                self.queue.append('listdirfailedpermission')
                            else:
                                self.queue.append('listdirfailed')
                        else:
                            self.queue.append(cmdfile)      
                    elif 'listcontents' in cmd:
                        self.queue.append(cmdfile)  
                    
                    elif 'mkdirsuccess' in cmd:
                        self.queue.append('mkdirsuccess')
                    
                    elif 'mkdirfailedfileexists' in cmd:
                        self.queue.append('mkdirfailedfileexists')
                    elif 'mkdirfailed' in cmd:
                        self.queue.append('mkdirfailed')
                    
                    elif 'iconfigsuccess' in cmd:
                        self.queue.append('iconfigsuccess')
                        
                    elif 'datacopied' in cmd:
                        self.queue.append('datacopied')
                        
                    elif 'datafailure' in cmd:
                        self.queue.append('datafailure')
                    
                    elif 'iconfigfailure' in cmd:
                        self.queue.append('iconfigfailure')
                        
                    elif 'optsuccess' in cmd:
                        self.queue.append('optsuccess')
                    
                    elif 'optfailure' in cmd:
                        self.queue.append('optfailure')
                        
                    elif 'notwriteable' in cmd:
                        self.queue.append('notwriteable')
                        
                    elif 'yeswriteable' in cmd:
                        self.queue.append('yeswriteable')
                        
                    elif 'lostconnection' in cmd:
                        print('lostconnection')
                        os.remove(read_command_loc+cmdfile)
                        self.cmdfiles.remove(cmdfile)
                        if self.alert_lostconnection:
                            self.alert_lostconnection=False

                            buttons={
                                'retry':{
                                    self.set_alert_lostconnection:[True]
                                    },
                                'work offline':{
                                },
                                'exit':{
                                    exit_func:[]
                                }
                            }
                            try:
                                dialog=ErrorDialog(controller=self.controller, title='Lost Connection',label='Error: RS3 lost connection with the spectrometer.\nCheck that the spectrometer is on.',buttons=buttons,button_width=15)
                            except:
                                print('Ignoring an error in Listener when I make a new error dialog')
                    elif 'rmsuccess' in cmd:
                        self.queue.append('rmsuccess')
                    elif 'rmfailure' in cmd:
                        self.queue.append('rmfailure')
                    elif 'unexpectedfile' in cmd:
                        if self.new_dialogs:
                            try:
                                dialog=ErrorDialog(self.controller, title='Untracked Files',label='There is an untracked file in the data directory.\nDoes this belong here?\n\n'+params[0])
                            except:
                                print('Ignoring an error in Listener when I make a new error dialog')
                        else:
                            self.unexpected_files.append(params[0])
                    else:
                        print('unexpected cmd: '+cmdfile)
            #This line always prints twice if it's uncommented, I'm not sure why.
            #print('forward!')

        self.cmdfiles0=list(self.cmdfiles)

    def set_alert_lostconnection(self,bool):
        self.alert_lostconnection=bool
        


        
def decrypt(encrypted):
    cmd=encrypted.split('&')[0]
    params=encrypted.split('&')[1:]
    i=0
    for param in params:
        params[i]=param.replace('+','\\').replace('=',':')
        params[i]=params[i].replace('++','+')
        i=i+1
    return cmd,params
    
def encrypt(cmd, num, parameters=[]):
    filename=cmd+str(num)
    for param in parameters:
        param=param.replace('/','+')
        param=param.replace('\\','+')
        param=param.replace(':','=')
        filename=filename+'&'+param
    return filename
    
def rm_reserved_chars(input):
    output= input.replace('&','').replace('+','').replace('=','').replace('$','').replace('^','').replace('*','').replace('(','').replace(',','').replace(')','').replace('@','').replace('!','').replace('#','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace(',','').replace('?','').replace('~','').replace('"','').replace("'",'').replace(';','').replace('`','')
    return output
    
def numbers_only(input):
    output=''
    for digit in input:
        if digit=='1' or digit=='2' or digit=='3' or digit=='4'or digit=='5'or digit=='6' or digit=='7' or digit=='8' or digit=='9' or digit=='0':
            output+=digit
    return output
    
    



if __name__=='__main__':
    main()