#AUTHOR: Matthew Ocando

import tkinter as tk
from tkinter import ttk,messagebox,PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from PIL import Image
import requests
from io import BytesIO

import serial
import os
import sys

import math
import time

class TtestFrame(ttk.Frame):
    """Tkinter Frame containing relevant widgets"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid(row=0, column=0)
        
        #tk variables
        #self.this_is_a_string = tk.StringVar()

        #Arduino variables
        self.fileName = "pressure-data.csv"
        self.baud = 115200

        #temporary variables for plotting test Graph
        self.counter = 0
        self.x=[]
        self.y=[]

        self.pressureout=tk.StringVar(value="Connecting to Arduino...")
        self.timerout=tk.StringVar(value="0:00")
        self.arduino_cnct = tk.StringVar(value="Attempting to connect to arduino...")

        #marker variables
        self.begin = False
        self.end = False

        #seaborn realted variables
        sns.set_style('whitegrid')
        sns.set_palette('deep')
        self.red = sns.xkcd_rgb['vermillion']
        self.blue = sns.xkcd_rgb['dark sky blue']
        self.green = sns.xkcd_rgb['leaf green']

        #matplotlib related variables
        self.fig, self.ax = plt.subplots()

        self.makewidgets()
    
    def makewidgets(self):
        """Creates widgets in TtestFrame

        returns: Nothing."""

        #ttk.Label(self, text='Pressure Readout Graph',font=16).grid(row=0,column=0,sticky=tk.W)
        ttk.Button(self, text='START',command=self.start).grid(row=2, column=0, sticky=tk.W)
        ttk.Button(self, text='STOP',command=self.stop).grid(row=2, column=1, sticky=tk.W)
        ttk.Button(self, text='Connect',command=self.cnct).grid(row=2, column=0, sticky=tk.E)
        #ttk.Button(self, text='Predict',command=self.ml).grid(row=2,column=2,sticky=tk.W)
        ttk.Button(self, text = 'RESTART', command = self.restart).grid(row=3, column =0, sticky = tk.W)
        ttk.Button(self, text = 'SAVE TO CSV', command = self.save).grid(row=4, column =0, sticky = tk.W)
        ttk.Entry(self, textvariable=self.pressureout, font=("Arial",45)).grid(row=0,column=0,sticky=tk.W)
        ttk.Entry(self, textvariable=self.timerout, font=("Arial",45)).grid(row=1,column=0,stick=tk.W)

    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def cnct(self):
        notconnected = True
        while(notconnected):
            for port in ["COM0","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COM10"]:
                self.arduino_port = port
                time.sleep(0.5)
                try:
                    self.ser = serial.Serial(self.arduino_port, self.baud)
                    notconnected=False
                    break
                except:
                    pass
        self.pressureout.set("Connected!")
        time.sleep(2)

    def save(self):
        self.file = open(self.fileName, "a")
        for value in self.y:
            self.file.write(str(value) +",")
        self.file.close()

    def start(self):
        self.starttime=time.time()
        self.start_readout()

    def stop(self):
        self.stop_readout()

    def start_readout(self):
        """collects pressure data and plots

        returns: Nothing."""
        
        #Arduino code
        self.getData = str(self.ser.readline())
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.data = self.getData[2:][:-3]

        self.xi = time.time()-self.starttime
        self.yi = float(self.data)

        self.x.append(self.xi)
        self.y.append(self.yi)

        self.pressureout.set(self.yi)
        self.xi_temp_s = int(self.xi%60)
        self.xi_temp_m = int(self.xi/60)
        self.timestring = str(self.xi_temp_m)+":"+str(self.xi_temp_s).zfill(2)
        self.timerout.set(self.timestring)

        #self.ax.clear()
        #self.ax.plot()
        # self.ax.set_xlim([-20, 20])
        #xmin, xmax = self.ax.get_xlim()
        #ymin, ymax = self.ax.get_ylim()
        # xmin, xmax, ymin, ymax = plt.axis()
        self.after_id = self.after(100, self.start_readout)

    def stop_readout(self):
        """ stops readout of plot

        Returns: Nothing"""
        self.after_cancel(self.after_id)

    '''def start_plot(self):
        self.mark = 'o'
        self.size = 3
        self.color = self.red
        self.ax.plot(self.xi, self.yi, color=self.color, marker=self.mark, markersize=self.size, linestyle='None')
        # self.ax.annotate('{:3.1f}%'.format(self.p_value * 100), 
        #                 xytext=(self.diff_measured + (xmax-self.diff_measured)*0.5, ymax//2), 
        #                 xy=(self.diff_measured, ymax//2), 
        #                 multialignment='right',
        #                 va='center',
        #                 color=self.red,
        #                 size='large',
        #                 arrowprops={'arrowstyle': '<|-', 
        #                             'lw': 2, 
        #                             'color': self.red, 
        #                             'shrinkA': 10})
        self.canvas.draw()
        self.after_id_plot = self.after(5000, self.start_plot)'''

    '''def stop_plot(self):
        self.after_cancel(self.after_id_plot)'''

    
    '''def ml(self):
        """uses ml to calc linear regression best fit for data set
        
        Returns: Nothing"""
        self.xml = np.array(self.x).reshape(-1,1) 
        self.yml = np.array(self.y).reshape(-1,1)       
        model = LinearRegression()
        

        poly = PolynomialFeatures(degree=5, include_bias=False)
        poly.fit(self.xml)
        self.x_poly = poly.transform(self.xml)

        #linear
        #model.fit(self.xml, self.yml)
        #self.y_pred = model.predict(self.xml)
        #self.ts = model.score(self.xml, self.y_pred)
        #self.ax.plot(self.x,self.y_pred, color=self.blue)
        #self.canvas.draw()

        #polynomial
        model.fit(self.x_poly,self.yml)
        self.y_pred = model.predict(self.x_poly)
        #self.polyscore = model.score(self.xml, self.y_pred)
        self.ax.plot(self.x,self.y_pred, color=self.green)
        self.canvas.draw()'''

root = tk.Tk()
root.resizable(False, False)
root.title("Chem-E-Car Readout")
TtestFrame(parent=root)
root.mainloop()