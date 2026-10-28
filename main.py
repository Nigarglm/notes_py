import tkinter as tk
from tkinter import messagebox
import json
import os

# Rengler ve fayl
BG = "#101827"
PANEL = "#1B263B"
EDITOR = "#243249"
BLUE = "#5B8DEF"
WHITE = "#F1F5F9"
GRAY = "#9CAEC5"
RED = "#DC4C4C"
DARK_RED= "#B93636"

FILE_NAME = "notes.txt"

notes = []
selected_index = None


# Fayldan qeydleri oxumaq
def load_notes():
    global notes

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                notes = [
                    note for note in data
                    if isinstance(note, dict)
                    and isinstance(note.get("title"), str)
                    and isinstance(note.get("content"), str)
                ]
            else:
                notes = []

        except (json.JSONDecodeError, OSError):
            notes = []
    else:
        notes = []

# Qeydleri fayla yazmaq
def save_to_file():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            notes,
            file,
            ensure_ascii=False,
            indent=4
        )

# Qeydlerin siyahisini yenile
def refresh_notes():
    note_list.delete(0, tk.END)

    for note in notes:
        note_list.insert(tk.END, note["title"])

# Yeni qeyd yarat
def create_note():
    global selected_index

    selected_index = None

    note_list.selection_clear(0, tk.END)

    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

    title_entry.focus_set()

# Qeydi ac ve redakte et
def open_note(event=None):
    global selected_index

    selection = note_list.curselection()

    if not selection:
        return

    selected_index = selection[0]
    note = notes[selected_index]

    title_entry.delete(0, tk.END)
    title_entry.insert(0, note["title"])

    content_text.delete("1.0", tk.END)
    content_text.insert("1.0", note["content"])

# Qeydi yadda saxlamaq
def save_note():
    global selected_index

    title = title_entry.get().strip()
    content = content_text.get("1.0", "end-1c")

    if not title:
        messagebox.showwarning(
            "Missing Title",
            "Please enter a title for your note.",
            parent= root
        )
        title_entry.focus_set()
        return

    # Movcud qeydlerin kopyasini saxlayiriq
    old_notes = [note.copy() for note in notes]
    old_index = selected_index

    #Yeni qeyd yaradiriq
    if selected_index is None:
        notes.append({
            "title": title,
            "content": content
        })
        selected_index = len(notes)-1
    #Movcud qeydi yenileyirik
    else:
        notes[selected_index]["title"] = title
        notes[selected_index]["content"] = content

    #Fayla yazmaq
    try:
        save_to_file()
    except OSError as error:
        notes.clear()
        notes.extend(old_notes)
        selected_index = old_index

        messagebox.showerror(
            "Save Error",
            f'Could not save the note:\n{error}',
            parent=root
        )
        return

    refresh_notes()

    note_list.selection_set(selected_index)
    note_list.activate(selected_index)

    messagebox.showinfo(
        "Success",
        "Your note has been saved",
        parent = root
    )

# Qeydi sil
def delete_note():
    global selected_index

    if selected_index is None:
        messagebox.showwarning(
            "No Note Selected",
            "Please select a note to delete",
            parent=root
        )
        return

    answer = messagebox.askyesno(
        "Delete Note",
        "Are you sure you want to delete this note?",
        parent = root
    )
    if not answer:
        return

    old_notes = [note.copy() for note in notes]

    notes.pop(selected_index)

    try:
        save_to_file()
    except OSError as error:
        notes.clear()
        notes.extend(old_notes)

        messagebox.showerror(
            "Delete Error",
            f'Could not save changes:\n{error}',
            parent = root
        )
        return

    refresh_notes()
    create_note()

    messagebox.showinfo(
        "Deleted",
        "Note deleted successfully",
        parent=root
    )

# UI
root = tk.Tk()
root.title("My Notes")
root.geometry("900x600")
root.minsize(700, 450)
root.configure(bg=BG)

root.grid_columnconfigure(0, minsize=240)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

sidebar = tk.Frame(
    root,
    bg= PANEL,
    width=240
)

sidebar.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(12,0),
    pady=12
)

sidebar.grid_propagate(False)
sidebar.grid_rowconfigure(4, weight=1)
sidebar.grid_columnconfigure(0, weight=1)

tk.Label(
    sidebar,
    text="MY NOTES",
    font=("Consolas", 17, "bold"),
    bg=PANEL,
    fg=WHITE
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=18,
    pady=(20,5)
)

tk.Label(
    sidebar,
    text="Your personal space",
    font=("Consolas", 10),
    bg=PANEL,
    fg=GRAY
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=20,
    pady=(0, 20)
)

new_button = tk.Button(
    sidebar,
    text="Create New Note",
    font=("Consolas", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    command=create_note
)

new_button.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=16,
    pady=(0,20),
    ipady=8
)

tk.Label(
    sidebar,
    text="Your Notes",
    font=("Consolas", 9, "bold"),
    bg=PANEL,
    fg=GRAY
).grid(
    row=3,
    column=0,
    sticky="w",
    padx=20,
    pady=(0,8)
)

note_list = tk.Listbox(
    sidebar,
    bg=PANEL,
    fg=WHITE,
    font=("Consolas", 11)
)
note_list.grid(
    row=4,
    column=0,
    sticky="nsew",
    padx=10,
    pady=(0,12)
)

note_list.bind("<<ListboxSelect>>", open_note)

editor = tk.Frame(root, bg=BG)

editor.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=20,
    pady=12
)

editor.grid_columnconfigure(0, weight=1)
editor.grid_rowconfigure(5, weight=1)

tk.Label(
    editor,
    text="Note Editor",
    font=("Consolas", 22, "bold"),
    bg=BG,
    fg=WHITE
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=(8,4)
)

tk.Label(
    editor,
    text="Write your thoughts and ideas",
    font=("Consolas", 10),
    bg=BG,
    fg=GRAY
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=(0,20)
)

tk.Label(
    editor,
    text="TITLE",
    font=("Consolas", 9, "bold"),
    bg=BG,
    fg=GRAY
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=(0,7)
)

title_entry = tk.Entry(
    editor,
    font=("Consolas", 12),
    bg=EDITOR,
    fg=WHITE
)
title_entry.grid(
    row=3,
    column=0,
    sticky="ew",
    ipady=12,
    pady=(0,16)
)

tk.Label(
    editor,
    text="CONTENT",
    font=("Consolas", 9, "bold"),
    bg=BG,
    fg=GRAY
).grid(
    row=4,
    column=0,
    sticky="w",
    pady=(0,7)
)

content_text = tk.Text(
    editor,
    font=("Consolas", 12),
    bg=EDITOR,
    fg=WHITE,
    padx=14,
    pady=14
)
content_text.grid(
    row=5,
    column=0,
    sticky="nsew"
)

button_frame = tk.Frame(
    editor,
    bg=BG
)
button_frame.grid(
    row=6,
    column=0,
    sticky="ew",
    pady=(14,4)
)

delete_button = tk.Button(
    button_frame,
    text="Delete Note",
    font=("Consolas", 12, "bold"),
    bg=RED,
    fg=WHITE,
    command=delete_note
)
delete_button.pack(side="left",ipadx=18,ipady=8)

save_button = tk.Button(
    button_frame,
    text="Save Note",
    font=("Consolas", 12, "bold"),
    bg=RED,
    fg=WHITE,
    command=save_note
)
save_button.pack(side="right",ipadx=18,ipady=8)

load_notes()
refresh_notes()
create_note()

root.mainloop()

