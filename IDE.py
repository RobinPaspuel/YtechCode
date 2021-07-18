from tkinter import *
from tkinter import ttk
import tkinter
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import YTechCode_interpreter
import subprocess
from datetime import datetime
import os



########## GLOBAL VARIABLES ##########

file_path = ''
########## GUI CONFIGS ##############
ide = ThemedTk(theme="breeze")
ide.title("YTech Code IDE")
ide.geometry("1200x720")

############ Line Numbers #################

############ Functions #####################
def run():
    if file_path == '':
        messagebox.showwarning("Save File", "The file must be saved before executing it!")
    else:
        code_output.config(state=NORMAL)
        now = datetime.now()
        now_time = datetime.now().time()
        command = f"python3 -c 'import sys, run_ide; run_ide.run_ide(sys.argv[1])' '{file_path}'"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.insert(END, output)
        code_output.insert(END, error)
        code_output.insert(END, f'---------------YTech Code---------------({now.year}-{now.month}-{now.day}|{now_time.hour}:{now_time.minute}:{now_time.second})\n')
        code_output.see(END)
        code_output.config(state=DISABLED)
        code_output.bind("<1>", lambda event: code_output.focus_set())


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('YTech Code Files', '*.ytc')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def open_file():
    path = askopenfilename(filetypes=[('YTech Code Files', '*.ytc')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

def set_file_path(path):
    global file_path
    file_path = path


def from_rgb(rgb):
    r, g, b  = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def line_number(event):
    line, column = editor.index('insert').split('.')
    line = int(line)
    if line >= 1:
        linenumbers.config(state = NORMAL)
        linenumbers.insert(END, f'\n{line+1}')
        linenumbers.config(state = DISABLED)
    global lines
    lines = line+1
    
def delete_number(event):
    global lines
    line, column = editor.index('insert').split('.')
    line = int(line)
    line_count = (linenumbers.get("end-3c linestart", "end-3c lineend"))
    print(str(line_count))
    print(str(line) + "-" + str(line_count))
    #print(line)
    if  line < lines and lines > 10:
        linenumbers.config(state = NORMAL)
        linenumbers.delete("end-3c linestart", END)
        linenumbers.update()
        linenumbers.config(state = DISABLED)
        lines = lines-1
    elif line < int(line_count):
        linenumbers.config(state = NORMAL)
        linenumbers.delete("end-3c linestart", END)
        linenumbers.update()
        linenumbers.config(state = DISABLED)
    #print(line_count)

def line_one(event):
    linenumbers.config(state  = NORMAL)
    linenumbers.insert(END, "1")
    linenumbers.config(state = DISABLED)

       

################# GUI ####################

## Main Frame
main_frame = LabelFrame(ide, text = "CODE")
main_frame.grid(row=0, column=2)

output_frame = LabelFrame(ide, text = "OUTPUT")
output_frame.grid(row=1, column=2)
## Shell Frame
shell_frame = LabelFrame(ide, bg = "green", text = "test")
shell_frame.grid(row=0, column=0, rowspan=2)

## Text Scroll
text_scroll = Scrollbar(main_frame)
#text_scroll.grid(row=0, column=1)
#text_scroll.pack(side=RIGHT, fill=Y)

output_scroll = Scrollbar(output_frame)
#text_scroll.grid(row=1, column=1, sticky=NS)
#output_scroll.pack(side=RIGHT, fill=Y)

#Setting Text Editor

editor = Text(main_frame, width=97, height=24, font=("Consolas", 11), selectbackground="lightblue", insertbackground=from_rgb((255, 205, 56)), background=from_rgb((22, 51, 72)),fg = "white", undo=True, yscrollcommand=text_scroll.set)
editor.grid(row=0, column=1)

linenumbers = Text(main_frame, width=2)
linenumbers.config(font=("Consolas", 11))
linenumbers.tag_configure('line', justify='right')
editor.bind("<Visibility>", line_one)
editor.bind("<Return>", line_number)
editor.bind("<BackSpace>", delete_number)
linenumbers.grid(row=0, column=0, sticky=NS)



code_output = Text(output_frame, width=100, height=13, font=("Consolas", 11), selectbackground="lightblue", selectforeground="black", background=from_rgb((16, 37, 55)),fg = "white", yscrollcommand=output_scroll.set)
code_output.grid()

test = Text(shell_frame, width=20, height=40, font=("Helvetica", 12), selectbackground="lightblue", selectforeground="black")
test.grid()

#Configure scrollbar
text_scroll.config(command = editor.yview)
output_scroll.config(command = code_output.yview)

menu_bar = Menu(ide)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label = "Open", command=open_file)
file_menu.add_command(label = "Save", command=save_as)
file_menu.add_command(label = "Save as", command=save_as)
file_menu.add_command(label = "Exit", command=exit)
menu_bar.add_cascade(label = "File", menu=file_menu)

run_button = Menu(menu_bar, tearoff=0)
run_button.add_command(label = "Run", command=run)
menu_bar.add_cascade(label = "Run", menu=run_button)


############# MAIM LOOP ###############

ide.config(menu = menu_bar)

ide.mainloop()