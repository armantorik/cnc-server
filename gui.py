import os
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess as commands
import server
import multiprocessing





class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.server_running = False
        f1 = ttk.Frame(self)
        f2 = ttk.Frame(self)
        f3 = ttk.Frame(self)
        f4 = ttk.Frame(self)
        f5 = ttk.Frame(self)

        self.ip_address = get_ip_address()
        OWD = os.getcwd()

        ttk.Label(f1, text='Your IP address:  {}'.format(self.ip_address), font='Helvetica 10 bold').pack()
        ttk.Label(f2, text='Key logger period: (hours) ', font='Helvetica 10 bold').pack(side='left')

        ttk.Label(f3, text='Directory to save: ', font='Helvetica 10 bold').pack(side='left')
        self.path_entry = ttk.Entry(f3, width=70)
        self.path_entry.insert('end', OWD)
        self.path_entry.pack(side='left')
        ttk.Button(f3, text='Browse', command=self.browse).pack(side='left', padx=10)
        ttk.Label(f4, text='Start/Stop the server: ', font='Helvetica 10 bold').pack(side='left')
        self.start_btn = ttk.Button(f4, text='Start server', command=self.start_clicked)
        self.start_btn.pack(side='left', padx=10)
        self.stop_btn = ttk.Button(f4, text='Stop server', command=self.stop_clicked, state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        ttk.Label(f5, text='Server state: ', font='Helvetica 10 bold').pack(side='left')
        self.serverstate_lbl = ttk.Label(f5, text='Stopped', font='Helvetica 15 bold', foreground='red')
        self.serverstate_lbl.pack(side='left')

        f1.grid(column=1, row=1, padx=10, pady=10, sticky='w')
        f2.grid(column=1, row=2, padx=10, pady=10, sticky='w')
        f3.grid(column=1, row=3, columnspan=3, padx=10, pady=10, sticky='w')
        f4.grid(column=1, row=4, padx=10, pady=10, sticky='w')
        f5.grid(column=2, row=4, padx=10, pady=10, sticky='w')

    def browse(self):
        path = filedialog.askdirectory()
        if os.path.isdir(path):
            self.path_entry.delete('0', tk.END)
            self.path_entry.insert('end', path)

    def start_clicked(self):

        if switch_dir(self.path_entry.get()):
            self.proc = multiprocessing.Process(target=server.getHello()) #, args=(1,)
            self.proc.start()

            self.server_running = True
            self.toggle_state_widgets()
            messagebox.showinfo('NOW SERVING', 'Now serving {} @{}'.format(os.getcwd(), self.ip_address))
        else:
            messagebox.showerror('Invalid path', 'The path you have provided does not exist!')

    def stop_clicked(self, notify=True):
        if self.server_running:
            self.proc.terminate()  # sends a SIGTERM
            messagebox.showinfo('SERVER SHUTDOWN', 'The server has been shutdown.')

    def toggle_state_widgets(self):
        if self.server_running:
            self.start_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
            txt = 'Serving'
            color = 'green'
        else:
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            txt = 'Stopped'
            color = 'red'
        self.serverstate_lbl.configure(text=txt, foreground=color)


def get_ip_address():
    if os.name == 'posix':
        ip = commands.getoutput("hostname -I")
    elif os.name == 'nt':
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = ''
        print('Couldn\'t get local ip')
    return ip

def switch_dir(path):
    if os.path.isdir(path):
        os.chdir(path)
        return True
    if path == '':
        os.chdir(OWD)
        return True
    else:
        return

