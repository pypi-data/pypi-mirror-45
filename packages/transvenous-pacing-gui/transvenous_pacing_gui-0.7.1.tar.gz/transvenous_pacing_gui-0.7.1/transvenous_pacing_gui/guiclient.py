import tkinter as tk
from tkinter import ttk

from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import Label
from tkinter import Radiobutton
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Scale

from client import Client

class InstructorGUI(tk.Frame):
    # Settings
    header_1_style = "TkDefaultFont 18 bold"
    header_2_style = "TkDefaultFont 16 bold"
    default_style  = "TkDefaultFont 14"

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.client = Client(port=25565)

        # GUI Variables
        self.message = StringVar(self)
        self.host = StringVar(self, value=self.client.get_hostname())
        self.hr = StringVar(self, value=80)
        self.threshold = StringVar(self, value=20)
        self.position = StringVar(self, value='SVC')
        self.pathway_1 = IntVar(self, value=0)
        self.pathway_2 = IntVar(self, value=0)

         # ============ Main Sides ===========
        frame_left = Frame(self, bd=1, relief=tk.SUNKEN)
        frame_left.pack(side=tk.LEFT, padx=10, pady=10)
        Label(frame_left, text="Real-Time Settings", font=self.header_1_style).pack()

        frame_right = Frame(self, bd=1, relief=tk.SUNKEN)
        frame_right.pack(side=tk.RIGHT, padx=10, pady=10)
        Label(frame_right, text="Override Settings", font=self.header_1_style).pack()

        # ============ Connection Space ===============
        frame_connection = Frame(frame_left)
        frame_connection.pack(pady=5)

        Label(frame_connection, text="Hostname", font=self.default_style).pack(side=tk.LEFT)

        entry_hostname = Entry(frame_connection, textvariable=self.host, font=self.default_style)
        entry_hostname.pack(side=tk.LEFT)

        btn_connect = Button(frame_connection, text="Connect", command=self.connect, fg="green", font=self.default_style)
        btn_connect.pack(side=tk.LEFT)

        # ============ Customisation Space ===============
        frame_signal = Frame(frame_left)
        frame_signal.pack(pady=5)

        Label(frame_signal, text="Heart Rate", font=self.default_style).grid(row=0, column=0)

        scale_hr = Scale(frame_signal, from_=0, to=200, length=150, variable=self.hr, orient=tk.HORIZONTAL)
        scale_hr.grid(row=0, column=1)

        entry_hr = Entry(frame_signal, textvariable=self.hr, font=self.default_style, width=4)
        entry_hr.grid(row=0, column=2)

        Label(frame_signal, text="Pacing Threshold", font=self.default_style).grid(row=1, column=0)

        scale_threshold = Scale(frame_signal, from_=0, to=200, length=150, variable=self.threshold, orient=tk.HORIZONTAL)
        scale_threshold.grid(row=1, column=1)

        entry_threshold = Entry(frame_signal, textvariable=self.threshold, font=self.default_style, width=4)
        entry_threshold.grid(row=1, column=2)

        btn_send_customisations = Button(frame_signal, text="Update ECG Settings", command=self.send_customisations, fg="green", font=self.default_style, pady=5)
        btn_send_customisations.grid(row=2, columnspan=3)

        # ============ Command Space ===============
        # frame_command = Frame(frame_left)
        # frame_command.pack(pady=5)

        # Label(frame_command, text="Command", font=default_style).pack(side=tk.LEFT)

        # entry_command = Entry(frame_command, textvariable=message, font=default_style)
        # entry_command.pack(side=tk.LEFT)

        # btn_send_command = Button(frame_command, text="Send", command=send_command, fg="green")
        # btn_send_command.pack(side=tk.LEFT)

        # ============ Position Selection ===============
        frame_position = Frame(frame_right)
        frame_position.pack(pady=5)

        POSITIONS = [
            ("Superior Vena Cava", "SVC"),
            ("High Right Atrium", "HRA"),
            ("Mid Right Atrium", "MRA"),
            ("Low Right Atrium", "LRA"),
            ("Inferior Vena Cava", "IVC"),
            ("Right Ventricle", "RV"),
            ("Right Ventricular Wall", "RVW"),
            ("Pulmonary Artery", "PA"),
            ("Asystole", "RIP"),
        ]

        Label(frame_position, text="Show Manual Position", font=self.default_style).pack()

        for button_text, position_value in POSITIONS:
            Radiobutton(frame_position, text=button_text, value=position_value, variable=self.position, font=self.default_style).pack()

        btn_send_position = Button(frame_position, text="Start Override", command=self.send_position, fg="green", font=self.default_style)
        btn_send_position.pack(side=tk.LEFT)

        btn_stop_position = Button(frame_position, text="Stop Override", command=self.stop_position, fg="red", font=self.default_style)
        btn_stop_position.pack(side=tk.RIGHT)

        # ========== Pathway Selection ==============
        frame_pathway = Frame(frame_left)
        frame_pathway.pack(pady=5)

        PATHWAYS_1 = [
            ("Low Right Atrium", 0),
            ("Inferior Vena Cava", 10)
        ]

        PATHWAYS_2 = [
            ("Right Ventricular Wall", 0),
            ("Pulmonary Artery", 10)
        ]

        self.pathway_1.trace('w', self.callback_pathway_1)
        self.pathway_2.trace('w', self.callback_pathway_2)

        Label(frame_pathway, text="Pathway Selection 1", font=self.header_2_style).pack(pady=5)

        for button_text, pathway_value in PATHWAYS_1:
            Radiobutton(frame_pathway, text=button_text, value=pathway_value, variable=self.pathway_1, font=self.default_style).pack()

        Label(frame_pathway, text="Pathway Selection 2", font=self.header_2_style).pack(pady=5)

        for button_text, pathway_value in PATHWAYS_2:
            Radiobutton(frame_pathway, text=button_text, value=pathway_value, variable=self.pathway_2, font=self.default_style).pack()

    def connect(self):
        self.client.set_hostname(self.host.get())
        self.client.start()

    def send_command(self):
        self.client.send_data(self.message.get())

    def send_customisations(self):
        self.client.send_data("update")
        self.client.send_data("{},{}".format(self.hr.get(), self.threshold.get()))

    def send_position(self):
        self.client.send_data("start-pos")
        self.client.send_data(self.position.get())

    def stop_position(self):
        self.client.send_data("stop-pos")

    def callback_pathway_1(self, *args):
        self.client.send_data("chpa1")
        self.client.send_data("%d" % self.pathway_1.get())

    def callback_pathway_2(self, *args):
        self.client.send_data("chpa2")
        self.client.send_data("%d" % self.pathway_2.get())
    
    def stop_gui(self):
        self.client.stop()
