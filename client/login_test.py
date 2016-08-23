

"""
################################################################################
login module's test file
################################################################################
"""


import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox


from minghu6.gui import TkUtil

from minghu6.gui.TkUtil import Dialog

import getpass
import subprocess
from subprocess import call



PAD = "0.75m"

def start_gui():
        call('python3 client_tk.py',shell=True)

class Window(Dialog.Dialog):

    def __init__(self, master, result):
        self.result = result
        super().__init__(master, "User — Login",
                TkUtil.Dialog.OK_BUTTON|TkUtil.Dialog.CANCEL_BUTTON)


    def initialize(self):
        self.update_ui()


    def body(self, master):
        self.create_widgets(master)
        self.create_layout()
        self.create_bindings()
        return self.frame, self.usernameEntry


    def create_widgets(self, master):
        self.frame = ttk.Frame(master)
        self.usernameLabel = ttk.Label(self.frame, text="Account ID:",
                underline=-1 if TkUtil.mac() else 0)
        self.usernameEntry = ttk.Entry(self.frame, width=25)
        self.usernameEntry.insert(0,'b123456789123456789')
        self.passwordLabel = ttk.Label(self.frame, text="Password:",
                underline=-1 if TkUtil.mac() else 0)
        self.passwordEntry = ttk.Entry(self.frame, width=25, show="•")


    def create_layout(self):
        self.usernameLabel.grid(row=0, column=0, padx=PAD, pady=PAD)
        self.usernameEntry.grid(row=0, column=1, padx=PAD, pady=PAD)
        self.passwordLabel.grid(row=1, column=0, padx=PAD, pady=PAD)
        self.passwordEntry.grid(row=1, column=1, padx=PAD, pady=PAD)


    def validate(self):

        return self.usernameEntry.get() and self.passwordEntry.get()


    def create_bindings(self):
        if not TkUtil.mac():
            self.bind("<Alt-p>", lambda *args: self.passwordEntry.focus())
            self.bind("<Alt-u>", lambda *args: self.usernameEntry.focus())
        self.usernameEntry.bind("<KeyRelease>", self.update_ui)
        self.passwordEntry.bind("<KeyRelease>", self.update_ui)


    def update_ui(self, event=None):
        state = "!" + tk.DISABLED if self.validate() else tk.DISABLED
        self.acceptButton.state((state,))


    def apply(self):
        self.result.account_id = self.usernameEntry.get()
        self.result.passwd = self.passwordEntry.get()
        self.result.ok = True

        from login import Login
        login=Login(self.result.account_id,self.result.passwd)


