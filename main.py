import encryption
import os
import subprocess
import styles
import string_functions
import save_window
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# screen dimensions
WIDTH = 600
HEIGHT = 600


class PasswordEncryptor(tk.Tk):
    '''
    mode:       encrypt or decrypt
    input:      txt to encrypt or decrypt
    output:     encrypted or decrypted text
    '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Encryptor App')
        tk.Tk.iconbitmap(self, default='images/key.ico')
        self.resizable(0, 0)
        self.geometry(f"{WIDTH}x{HEIGHT}")

        # container
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # app variables
        self.mode = 'encrypt'
        self.output = 'None'
        self.storage_file = None

        # app pages
        self.frames = {}

        for f in (EncryptorPage, ResultsPage):
            frame = f(container, self)

            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(EncryptorPage)

    def show_frame(self, cont):
        # cont = controler
        frame = self.frames[cont]

        if isinstance(frame, ResultsPage):
            frame._widgets()
            frame._show_output()

        frame.tkraise()

    def close(self):
        self.destroy()


class EncryptorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # frame configuration
        self.grid_propagate(0)
        self.config(bg=styles.APP_BACKGROUND)
        self.grid_columnconfigure((0, 2), weight=1)
        self.columnconfigure((0, 2), uniform='entrycol')
        self.title = 'ENCRYPTOR'
        # variables
        self.text = tk.StringVar()
        self.password = tk.StringVar()
        self.pin = tk.StringVar()

        self.encryptor = encryption.Encryptor()
        self.controller = controller
        self.show_input = True
        self._widgets()

    def _widgets(self):
        # empty labels
        for i in range(15):
            tk.Label(self, bg=styles.APP_BACKGROUND, width=10,
                     height=2).grid(row=i, column=1)

        #### Title ####

        title_label = tk.Label(self, text=self.title, font=styles.LARGE_FONT)
        title_label.config(bg=styles.APP_BACKGROUND,
                           fg=styles.LABEL_TEXT,
                           relief="groove",
                           highlightbackground='#69F3E5',
                           borderwidth=10, pady=15)
        title_label.place(x=0, y=0, relwidth=1)

        #### Password & PIN ####
        # password
        password_title = tk.Label(
            self, text='Password', font=styles.MEDIUM_FONT)
        password_title.config(bg=styles.APP_BACKGROUND,
                              fg=styles.LABEL_TEXT,
                              relief='groove',
                              bd=4, height=1)
        password_title.grid(row=4, column=0,
                            padx=styles.SPACING,
                            sticky='nsew')

        pass_entry = tk.Entry(self, textvariable=self.password)
        pass_entry.config(font=styles.TEXT_FONT,
                          bg=styles.ENTRY_BACKGROUND,
                          justify='center',
                          width=15)
        pass_entry.grid(row=5, column=0, padx=styles.SPACING, sticky='nsew')

        # pin
        pin_title = tk.Label(self, text='PIN', font=styles.MEDIUM_FONT)
        pin_title.config(bg=styles.APP_BACKGROUND,
                         fg=styles.LABEL_TEXT,
                         relief='groove',
                         bd=4, height=1)
        pin_title.grid(row=4, column=2, padx=styles.SPACING, sticky='nsew')

        pin_entry = tk.Entry(self, textvariable=self.pin)
        pin_entry.config(font=styles.NUMBERS_FONT,
                         bg=styles.ENTRY_BACKGROUND,
                         justify='right',
                         width=15)
        pin_entry.grid(row=5, column=2, padx=styles.SPACING, sticky='nsew')

        #### Input ####

        input_title = tk.Label(self, text='Input', font=styles.MEDIUM_FONT)
        input_title.config(bg=styles.APP_BACKGROUND,
                           fg=styles.LABEL_TEXT,
                           relief='groove',
                           bd=4, height=1)
        input_title.grid(row=8, column=0,
                         padx=styles.SPACING,
                         sticky='nswe',
                         columnspan=3)

        self.input_entry = tk.Entry(self, textvariable=self.text)
        self.input_entry.config(font=styles.TEXT_FONT,
                                bg=styles.ENTRY_BACKGROUND,
                                justify='center')
        self.input_entry.grid(row=9, column=0,
                              padx=styles.SPACING,
                              sticky='nsew',
                              columnspan=3)

        clear_btn = tk.Button(
            self, text="Clear", command=lambda: self._clear_input())
        clear_btn.config(font=styles.SHORT_BTN_FONT,
                         fg=styles.BTN_TEXT,
                         relief='raised',
                         bg=styles.SHORT_BTN_BG,
                         width=styles.SHORT_BTN_WIDTH)
        clear_btn.grid(row=10, column=0,
                       padx=styles.BTN_SPACING,
                       pady=styles.SHORT_BTN_SPACING,
                       sticky='w')

        hide_btn = tk.Button(
            self, text="Hide", command=lambda: self._hide())
        hide_btn.config(font=styles.SHORT_BTN_FONT,
                        fg=styles.BTN_TEXT,
                        relief='raised',
                        bg=styles.SHORT_BTN_BG,
                        width=styles.SHORT_BTN_WIDTH)
        hide_btn.grid(row=10, column=2,
                      padx=styles.BTN_SPACING,
                      pady=styles.SHORT_BTN_SPACING,
                      sticky='e')

        #### Encrypt & Decrypt Button ####

        encrypt_btn = tk.Button(
            self, text="Encrypt", command=lambda: self._set_up('encrypt'))

        encrypt_btn.config(font=styles.BTN_FONT,
                           width=styles.BTN_WIDTH,
                           fg=styles.BTN_TEXT,
                           relief=styles.BTN_BORDER,
                           borderwidth=styles.BTN_BORDER_WIDTH,
                           bg=styles.BTN_BG)

        encrypt_btn.grid(row=12, column=0,
                         padx=styles.BTN_SPACING,
                         pady=18,
                         sticky='w')

        decrypt_btn = tk.Button(
            self, text="Decrypt", command=lambda: self._set_up('decrypt'))

        decrypt_btn.config(font=styles.BTN_FONT,
                           width=styles.BTN_WIDTH,
                           fg=styles.BTN_TEXT,
                           relief=styles.BTN_BORDER,
                           borderwidth=styles.BTN_BORDER_WIDTH,
                           bg=styles.BTN_BG)

        decrypt_btn.grid(row=12, column=2,
                         padx=styles.BTN_SPACING,
                         pady=18,
                         sticky='e')

    def _clear_input(self):
        self.input_entry.delete(0, 'end')

    def _hide(self):
        if self.show_input:
            self.input_entry.config(show=styles.HIDE_CHAR)
            self.show_input = False
        else:
            self.input_entry.config(show='')
            self.show_input = True

    def _set_up(self, mode):

        if not self._exceptions():
            txt = self.text.get().strip()
            self.encryptor.password = self.password.get()
            self.encryptor.pin = self.pin.get()

            # encrypting
            if mode == 'encrypt':
                output = self._encrypt(txt)

            # decrypting
            else:
                output = self._decrypt(txt)

            if output is not None:
                self.controller.mode = mode
                self.controller.output = output
                self.controller.show_frame(ResultsPage)

    def _encrypt(self, txt):
        return styles.ENC_SEPARATOR.join(self.encryptor.encrypt(txt))

    def _decrypt(self, txt):
        try:
            encrypted_list = txt.split(sep=styles.ENC_SEPARATOR)
            return self.encryptor.decrypt(encrypted_list)
        except Exception:
            messagebox.showerror(
                "Decrypting Error",
                "Invalid Password, PIN or Input.")
            return None

    def _exceptions(self):
        if len(self.password.get()) < 8:
            messagebox.showerror(
                "Invalid Password",
                "Password must have at least 8 characters.")
            return True

        if not string_functions.is_password(self.password.get()):
            messagebox.showerror(
                "Invalid Password",
                "Password must have at least one special character, one capital & lowercase letter and one number.")
            return True

        if not self.pin.get().isnumeric() or len(str(self.pin.get())) < 4:
            messagebox.showerror(
                "Invalid PIN",
                "PIN must only contain numbers and cannot have less than 4 digits.")
            return True

        if len(self.text.get()) == 0:
            messagebox.showerror(
                "Invalid Input",
                "Must specify input text before Encrypting/Decrypting.")
            return True

        return False


class ResultsPage(tk.Frame):

    indentation = 2

    def __init__(self, parent, controller):
        '''
        parent = App class
        '''
        tk.Frame.__init__(self, parent)

        # frame configuration
        self.grid_propagate(0)
        self.config(bg=styles.APP_BACKGROUND)
        self.grid_columnconfigure((0, 0), weight=1)
        self.columnconfigure((0, 2), uniform='entrycol')

        # other attributes
        self.controller = controller
        self.show_output = True

        self._widgets()

    @ property
    def title(self):
        if self.controller.mode == 'encrypt':
            return 'ENCRYPTED RESULT'

        elif self.controller.mode == 'decrypt':
            return 'DECRYPTED RESULT'

    def _widgets(self):
        # empty labels
        for i in range(15):
            if i <= 3:
                tk.Label(self, bg=styles.APP_BACKGROUND, width=10,
                         height=2).grid(row=i, column=1)
            else:
                tk.Label(self, bg=styles.APP_BACKGROUND, width=10,
                         height=1).grid(row=i, column=1)

        #### Title ####
        title = tk.Label(self, text=self.title, font=styles.LARGE_FONT)
        title.config(bg=styles.APP_BACKGROUND, fg=styles.LABEL_TEXT, relief="groove",
                     borderwidth=10, pady=15, highlightbackground='#69F3E5')
        title.place(x=0, y=0, relwidth=1)

        #### Output ####
        output_title = tk.Label(self, text='Output')
        output_title.config(bg=styles.APP_BACKGROUND,
                            font=styles.MEDIUM_FONT,
                            fg=styles.LABEL_TEXT,
                            relief='groove',
                            bd=4, height=1)
        output_title.grid(row=4, column=0,
                          padx=styles.SPACING,
                          sticky='nswe',
                          columnspan=3)

        self.output_textbox = tk.Text(self, state="disabled")
        self.output_textbox.config(font=styles.NUMBERS_FONT,
                                   bg=styles.ENTRY_BACKGROUND,
                                   fg=styles.ENTRY_FG,
                                   width=50, height=1)  # 10F700
        self.output_textbox.grid(row=5, column=0,
                                 padx=styles.SPACING,
                                 sticky='nsew',
                                 columnspan=3)

        copy_btn = tk.Button(
            self, text="Copy", command=lambda: self._copy())
        copy_btn.config(font=styles.SHORT_BTN_FONT,
                        fg=styles.BTN_TEXT,
                        relief='raised',
                        bg=styles.SHORT_BTN_BG,
                        width=styles.SHORT_BTN_WIDTH)
        copy_btn.grid(row=6, column=0,
                      padx=styles.BTN_SPACING,
                      pady=styles.SHORT_BTN_SPACING,
                      sticky='w')

        hide_btn = tk.Button(
            self, text="Hide", command=lambda: self._hide())
        hide_btn.config(font=styles.SHORT_BTN_FONT,
                        fg=styles.BTN_TEXT,
                        relief='raised',
                        bg=styles.SHORT_BTN_BG,
                        width=styles.SHORT_BTN_WIDTH)
        hide_btn.grid(row=6, column=2,
                      padx=styles.BTN_SPACING,
                      pady=styles.SHORT_BTN_SPACING,
                      sticky='e')

        #### Select File ####
        select_title = tk.Label(self, text='Save Output in File')
        select_title.config(bg=styles.APP_BACKGROUND,
                            font=styles.MEDIUM_FONT,
                            fg=styles.LABEL_TEXT,
                            relief='groove',
                            bd=4, height=1)
        select_title.grid(row=8, column=0,
                          padx=styles.SPACING,
                          sticky='nswe',
                          columnspan=3)

        self.select_file = tk.Text(self, state="disabled")
        self.select_file.config(font=styles.SHORT_TEXT_FONT,
                                bg=styles.ENTRY_BACKGROUND,
                                fg=styles.ENTRY_FG,
                                width=50, height=1)
        self.select_file.grid(row=9, column=0,
                              padx=styles.SPACING,
                              sticky='nsew',
                              columnspan=3)

        #### File Selector Buttons ####
        select_btn = tk.Button(
            self, text="Select File", command=lambda: self._select_file())
        select_btn.config(font=styles.SHORT_BTN_FONT,
                          fg=styles.BTN_TEXT,
                          relief='raised',
                          bg=styles.SHORT_BTN_BG,
                          width=styles.SHORT_BTN_WIDTH)
        select_btn.grid(row=10, column=0,
                        padx=styles.BTN_SPACING,
                        pady=styles.SHORT_BTN_SPACING,
                        sticky='w')

        save_btn = tk.Button(
            self, text="Save Output", command=lambda: self._save_output())
        save_btn.config(font=styles.SHORT_BTN_FONT,
                        fg=styles.BTN_TEXT,
                        relief='raised',
                        bg=styles.SHORT_BTN_BG,
                        width=styles.SHORT_BTN_WIDTH)
        save_btn.grid(row=10, column=2,
                      padx=styles.BTN_SPACING,
                      pady=styles.SHORT_BTN_SPACING,
                      sticky='e')

        #### Encryptor & Exit Button ####
        back_btn = tk.Button(
            self, text="Back", command=lambda: self.controller.show_frame(EncryptorPage))

        back_btn.config(font=styles.BTN_FONT,
                        fg=styles.BTN_TEXT,
                        relief=styles.BTN_BORDER,
                        borderwidth=styles.BTN_BORDER_WIDTH,
                        bg=styles.BTN_BG,
                        width=styles.BTN_WIDTH)
        back_btn.grid(row=13, column=0,
                      padx=styles.BTN_SPACING,
                      sticky='w')

        exit_btn = tk.Button(
            self, text="Exit", command=lambda: self.controller.close())

        exit_btn.config(font=styles.BTN_FONT,
                        fg=styles.BTN_TEXT,
                        relief=styles.BTN_BORDER,
                        borderwidth=styles.BTN_BORDER_WIDTH,
                        bg=styles.BTN_BG,
                        width=styles.BTN_WIDTH)

        exit_btn.grid(row=13, column=2,
                      padx=styles.BTN_SPACING,
                      sticky='e')

    def _hide(self):
        if self.show_output:
            self.show_output = False
            self._hide_output()
        else:
            self.show_output = True
            self._show_output()

    def _show_output(self):
        # clear textbox
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete('1.0', 'end-1c')

        # set output
        self.output_textbox.insert(tk.INSERT, self.controller.output)
        self.output_textbox.configure(state="disabled")

    def _hide_output(self):
        # hide input in textbox
        hidden_output = string_functions.hide(
            self.output_textbox.get("1.0", tk.END),
            styles.HIDE_CHAR,
            styles.ENC_SEPARATOR)

        # show hidden text
        self.output_textbox.configure(state='normal')
        self.output_textbox.delete('1.0', 'end-1c')
        self.output_textbox.insert(tk.INSERT, hidden_output)
        self.output_textbox.configure(state='disabled')

    def _select_file(self):
        path = filedialog.askopenfilename(
            title='Select a file:',
            filetypes=(('text files', 'txt'),))

        if path != '':
            indented_path = string_functions.indent(path, self.indentation)
            self.select_file.configure(state="normal")
            self.select_file.delete('1.0', 'end-1c')
            self.select_file.insert(tk.INSERT, indented_path)
            self.select_file.configure(state="disabled")

    def _save_output(self):
        path = self.select_file.get("1.0", "end-1c").strip()

        if os.path.exists(path):
            root = save_window.SaveWindow(path, self.controller.output)
            root.mainloop()

        else:
            if not path:
                messagebox.showerror(
                    "Invalid File",
                    "You must select a file first")
            else:
                messagebox.showerror(
                    "Invalid File",
                    "Selected file does not exist.")

    def _copy(self):
        cmd = 'echo {}|clip'.format(self.controller.output)
        return subprocess.check_call(cmd, shell=True)


encryptor_app = PasswordEncryptor()
encryptor_app.mainloop()
