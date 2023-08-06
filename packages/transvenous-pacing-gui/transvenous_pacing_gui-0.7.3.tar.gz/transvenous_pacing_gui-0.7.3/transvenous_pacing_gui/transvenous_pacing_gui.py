import tkinter as tk
from tkinter import ttk

from guiclient import InstructorGUI
from guiserver import StudentGUI

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # GUI design
        notebook = ttk.Notebook(self.parent)

        # Student GUI design
        self.student_gui = StudentGUI(notebook)
        self.student_gui.configure(bg="black")

        # Teacher GUI design
        self.instructor_gui = InstructorGUI(notebook)
        self.instructor_gui.configure(bg="black")

        # Building the notebook
        notebook.add(self.student_gui, text="Student")
        notebook.add(self.instructor_gui, text="Instructor")
        notebook.pack()

    def stop_gui(self):
        self.instructor_gui.stop_gui()
        self.student_gui.stop_gui()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tranvenous Pacing GUI")

    main_app = MainApplication(root)
    main_app.pack(side="top", fill="both", expand=True)

    root.mainloop()

    main_app.stop_gui()