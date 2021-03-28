import file_handling
import tkinter as tk
from tkinter import messagebox

# Constants
BG = "black"
BOTTOM_BG = '#333333'
BTN_FONT = ('Technology', 20)
ENTRY_BG = 'grey'
LABEL_FONT = ('SquareFont', 20)
ENTRY_FONT = ('blank', 17)


class SaveWindow(tk.Tk):
    def __init__(self, path, password):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Save Password')
        tk.Tk.iconbitmap(self, default='images/key.ico')

        self.resizable(0, 0)
        self.config(bg=BOTTOM_BG)

        self.path = path
        self.password = password

        # data frame
        self.frame = DataFrame(self)
        self.frame.pack(side='top', fill='both', expand=True)

        # cancel button
        cancel_btn = tk.Button(self, text='Cancel',
                               command=lambda: self.close())
        cancel_btn.config(bg=ENTRY_BG,
                          font=BTN_FONT,
                          relief='raised',
                          borderwidth=4,
                          width=6)
        cancel_btn.pack(side='left')

        # save button
        save_btn = tk.Button(self, text='Save', command=lambda: self.save())
        save_btn.config(bg=ENTRY_BG,
                        font=BTN_FONT,
                        relief='raised',
                        borderwidth=4,
                        width=6)
        save_btn.pack(side='right')

    def save(self):
        website = self.frame.website_entry.get().strip()
        mail = self.frame.mail_entry.get().strip()
        username = self.frame.username_entry.get().strip()

        if website or mail or username:
            file_handling.save_password(self.path,
                                        self.password,
                                        website,
                                        mail,
                                        username)
            self.close()
        else:
            messagebox.showerror(
                "Saving Error",
                "You must enter at least one of the above options.")

    def close(self):
        self.destroy()


class DataFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.config(bg=BG)
        self.pack()
        self._widgets()

    def _widgets(self):
        # empty labels:
        for i in range(0, 7, 2):
            tk.Label(self, bg=BG).grid(row=i)

        # Website
        website_lab = tk.Label(self, text='Website', font=LABEL_FONT)
        website_lab.config(bg=BG, fg='#C9C6C6')
        website_lab.grid(row=1, column=0, padx=10, sticky='w')

        self.website_entry = tk.Entry(self)
        self.website_entry.config(font=ENTRY_FONT,
                                  bg=ENTRY_BG,
                                  justify='left',
                                  width=15)
        self.website_entry.grid(row=1, padx=10, column=1, sticky='nsew')

        # Mail
        mail_lab = tk.Label(self, text='Mail', font=LABEL_FONT)
        mail_lab.config(bg=BG, fg='#C9C6C6')
        mail_lab.grid(row=3, column=0, padx=10, sticky='w')

        self.mail_entry = tk.Entry(self)
        self.mail_entry.config(font=ENTRY_FONT,
                               bg=ENTRY_BG,
                               justify='left',
                               width=15)
        self.mail_entry.grid(row=3, padx=10, column=1, sticky='nsew')

        # Username
        username_lab = tk.Label(self, text='Username', font=LABEL_FONT)
        username_lab.config(bg=BG, fg='#C9C6C6')
        username_lab.grid(row=5, column=0, padx=10, sticky='w')

        self.username_entry = tk.Entry(self)
        self.username_entry.config(font=ENTRY_FONT,
                                   bg=ENTRY_BG,
                                   justify='left',
                                   width=15)
        self.username_entry.grid(row=5, padx=10, column=1, sticky='nsew')
