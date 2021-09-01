# Created by Jericho Loke
# This is an open-source program and can be modified accordingly to your needs.

from threading import Thread
import os, glob, webbrowser
import tkinter as tk
from tkinter import ttk, StringVar, filedialog, PhotoImage, Menu
from tkinter.filedialog import askdirectory, askopenfile, askopenfilename, asksaveasfile
from tkinter.ttk import Progressbar
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import keyboard

file_types = ('*.pdf', '*png', '*.jpg', '*.jpeg', '*.docx', '*.csv', '*.xlsx', '*.xml', '*.txt')


class Cryptor:
    # Create instance
    win = tk.Tk()
    win.resizable(False, False)
    # Add a title
    win.title("File Cryptor - By Jericho")
    win.geometry("540x300")
    win.iconbitmap('img\icon.ico')

    def __init__(self):  # Initializer method
        self.create_widgets()

    # ===============#
    #   Functions   #
    # ===============#

    # Create Thread
    def create_thread(self, target):
        # To pass argument to 'target', button has to use lambda for passing it
        self.run_thread = Thread(target=target)
        self.run_thread.start()

    # Ask file
    def file_selection(self):
        self.file_path = askopenfilename(title='Select file')
        self.file_folder_entry.set(self.file_path)

    # Ask directory
    def directory_selection(self):
        self.folder_path = askdirectory(title='Select folder/directory')  # shows dialog box and return the path
        self.file_folder_entry.set(self.folder_path)

    # Ask key
    def key_selection(self):
        self.key_file = askopenfile(mode='r', filetypes=[('Key Files', '*.key')],
                                    defaultextension=[('Key Files', '*.key')])
        cleanpath = str(self.key_file)
        path = cleanpath[25:-29]
        if self.key_file is not None:
            key_content = self.key_file.read().encode()
            self.encoded_key_content = Fernet(key_content)
            self.key_selection_entry.set(path)

    # Encrypt file
    def encrypt_file(self):
        global file_types, s
        files_array = []
        count = 0
        max_files = 0
        try:
            # Check if directory or file
            if os.path.isdir(self.file_folder_entry.get()):
                answer = askyesno(title='Confirm folder/directory encryption', message='Are you sure that you want to encrypt all files within specified folder/directory?')
                try:
                    if answer == True:
                        self.progress_bar1['value'] = 0
                        self.label3.configure(text="")
                        # Open each file in folder/directory
                        os.chdir(str(self.file_folder_entry.get()))
                        # Counting max files in directory
                        for item in file_types:
                            files_array.extend(glob.glob(item))
                        max_files = len(files_array)
                        selected_path = str(self.file_folder_entry.get()).replace("/", r'\\')
                        for file in files_array:
                            file_path = ("".join([selected_path, r'\\', files_array[count]]))
                            with open(file_path, "rb") as open_file:
                                file_data = open_file.read()
                                # Encrypt each opened file
                                encrypted_data = self.encoded_key_content.encrypt(file_data)
                                open_file.close()
                                # Write encrypted data into file
                                with open(file_path, "wb") as open_file:
                                    open_file.write(encrypted_data)
                                    open_file.close()
                            label = str("".join([self.file_folder_entry.get(), '/', files_array[count]]))
                            self.label3.configure(text='Encrypting: %s' %label)
                            count += 1
                            self.progress_bar1['value'] = (count / max_files) * 100
                        self.label3.configure(text="Encryption completed.")
                except:
                    tk.messagebox.showerror(title='Error', message='An error has occurred while trying to encrypt files in directory.')
            elif os.path.isfile(self.file_folder_entry.get()):
                try:
                    answer = askyesno(title='Confirm folder/directory encryption',
                                      message='Are you sure that you want to encrypt the specified file?')
                    if answer == True:
                        path = str(self.file_folder_entry.get()).replace("/", r'\\')
                        with open(path, "rb") as open_file:
                            file_data = open_file.read()
                            encrypted_data = self.encoded_key_content.encrypt(file_data)
                            open_file.close()
                            # Write encrypted data into file
                            with open(self.file_folder_entry.get(), "wb") as open_file:
                                open_file.write(encrypted_data)
                                open_file.close()
                                self.progress_bar1['value'] = 100
                                self.label3.configure(text='Encrypting: %s' % self.file_folder_entry.get())
                        self.label3.configure(text="Encryption completed.")
                except:
                    tk.messagebox.showerror(title='Error', message='An error has occurred while trying to encrypt specified file.')

        except:
            tk.messagebox.showerror(title='Error', message='File/folder path is invalid.')

    def decrypt_file(self):
        global file_types
        count = 0
        max_files = 0
        files_array = []
        # Check if directory or file
        try:
            if os.path.isdir(self.file_folder_entry.get()):
                answer = askyesno(title='Confirm folder/directory encryption', message='Are you sure that you want to decrypt all files within specified folder/directory?')
                try:
                    if answer == True:
                        self.progress_bar1['value'] = 0
                        self.label3.configure(text="")
                        # Open each file in folder/directory
                        os.chdir(str(self.file_folder_entry.get()))
                        for item in file_types:
                            files_array.extend(glob.glob(item))
                        max_files = len(files_array)
                        selected_path = str(self.file_folder_entry.get()).replace("/", r'\\')
                        for file in files_array:
                            file_path = ("".join([selected_path, r'\\', files_array[count]]))
                            with open(file_path, "rb") as open_file:
                                file_data = open_file.read()
                                # Decrypt each opened file
                                decrypted_data = self.encoded_key_content.decrypt(file_data)
                                open_file.close()
                                # Write decrypted data into file
                                with open(file_path, "wb") as open_file:
                                    open_file.write(decrypted_data)
                                    open_file.close()
                            label = str("".join([self.file_folder_entry.get(), '/', files_array[count]]))
                            self.label3.configure(text='Decrypting: %s' % label)
                            count += 1
                            self.progress_bar1['value'] = (count / max_files) * 100
                        self.label3.configure(text="Decryption completed.")
                except:
                    tk.messagebox.showerror(title='Error', message='An error has occurred while trying to decrypt files.')

            elif os.path.isfile(self.file_folder_entry.get()):
                answer = askyesno(title='Confirm folder/directory encryption',
                                  message='Are you sure that you want to encrypt the specified file?')
                try:
                    if answer == True:
                        path = str(self.file_folder_entry.get()).replace("/", r'\\')
                        with open(path, "rb") as open_file:
                            file_data = open_file.read()
                            decrypted_data = self.encoded_key_content.decrypt(file_data)
                            open_file.close()
                            # Write encrypted data into file
                            with open(self.file_folder_entry.get(), "wb") as open_file:
                                open_file.write(decrypted_data)
                                open_file.close()
                                self.progress_bar1['value'] = 100
                                self.label3.configure(text='Decrypting: %s' % self.file_folder_entry.get())
                        self.label3.configure(text="Decryption completed.")
                except:
                    tk.messagebox.showerror(title='Error', message='An error has occurred while trying to decrypt a file.')
        except:
            tk.messagebox.showerror(title='Error', message='An error has occurred while trying to decrypt a file.')

    def link1(self, event):
        webbrowser.open_new(event.widget.cget("text"))
    def link2(self, event):
        webbrowser.open_new(event.widget.cget("text"))

    def close(self):
        self.win.quit()
    # ===============#
    #    Widgets    #
    # ===============#
    def create_widgets(self):
        # ==============#
        #     Tabs     #
        # ==============#
        self.tabControl = ttk.Notebook(self.win)  # Creates Tab Control
        self.tabControl.pack(expand=1, fill='both')

        self.tab1 = ttk.Frame(self.tabControl)  # Creates first tab
        self.tabControl.add(self.tab1, text='Encryption/Decryption Panel')
        self.tab2 = ttk.Frame(self.tabControl)  # Creates second tab
        self.tabControl.add(self.tab2, text= 'Hotkeys List')
        self.tab3 = ttk.Frame(self.tabControl)  # Creates third tab
        self.tabControl.add(self.tab3, text='About')

        # Configurations for tab1 frame
        canvas1 = ttk.Labelframe(self.tab1, text=' File Cryptor - Encryption/Decryption Tab ')
        canvas1.grid(column=0, row=0, padx=0, pady=0)
        canvas1.pack(fill='both', expand='yes')
        # self.interface.place(x=0, y=0, width=1280, height=720)

        # Configuration for tab2 frame
        canvas2 = ttk.Labelframe(self.tab2, text=' File Cryptor - Hotkeys List ')
        canvas2.grid(column=0, row=0, padx=0, pady=0)
        canvas2.pack(fill='both', expand='yes')

        # Configuration for tab3 frame
        canvas3 = ttk.Labelframe(self.tab3, text=' File Cryptor - About ')
        canvas3.grid(column=0, row=0, padx=0, pady=0)
        canvas3.pack(fill='both', expand='yes')

        # ============#
        #   Labels   #
        # ============#
        # File/folder label
        label1 = ttk.Label(canvas1, text="File/Folder:", background='', font=("Arial", '15'))
        label1.place(x=5, y=5)

        # Key Selection label
        label2 = ttk.Label(canvas1, text="Encryption Key:", background='', font=("Arial", '15'))
        label2.place(x=5, y=70)

        # File being encrypted/decrypted
        self.label3 = ttk.Label(canvas1, text="", background='', font=("Arial", '9'))
        self.label3.place(x=5, y=175)

        # Labels for hotkeys
        hotkeys_list_label = ttk.Label(canvas2, text="Open a File:\t\tCtrl + O\nOpen a directory/folder\tCtrl + Shift + O\nSelect a key\t\tCtrl + K\nEncrypt file/directory\t\tCtrl + E\nDecrypt file/directory\t\tCtrl + D\nClose application\t\tCtrl + Q", font=("Arial", '12'))
        hotkeys_list_label.place(x=5, y=5)

        # Labels for About
        about_label1 = ttk.Label(canvas3, text="This application is developed by Jericho Loke.\n\nThe purpose for this application is to eliminate the usage of \npassword-protected files/folders thorugh the use of symmetric encryption.\n\nA unique key is generated and provided to client for encryption/decryption \npurposes.", background='', font=("Arial", '12'))
        about_label1.place(x=5, y=5)
        about_label2 = ttk.Label(canvas3, text="Links to all other open-source resources used within this application:", background='', font=("Arial", '12'))
        about_label2.place(x=5, y=145)
        about_label3 = ttk.Label(canvas3, text="https://github.com/Jericho-Technology/File-Cryptor-client-", foreground='blue', font=("Arial", '10'), cursor="hand2")
        about_label3.place(x=180, y=170)
        about_label3.bind("<Button-1>", self.link1)
        about_label4 = ttk.Label(canvas3, text="https://icons8.com", foreground='blue', font=("Arial", '10'), cursor="hand2")
        about_label4.place(x=180, y=202)
        about_label4.bind("<Button-1>", self.link2)
        about_label_desc = ttk.Label(canvas3, text="Official Github Repository:\n\nIcon images by Icons8:", font=("Arial", '10'))
        about_label_desc.place(x=25, y=170)

        # =============#
        #   Entries   #
        # =============#
        # File/folder
        self.file_folder_entry = tk.StringVar()
        self.input_bar = ttk.Entry(canvas1, width=75, textvariable=self.file_folder_entry)
        self.input_bar.place(x=5, y=40)

        # Key Selection
        self.key_selection_entry = tk.StringVar()
        self.key_selection_bar = ttk.Entry(canvas1, width=75, textvariable=self.key_selection_entry)
        self.key_selection_bar.place(x=5, y=105)

        #===========#
        #  Buttons  #
        #===========#
        # Importing images for buttons
        self.image_btn = ImageTk.PhotoImage(Image.open(r'img\folder_icon.png'))
        self.enc_key_image = ImageTk.PhotoImage(Image.open('img\key-64.png'))
        self.file_image = ImageTk.PhotoImage(Image.open(r'img\file-48.png'))

        # Create image button for folder
        self.folder_button = tk.Button(canvas1, image=self.image_btn,
                                       command=lambda: self.create_thread(self.directory_selection), height=15,
                                       width=15)
        self.folder_button.place(x=470, y=40)

        # Create image button for file selection
        self.file_btn = tk.Button(canvas1, image=self.file_image,
                                  command=lambda: self.create_thread(self.file_selection), height=15, width=15)
        self.file_btn.place(x=500, y=40)

        # Create image button for key selection
        self.encryption_key_button = tk.Button(canvas1, image=self.enc_key_image, command=lambda: self.create_thread(self.key_selection), height=15, width=15)
        self.encryption_key_button.place(x=470, y=105)

        # Create encrypt file button
        self.encrypt_file_btn = tk.Button(canvas1, text='Encrypt File(s)', command=lambda: self.create_thread(self.encrypt_file), height=2, width=25)
        self.encrypt_file_btn.place(x=5, y=200)

        # Create decrypt file button
        self.decrypt_file_btn = tk.Button(canvas1, text='Decrypt File(s)', command=lambda: self.create_thread(self.decrypt_file), height=2, width=25)
        self.decrypt_file_btn.place(x=200, y=200)

        # Create Exit Button
        self.exit_btn = tk.Button(canvas1, text='Close', command=lambda: self.create_thread(self.close), height=2, width=17)
        self.exit_btn.place(x=395, y=200)

        #==================#
        #   Progress Bar   #
        #==================#
        self.progress_bar1 = Progressbar(canvas1, orient='horizontal', length=455, mode='determinate')
        self.progress_bar1.place(x=5, y=150)

        #=================#
        #     Hotkeys     #
        #=================#

        keyboard.add_hotkey('ctrl + o', self.file_selection)
        keyboard.add_hotkey('ctrl + shift + o', self.directory_selection)
        keyboard.add_hotkey('ctrl + k', self.key_selection)
        keyboard.add_hotkey('ctrl + e', self.encrypt_file)
        keyboard.add_hotkey('ctrl + d', self.decrypt_file)
        keyboard.add_hotkey('ctrl + q', self.close)

# ======================= #
#        Start GUI        #
# ======================= #
Crypt = Cryptor()
Crypt.win.mainloop()
