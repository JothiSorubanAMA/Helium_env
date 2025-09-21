"""
Created on Sat Jun 21 22:15:53 2025

@author: jothisorubanst
"""

import subprocess
import tempfile
import tkinter.messagebox
from tkinter import ttk
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter import *
from tkinter.filedialog import askopenfilename
# importing all the needed modules
from tkinter.filedialog import asksaveasfilename
import customtkinter
import speech_recognition as sr
from PIL import Image
from PyQt5.sip import delete
from customtkinter import CTkImage
from editor_themes import *
import ttkbootstrap as tb
from fpdf import FPDF
from tkinter import filedialog
from fpdf import FPDF

#creating form
form=customtkinter.CTk()
form.title("Helium_env")
form.geometry("800x600")
form.iconbitmap("asset/he_icon.ico")



#global variable for file path
global_path = ''

def set_global_path(path):
    global global_path
    global_path = path

#to close the uncloseed symbol
def auto_create(event):
        char = event.char
        pairs = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}

        if char in pairs:
            current_pos = editor.index(INSERT)
            editor.insert(current_pos, pairs[char])
            editor.mark_set(INSERT, current_pos)  # Put cursor between brackets

e_font = ("Courier", 18)
editor = Text (font=e_font,fg="white",bg="#202b61",undo=True,wrap="none")
editor.pack(fill='both',expand=TRUE)

scrollbar_v=Scrollbar(editor,command=editor.yview)
scrollbar_v.pack(side=RIGHT,fill='y')
editor.config(yscrollcommand=scrollbar_v.set)

scrollbar_h=Scrollbar(editor,command=editor.xview)
scrollbar_h.pack(side=BOTTOM,fill='x')
editor.config(xscrollcommand=scrollbar_h.set)


color = ColorDelegator()
color.tagdefs["COMMENT"] = {"foreground": "#888888"}     # gray comments
color.tagdefs["KEYWORD"] = {"foreground": "#569cd6"}     # blue keywords
color.tagdefs["STRING"] = {"foreground": "#ce9178"}      # orange strings
Percolator(editor).insertfilter(color)

#editor creation
editor.bind('<Key>',auto_create)
option_panel = Frame(form,height=60,background="white")
option_panel.pack(fill='x')

def run():
    output = Toplevel(form)
    output.title("output")
    output.geometry("600x200")
    console = Text(output,fg="green",)
    console.pack(fill='both',expand=TRUE)
    output.resizable(FALSE,FALSE)
    console.delete("1.0",END)
    code = editor.get("1.0",END)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    result = subprocess.run(["python", tmp_path], capture_output=True, text=True)
    # Show output and errors
    if result.stdout:
        console.insert(END, result.stdout)
    if result.stderr:
        console.insert(END, result.stderr)
        console.config(fg="red")
    console.insert(END, ' ~~programm finished.')

def save():
    global global_path  # Declare it so we can read and write to it

    if global_path == '':
        code_path = asksaveasfilename(defaultextension=".py", filetypes=[("Python File", "*.py"),("Text File", "*.txt")])
        if code_path:  # Only proceed if a path was selected
            with open(code_path, "w") as file:
                content = editor.get("1.0", END)
                file.write(content)
            form.title("Helium_env  " + code_path)
            global_path = code_path  # Save the new path
    else:
        with open(global_path, "w") as file:
            content = editor.get("1.0", END)
            file.write(content)
        form.title("Helium_env  " + global_path)

def save_as():
    code_path = asksaveasfilename(defaultextension=".py", filetypes=[("Python File", "*.py"), ("Text File", "*.txt")])
    if code_path:  # Only proceed if a path was selected
        with open(code_path, "w") as file:
            content = editor.get("1.0", END)
            file.write(content)
        form.title("Helium_env  " + code_path)


