import os
import tkinter as tk
import shutil
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# ---------------- ROOT ---------------- #
window = tk.Tk()
window.title("File Manager")
window.geometry("800x500")

# ---------------- STATE ---------------- #
current_folder = os.getcwd()

# ---------------- UI ---------------- #
top_frame = tk.Frame(window)
top_frame.pack(fill="x")

path_label = tk.Label(top_frame, text=current_folder)
path_label.pack(side="left")

back_button = tk.Button(top_frame, text="Back")
back_button.pack(side="right")

action_frame = tk.Frame(window)
action_frame.pack(fill="x")

new_file_btn = tk.Button(action_frame, text="New File")
new_file_btn.pack(side="left")

new_folder_btn = tk.Button(action_frame, text="New Folder")
new_folder_btn.pack(side="left")

rename_btn = tk.Button(action_frame, text="Rename")
rename_btn.pack(side="left")

delete_btn = tk.Button(action_frame, text="Delete")
delete_btn.pack(side="left")

search_frame = tk.Frame(window)
search_frame.pack(fill="x")

search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True)

search_button = tk.Button(search_frame, text="Search")
search_button.pack(side="left")

clear_search_btn = tk.Button(search_frame, text="Clear Search")
clear_search_btn.pack(side="left")

main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True)

listbox = tk.Listbox(main_frame, width=40)
listbox.pack(side="left", fill="y")


text_area = tk.Text(main_frame)
text_area.pack(side="right", fill="both", expand=True)

# ---------------- LOAD FOLDER ---------------- #
def load_folder(path):
    global current_folder

    current_folder = path
    path_label.config(text=current_folder)

    listbox.delete(0, tk.END)

    for item in os.listdir(current_folder):
        listbox.insert(tk.END, item)

    text_area.delete("1.0", tk.END)

# ---------------- OPEN ITEM ---------------- #
def open_item(event):
    global current_folder

    selected = listbox.get(listbox.curselection())
    path = os.path.join(current_folder, selected)

    # FOLDER
    if os.path.isdir(path):
        load_folder(path)

    # FILE
    else:
        ext = os.path.splitext(path)[1].lower()

        # IMAGE FILES
    if ext in [".png", ".jpg", ".jpeg", ".gif"]:
        try:
            img = Image.open(path)

            img.thumbnail((450, 450))

            photo = ImageTk.PhotoImage(img)

            text_area.delete("1.0", tk.END)
            text_area.image_create(tk.END, image=photo)

            text_area.image = photo

        except:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, "Cannot open image.")

    # TEXT FILES
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, content)

            text_area.image = None

        except:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, "Cannot open file.")
# ------------------ GET SELECTED FILE ---------------- #
def get_selected_path():
    try:
        selected = listbox.get(listbox.curselection())
        return os.path.join(current_folder, selected)
    except:
        return None

# ------------------ DELETE ITEM ---------------- #
def delete_item():
    path = get_selected_path()
    if not path:
        return

    if os.path.isdir(path):
        warning = messagebox.askyesno("Delete Folder", "Are you sure you want to delete this folder and all its contents?")
        if warning == False:
            return
        else:
            shutil.rmtree(path)
    else:
        warning = messagebox.askyesno("Delete File", "Are you sure you want to delete this file?")
        if warning == False:
            return
        else:
            os.remove(path)

    load_folder(current_folder)

# ------------------ CREATE NEW FOLDER ---------------- #
def create_new_folder():
    folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
    if folder_name:
        if os.path.exists(os.path.join(current_folder, folder_name)):
            messagebox.showerror("Error", "A folder with this name already exists!")
        else:
            path = os.path.join(current_folder, folder_name)
            os.makedirs(path)
            load_folder(current_folder)

# ------------------ CREATE NEW FILE ---------------- #
def create_new_file():
    file_name = simpledialog.askstring("New File", "Enter file name:")
    if file_name:
        if os.path.exists(os.path.join(current_folder, file_name)):
            messagebox.showerror("Error", "A file with this name already exists!")
        else:
            path = os.path.join(current_folder, file_name)
            with open(path, "w") as f:
                pass
            load_folder(current_folder)

# ---------------- RENAME ITEM ---------------- #
def rename_item():
    old_path = get_selected_path()
    if not old_path:
        return

    old_name = os.path.basename(old_path)

    new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=old_name)

    if not new_name:
        return

    new_path = os.path.join(current_folder, new_name)

    if os.path.exists(new_path):
        messagebox.showerror("Error", "A file with this name already exists!")
        return

    try:
        os.rename(old_path, new_path)
        load_folder(current_folder)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- SEARCH ITEM ---------------- #
def search():
    search_text = search_entry.get().strip().lower()

    listbox.delete(0, tk.END)

    for root, dirs, files in os.walk(current_folder):
        for name in files + dirs:
            if search_text in name.lower():
                full_path = os.path.join(root, name)
                listbox.insert(tk.END, full_path)

# ---------------- CLEAR SEARCH ---------------- #
def clear_search():
    search_entry.delete(0, tk.END)
    load_folder(current_folder)

# ---------------- BACK BUTTON ---------------- #
def go_back():
    global current_folder

    parent = os.path.dirname(current_folder)

    if parent != current_folder:
        load_folder(parent)

# ---------------- BINDINGS ---------------- #
listbox.bind("<Double-Button-1>", open_item)
back_button.config(command=go_back)
new_file_btn.config(command=create_new_file)
new_folder_btn.config(command=create_new_folder)
delete_btn.config(command=delete_item)
rename_btn.config(command=rename_item)
search_button.config(command=search)
clear_search_btn.config(command=clear_search)
# ---------------- START ---------------- #
load_folder(current_folder)

window.mainloop()