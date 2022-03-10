from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
from datetime import datetime
from sys import platform as _platform


########## GLOBAL VARIABLES ##########

file_path = ''
########## GUI CONFIGS ##############
#ide = Tk()
style = Style("superhero")
ide = style.master
#ide = ThemedTk(theme="breeze")
ide.title("YTech Code IDE")
ide.geometry("1200x720")


############ Line Numbers #################

############ Functions #####################
def run():
    if file_path == '':
        messagebox.showwarning(
            "Save File", "The file must be saved before executing it!")
    else:
        code_output.config(state=NORMAL)
        now = datetime.now()
        now_time = datetime.now().time()
        command = f"python3 -c 'import sys, run_ide; run_ide.run_ide(sys.argv[1])' '{file_path}'"
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.insert(END, output)
        code_output.insert(END, error)
        code_output.insert(END, (35*"-") + "Tech Code" + (35*"-") +
                           f'({now.year}-{now.month}-{now.day}|{now_time.hour}:{now_time.minute}:{now_time.second})\n')
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
    lines = 1
    line_count, column = editor.index('insert').split('.')
    line_count = int(line_count)
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
        for line in code:
            if line == '\n':
                lines += 1
                linenumbers.config(state=NORMAL)
                linenumbers.insert(END, f'\n{lines}')
                linenumbers.config(state=DISABLED)


def set_file_path(path):
    global file_path
    file_path = path


def shell_Test():
    subprocess.call(['gnome-terminal', '-e',
                    '/bin/bash -c "cd ~/YtechCode; python3 YTechShell.py" '])


def from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def line_number(event):
    line, column = editor.index('insert').split('.')
    line = int(line)
    if line >= 1:
        if line < 10:
            if int(linenumbers.get("end-2c linestart", "end-2c lineend")) != (line+1):
                linenumbers.config(state=NORMAL)
                linenumbers.insert(END, f'{line+1}\n')
                linenumbers.config(state=DISABLED)
            else:
                pass
        elif line >= 10:
            if int(linenumbers.get("end-2c linestart", "end-2c lineend")) != (line+1):
                linenumbers.config(state=NORMAL)
                linenumbers.insert(END, f'{line+1}\n')
                linenumbers.config(state=DISABLED)


def delete_number(event):
    count = 0
    text = editor.get("1.0", END)
    text = list(text)
    linenumbers.config(state=NORMAL)
    linenumbers.delete("1.0", END)
    for element in text:
        if element == "\n":
            count += 1
            linenumbers.insert(END, f"{count}\n")
    linenumbers.config(state=DISABLED)


def line_one(event):
    linenumbers.config(state=NORMAL)
    linenumbers.insert(END, "1\n")
    linenumbers.config(state=DISABLED)


def number_lines_for_paste(event):
    clipboard = ide.clipboard_get()
    lines = 0
    line_count, column = editor.index('insert').split('.')
    line_count = int(line_count)
    for line in clipboard:
        if line_count:
            if line_count < 10:
                insert_number = int(linenumbers.get(
                    "end-2c linestart", "end-2c lineend"))
                if line == '\n':
                    insert_number += 1
                    linenumbers.config(state=NORMAL)
                    linenumbers.insert(END, f'\n{insert_number}')
                    linenumbers.config(state=DISABLED)
            else:
                insert_number = int(linenumbers.get(
                    "end-3c linestart", "end-3c lineend")) + lines
                if line == '\n':
                    insert_number += 1
                    linenumbers.config(state=NORMAL)
                    linenumbers.insert(END, f'\n{insert_number}')
                    linenumbers.config(state=DISABLED)
        else:
            if line == '\n':
                lines += 1
                linenumbers.config(state=NORMAL)
                linenumbers.insert(END, f'\n{lines}')
                linenumbers.config(state=DISABLED)


def scroll_code_and_lines(*args):
    editor.yview(*args)
    linenumbers.yview(*args)


def scroll_windows(event):
    main_frame.yview_scroll(-1*event.delta/120, "units")


def scroll_linux(event):
    def delta(event):
        if event.num == 5:
            return -1
        return 1
    linenumbers.yview_scroll(delta(event)*-1, "units")
    editor.yview_scroll(delta(event), "units")
################# GUI ####################


# Main Frame
main_frame = ttk.Frame(ide)
main_frame.grid(row=0, column=2)

output_frame = ttk.Frame(ide)
output_frame.grid(row=1, column=2)
# Shell Frame
shell_frame = ttk.Frame(ide)
shell_frame.grid(row=0, column=0, rowspan=2)

# Text Scroll
text_scroll = ttk.Scrollbar(main_frame)
#text_scroll.grid(row=0, column=1)
text_scroll.pack(side=RIGHT, fill=Y)

output_scroll = ttk.Scrollbar(output_frame)
#text_scroll.grid(row=1, column=1, sticky=NS)
output_scroll.pack(side=RIGHT, fill=Y)

# Setting Text Editor

editor = Text(main_frame, width=96, height=24, font=("Consolas", 11), bd=0, selectbackground=from_rgb((0, 62, 135)), insertbackground=from_rgb(
    (255, 205, 56)), background=from_rgb((22, 51, 72)), fg="white", undo=True, yscrollcommand=text_scroll.set)
#editor.grid(row=0, column=1)
editor.pack(side=RIGHT, fill=Y)

linenumbers = Text(main_frame, width=3, font=("Consolas", 11), background=from_rgb(
    (15, 47, 64)), fg=from_rgb((147, 152, 154)), bd=0, yscrollcommand=text_scroll.set)
linenumbers.tag_configure('line', justify='right')
editor.bind("<Visibility>", line_one)
editor.bind("<Return>", line_number)
editor.bind("<BackSpace>", delete_number)
editor.bind("<Control-v>", number_lines_for_paste)
editor.bind("<Control-z>", delete_number)
# Mouse wheel
if _platform.startswith('linux'):
    editor.bind("<Button-4>", scroll_linux)
    editor.bind("<Button-5>", scroll_linux)
    linenumbers.bind("<Button-4>", scroll_linux)
    linenumbers.bind("<Button-5>", scroll_linux)
else:
    editor.bind("<MouseWheel>", scroll_windows)
    linenumbers.bind("<MouseWheel>", scroll_windows)


linenumbers.pack(side=LEFT, fill=Y)
#linenumbers.grid(row=0, column=0, sticky=NS)


code_output = Text(output_frame, width=100, height=13, font=("Consolas", 11), selectbackground="lightblue",
                   selectforeground="black", background=from_rgb((16, 37, 55)), fg="white", yscrollcommand=output_scroll.set)
# code_output.grid()
code_output.pack()

test = Text(shell_frame, width=20, height=40, font=("Helvetica", 12),
            selectbackground="lightblue", selectforeground="black")
test.pack()

# Configure scrollbar
text_scroll.config(command=scroll_code_and_lines)
output_scroll.config(command=code_output.yview)

menu_bar = Menu(ide)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_as)
file_menu.add_command(label="Save as", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit)
menu_bar.add_cascade(label="File", menu=file_menu)

run_button = Menu(menu_bar, tearoff=0)
run_button.add_command(label="Run", command=run)
menu_bar.add_cascade(label="Run", menu=run_button)

shell = Menu(menu_bar, tearoff=0)
shell.add_command(label="Run Shell", command=shell_Test)
menu_bar.add_cascade(label="Run Shell", menu=shell)


############# MAIM LOOP ###############
ide.config(menu=menu_bar)
ide.configure(bg=from_rgb((12, 40, 55)), bd=0)

ide.mainloop()