def open_f():
    file_path = askopenfilename(filetypes=[("Python Files", "*.py"),("Text File", "*.txt"),("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            editor.delete("1.0", END)  # Clear current text
            editor.insert("1.0", content)
            form.title("Helium_env  "+file_path)
            set_global_path(file_path)

def new():
    new_f=Toplevel(form)
    new_f.title("Helium_env (New File) ")
    new_f.geometry("200x150")
    new_f_code = ['Tkinter window','Simple Python Program']
    clicked = StringVar()
    clicked.set(new_f_code[1])

    choose = OptionMenu(new_f,clicked,*new_f_code)
    choose.pack(pady=10,padx=5)

    def select():
        if clicked.get() == new_f_code[0]:
            new_f.destroy()
            editor.delete("1.0",END)
            editor.insert("1.0",'''from tkinter import *
root = Tk()
root.title("title")
root.geometry("500x500")


root.mainloop()            ''')


        elif clicked.get() == new_f_code[1]:
            new_f.destroy()
            editor.delete("1.0",END)
            editor.insert("1.0",'# start to program!')


    ok_button = customtkinter.CTkButton(new_f,text="OK",command=select)
    ok_button.pack(pady=10,padx=5)



def src():
    code_rec=sr.Recognizer()
    try:
        with sr.Microphone() as source:
            code_rec.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = code_rec.listen(source)

        code = code_rec.recognize_google(audio)
        code = code.lower()
        if code == 'print':
            editor.insert(INSERT, 'print("")''')
        elif code == 'exit the editor':
            form.destroy()
        elif code == 'save file':
            save()
        elif code == 'save':
            save()
        elif code == 'save the file':
            save()
        elif code == 'open file':
           open_f()
        elif code == 'open':
            open_f()
        elif code == 'open a file':
            open_f()
        elif code == 'run the program':
            run()
        elif code == 'create a new program':
            new()
        elif code == 'open a new program':
            new()
        elif code == 'create if':
            editor.insert(INSERT, '''if command():
            #to do''')
        elif code == 'install module':
            ins_mod()

    except sr.UnknownValueError:
        tkinter.messagebox.showerror("Speech Error", "Sorry, I couldn't understand your voice. Please speak clearly.")

def f_r():
    fr = Toplevel(form)
    fr.title("Find & Replace")
    fr.geometry("350x220")

    f_label = Label(fr, text="Find")
    f_label.pack(pady=7)

    find = customtkinter.CTkEntry(fr, fg_color="orange", width=300)
    find.pack(padx=5, pady=10)

    r_label = Label(fr, text="Replace With")
    r_label.pack(pady=7)

    replace = customtkinter.CTkEntry(fr, fg_color="green", width=300)
    replace.pack(padx=5, pady=10)

    def f_r_func():
        find_text = find.get()
        replace_text = replace.get()
        content = editor.get("1.0", END)

        if find_text:
            new_content = content.replace(find_text, replace_text)
            editor.delete("1.0", END)
            editor.insert("1.0", new_content)
            tkinter.messagebox.showinfo("Replace Complete", f"All occurrences of '{find_text}' replaced with '{replace_text}'")

    ok_but = customtkinter.CTkButton(fr, text="Replace All", command=f_r_func, width=100)
    ok_but.pack(padx=5, pady=10)

def library():
    lib=Toplevel(form)
    lib.title("Library")
    lib.geometry("500x500")
    module_choose = tkinter.ttk.Combobox()
    module=tb.Frame(lib)
    module.pack()



def ins_mod():
    ins=Toplevel(form)
    ins.title("Install Module")
    ins.geometry("450x150")
    ins_label = Label(ins, text="To install module enter the name of the module you want to install")
    ins_label.pack(pady=7)
    ins_textbox=Entry(ins)
    ins_textbox.pack(padx=5, pady=10)

    def ins_func():
        module_name = ins_textbox.get()
        output=Text(ins,height=10)
        output.pack()
        result = subprocess.run(["pip", "install", module_name], capture_output=True, text=True)
        output.delete(1.0, END)
        output.insert(END, result.stdout if result.returncode == 0 else result.stderr)

    ins_button = Button(ins, text="Install Module", command=ins_func)
    ins_button.pack(padx=5, pady=10)


def pdf_c():
        t=editor.get("1.0", END)
        file=open('pdf_c.txt','w')
        file.write(t)
        file.close()
        file = open("pdf_c.txt", "r")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        for i in file:
            pdf.cell(200, 10, txt=i, ln=1)
        file.close()
        f_name=filedialog.asksaveasfilename(defaultextension=".pdf")
        pdf.output(f_name)





main_menu=Menu(form, tearoff=False)
form.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new)
file_menu.add_command(label="Open", command=open_f)
file_menu.add_command(label="Save", command=save)
file_menu.add_command(label="Save as", command=save_as)
file_menu.add_command(label="Exit", command=exit)

edit_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=editor.edit_undo)
edit_menu.add_command(label="Redo", command=editor.edit_redo)
edit_menu.add_command(label='find & replace', command=f_r)

exp_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Export", menu=exp_menu)
exp_menu.add_command(label="PDF", command=pdf_c)

run_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="run python program", command=run)

undo_img = CTkImage(light_image=Image.open("asset/redo.png"))
undo_but=customtkinter.CTkButton(master=option_panel, image=undo_img, text="", command=editor.edit_undo, fg_color="#ffffff",height=30,width=30)
undo_but.pack(side=LEFT, padx=10, pady=10)

redo_img = CTkImage(light_image=Image.open("asset/undo.png"))
redo_but=customtkinter.CTkButton(master=option_panel, image=redo_img, text="", command=editor.edit_redo, fg_color="#ffffff",height=30,width=30)
redo_but.pack(side=LEFT, padx=10, pady=10)

src_img = CTkImage(light_image=Image.open("asset/src.png"))
src_but=customtkinter.CTkButton(master=option_panel, image=src_img, text="", command=src, fg_color="#ffffff",height=30,width=30)
src_but.pack(side=LEFT, padx=10, pady=10)

add_module_img = CTkImage(light_image=Image.open("asset/install_mod.png"))
add_module_but=customtkinter.CTkButton(master=option_panel, image=add_module_img, text="", command=ins_mod, fg_color="#ffffff",height=30,width=30)
add_module_but.pack(side=LEFT, padx=10, pady=10)

l_theme=Label(master=option_panel,text="THEMES: ",background='white',foreground='black')
l_theme.pack(pady=10,padx=10)

def theme_choose(choice):
    if choice == 'Dark':
        editor.config(bg=dark_theme['bg'],fg=dark_theme['fg'],selectbackground=dark_theme['selectbackground'],insertbackground=dark_theme['cursor_color'])
    elif choice == 'Light':
        editor.config(bg=light_theme['bg'],fg=light_theme['fg'],selectbackground=light_theme['selectbackground'],insertbackground=light_theme['cursor_color'])
    elif choice == 'Default':
        editor.config(bg=default_theme['bg'], fg=default_theme['fg'], selectbackground=default_theme['selectbackground'],insertbackground=dark_theme['cursor_color'])



theme_op = ['Default','Light','Dark']
theme_click=StringVar()
theme_click.set(theme_op[0])

theme_choose = customtkinter.CTkComboBox(master=option_panel, values=theme_op,command=theme_choose,state='readonly')
theme_choose.pack(pady=10)
theme_choose.set(theme_op[0])
def on_close():
    if tkinter.messagebox.askyesno("Exit", "Do you want to exit Helium IDE?"):
        form.destroy()


form.protocol("WM_DELETE_WINDOW", on_close)

form.mainloop()