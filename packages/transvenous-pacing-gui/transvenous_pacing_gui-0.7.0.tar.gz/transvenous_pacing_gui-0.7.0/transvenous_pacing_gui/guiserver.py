# Pip Modules
import tkinter as tk
from tkinter import ttk

from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import StringVar
from tkinter import OptionMenu

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random

import serial
from serial import SerialException
import serial.tools.list_ports

# Project Modules
from signals import Signals
from server import Server

from queue import Queue

class StudentGUI(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.socket_queue = Queue()

        self.server = Server(port=25565)
        self.server.start(self.socket_queue)

        self.ecg_signals = Signals()

        self.hr = IntVar(self, value=80)
        self.threshold = IntVar(self, value=20)

        self.position = StringVar(self, value='RIP')
        self.serial_position = IntVar(self, value='0')
        self.hr1 = StringVar(self, value='0')

        self.override_position = BooleanVar(self, value=False)

        self.pathway_1 = IntVar(self, value=0)
        self.pathway_2 = IntVar(self, value=0)

        # Take care of plotting
        fig = plt.Figure(figsize=(14, 4.5), dpi=100,facecolor='k',edgecolor='k')

        self.new_x = [0.0]
        self.new_y = [0.0]

        self.last_x = 0
        self.last_x_lim = 0

        self.position_to_show = 0

        self.variation = 0

        Options=['']
        Options.extend(serial.tools.list_ports.comports())

        # GUI Utilisation
        self.wait_for_update = BooleanVar(self, value=False)
        self.wait_for_position = BooleanVar(self, value=False)
        self.wait_for_pathway_1 = BooleanVar(self, value=False)
        self.wait_for_pathway_2 = BooleanVar(self, value=False)
        
        self.s = 'RIP'
        self.ser = None

        BPM="BPM "
        whites="                                  "
        tk.Label(self, text="Simulation ECG",font="Times 30 bold", bg="black",fg="lime green").grid(row=0, column=1)
        tk.Label(self, textvariable=self.hr1,font='Times 24 bold',bg="black", fg="lime green").grid(row=0, column=3)
        tk.Label(self, text="BPM", font='Times 24 bold', bg="black", fg="lime green").grid(row=0, column=2)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=1, column=1)

        self.variable = StringVar(self)
        self.variable.set(Options[0]) #Default option

        w=OptionMenu(self, self.variable, *Options)
        w.grid(row=2, column=1)

        self.variable.trace('w', self.change_dropdown)

        # ===== ECG Signal Setup
        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(self.last_x_lim, 4)
        self.ax.set_ylim(-3.0, 3.0)
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.xaxis.set_tick_params(width=1, top=True)
        self.ax.set_facecolor('black')

        self.line, = self.ax.plot(0, 0)
        self.ax.get_lines()[0].set_color("xkcd:lime")
        self.ani = animation.FuncAnimation(fig, self.animate, frames=31, interval=24, repeat=True, blit=True)

        # Polling Initialisation
        self.after(10, self.read_socket)

    def animate(self, i):
        if self.override_position.get():
            [x, y] = self.ecg_signals.get_signal(self.position.get(), self.hr.get(), self.variation)
        
            if self.position.get() == 0:
                self.hr1.set(0)
            else:
                self.hr1.set(self.hr.get())
        else:
            position_index = self.serial_position.get()

            if position_index == 4:
                position_index = position_index + self.pathway_1.get()
            elif position_index == 6:
                position_index = position_index + self.pathway_2.get()
            else:
                position_index = position_index

            print(self.ecg_signals.signal_index[position_index])

            if position_index == 0:
                if self.position_to_show == 1:
                    position_index = 0
                else:
                    position_index = self.position_to_show
            else:
                self.position_to_show = position_index

            if position_index == 0:
                self.hr1.set(0)
            else:
                self.hr1.set(self.hr.get())

            [x, y] = self.ecg_signals.get_signal(self.ecg_signals.signal_index[position_index], self.hr.get(), self.variation)

        x_val = self.last_x + x[i]

        if x_val > self.new_x[-1]:
            self.new_x.append(x_val)
            self.new_y.append(y[i])

            self.line.set_data(self.new_x, self.new_y)  # update the data
        
        if i == 30:
            variation = random.randint(0, 1)
            self.last_x = self.new_x[-1]
            
        if self.new_x[-1] >= self.last_x_lim + 5:
            self.last_x_lim += 5
            self.ax.set_xlim(self.last_x_lim, self.last_x_lim + 5)
        
        return self.line,

    def change_dropdown(self, *args):
        if not self.variable.get() == '':
            try:
                choice = self.variable.get().split(' -')
                self.ser = serial.Serial(choice[0], 9600)
                print('Connection established.')
                self.after(10, self.read_serial)
            except SerialException as e:
                print('Error: {}'.format(e))

    def read_socket(self):
        if not self.socket_queue.empty():
            message = self.socket_queue.get()

            print(message)

            if self.wait_for_update.get():
                result = [x.strip() for x in message.decode('utf-8').split(',')]

                self.hr.set(result[0])
                self.threshold.set(result[1])
                
                self.wait_for_update.set(False)
            elif self.wait_for_position.get():
                self.position.set(message.decode('utf-8'))
                self.wait_for_position.set(False)
                self.override_position.set(True)
            elif self.wait_for_pathway_1.get():
                self.pathway_1.set(int(message.decode('utf-8')))
                print(self.pathway_1.get())
                self.wait_for_pathway_1.set(False)
            elif self.wait_for_pathway_2.get():
                self.pathway_2.set(int(message.decode('utf-8')))
                print(self.pathway_2.get())
                self.wait_for_pathway_2.set(False)
            else:
                if message == b'update':
                    self.wait_for_update.set(True)
                elif message == b'start-pos':
                    self.wait_for_position.set(True)
                elif message == b'stop-pos':
                    self.override_position.set(False)
                elif message == b'chpa1':
                    self.wait_for_pathway_1.set(True)
                elif message == b'chpa2':
                    self.wait_for_pathway_2.set(True)
                elif message == b'close':
                    self.destroy()
            
        self.after(10, self.read_socket)

    def read_serial(self):
        if not self.ser == None:
            try:
                if self.ser.in_waiting:
                    self.s = self.ser.read()
                    self.serial_position.set(int(self.s))
                    print(int(self.s))
                
            except Exception as e:
                print('Error: {}'.format(e))

        self.after(10, self.read_serial)

    def stop_gui(self):
        # Clean-up
        try:
            self.server.stop()
            self.ser.close()
        except Exception as e:
            print(e)
