import tkinter as tk
import pyperclip
import requests
import threading
import os
from datetime import datetime
from PIL import Image, ImageTk

windows = tk.Tk()
windows.title("Download any file here!")
windows.geometry("800x500")
windows.config(padx=20, pady=20)

# ----------------------PASTE LINK BUTTON ----------------------
def paste_link():
    link_entry.delete(0, tk.END)
    link = pyperclip.paste()
    link_entry.insert(0,link)

# ----------------------DOWNLOAD BUTTON ----------------------
def download():
    try:
        url = link_entry.get()

        response = requests.get(url)

        if response.status_code == 200:

            filename = url.split("/")[-1]

            path = f"File downloader\\{filename}"

            with open(path, "wb") as file:
                file.write(response.content)

            print("Download successful")
            size_int = os.path.getsize(path)
            sizer = str(size_int)

            if len(sizer) <= 5:
                sizer_eqf = size_int/1024
                size = f"{sizer_eqf:.2f} kb"
            elif len(sizer) > 5:
                sizer_eqf = size_int/(1024*1024)
                size = f"{sizer_eqf:.2f} mb"
        
            
            now = datetime.now()
            curr = str(now.time())
            current = curr.split(".")
            current_time = current[0]

            download_details.delete("1.0",tk.END)
            details = f"File Name: {filename}\nSize: {size}\nTime: {current_time}\n"
            download_details.insert(tk.END, details)
            
            ext = os.path.splitext(path)[1].lower()

            # IMAGE FILES
        if ext in [".png", ".jpg", ".jpeg", ".gif"]:
            img = Image.open(path)

            img.thumbnail((450, 450))

            photo = ImageTk.PhotoImage(img)

            
            download_details.image_create(tk.END, image=photo)

            download_details.image = photo

        else:
            print("Failed:", response.status_code)

    except Exception as e:
        print("Error:", e)

# ----------------------GUI SETUP----------------------
top_frame = tk.Frame(windows)
top_frame.pack(fill="x")

link_entry = tk.Entry(top_frame)
link_entry.pack(side="left", fill="x", expand= True)

paste_button = tk.Button(top_frame, text= "Paste", command= paste_link)
paste_button.pack(side="left")

download_button = tk.Button(top_frame, text="Download",command= lambda:threading.Thread(target=download, daemon= True).start())
download_button.pack(side="right")

main_frame = tk.Frame(windows)
main_frame.pack(fill="both", expand=True)

download_details = tk.Text(main_frame)
download_details.pack(fill="both", expand=True, pady= 10)


windows.mainloop()