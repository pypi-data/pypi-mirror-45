# -*- coding: utf-8 -*-
"""
@who: Niccolò Bonacchi (%(username)s)
@when: Created on %(date)s
@where: Mainen Lab - Champalimaud Neuroscience Programme, Lisbon, Portugal
@what: ...
@why: ...
@how:(code below!)
"""
# from pathlib import Path

# if __name__ == '__main__':
#     print(Path().cwd())
#     print(Path(__file__))
#     print(Path(__file__).parent.parent)

import tkinter as tk
from tkinter import simpledialog


def login():
    class MyDialog(simpledialog.Dialog):

        def body(self, master):

            tk.Label(master, text="Login:").grid(row=0)
            tk.Label(master, text="Password:").grid(row=1)

            self.e1 = tk.Entry(master)
            self.e2 = tk.Entry(master, show='*')

            self.e1.grid(row=0, column=1)
            self.e2.grid(row=1, column=1)
            return self.e1  # initial focus

        def apply(self):
            first = self.e1.get()
            second = self.e2.get()
            print(first, second)
            return (first, second)

    root = tk.Tk()
    root.withdraw()
    d = MyDialog(root)
    print(d.result)


if __name__ == "__main__":
    login()
    # login, passw, _ = [x.decode() for x in subprocess.check_output(['python', 'scratch/scratch.py']).split()]
