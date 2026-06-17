import requests
import tkinter as tk
import json
import os
from PIL import Image, ImageTk
import webbrowser

favorites = []
movies_data = []

if os.path.exists("Movie App\\favorites.json"):
    with open("Movie App\\favorites.json", "r") as f:
        favorites = json.load(f)

def add_favorite():
    selected = results_listbox.curselection()
    if not selected:
        return

    movie = results_listbox.get(selected)
    favorites.append(movie)
    with open("Movie App\\favorites.json", "w") as f:
        json.dump(favorites, f, indent=4)

def search_movies():
    results_listbox.delete(0, tk.END)  # clear previous results
    api_key = "8b8244b8"
    query = search_entry.get() if search_entry else "Marvel"  # default to "Marvel" if search_entry is not defined
    

    try:
        for page in range(1, 11):  # pages 1–10 (100 movies total)
            url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}&page={page}"
            res = requests.get(url)
            data = res.json()
            if data.get("Response") == "True":
                for movie in data.get("Search", []):
                    movies_data.append(f"{movie['Title']}")
            elif data.get("Response") == "False":
                break  # no more results, exit the loop    
    except Exception:
        movies_data.append("Error fetching movies. Please try again.")

    for movie in movies_data:
        results_listbox.insert(tk.END, movie)
    search_entry.delete(0, tk.END)  # clear search entry after search

def on_select(event):
    selected_index = results_listbox.curselection()

    if not selected_index:
        return

    movie = results_listbox.get(selected_index)
    api_key = "8b8244b8"
    url = f"http://www.omdbapi.com/?s={movie}&apikey={api_key}"
    res = requests.get(url)
    data = res.json()
    if data.get("Response") == "True":
        movie_details = data.get("Search", [])[0]  # get the first matching movie
        imdb_id = movie_details.get("imdbID", "N/A")
        new_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
        new_res = requests.get(new_url)
        new_data = new_res.json()
        title = new_data.get("Title")
        year = new_data.get("Year")
        rating = new_data.get("imdbRating")
        plot = new_data.get("Plot")
        message = f"Title: {title}\nYear: {year}\nRating: {rating}\nPlot: {plot}"
        watch_button.grid(
            row=2,
            column=3,
            padx=10,
            pady=10
        )
    else:
        message = "Movie details not found."

    details_label.config(text=message)
    

def open_favorites():
    fav_window = tk.Toplevel(window)
    fav_window.title("Favorites")
    fav_window.config(bg="black")
    fav_listbox = tk.Listbox(
    fav_window,
    font=("Arial", 14),
    bg="Orange",
    fg="white",
    width=50,
    height=20
    )
    fav_listbox.pack(padx=10, pady=10)
    def watch_movie_from_favorites():
        selected_movie = fav_listbox.get(fav_listbox.curselection())
        movie_name_before = selected_movie.replace(" ", "-").lower()
        movie_name = movie_name_before.replace(":", "")
        url = f"https://watch.plex.tv/movie/{movie_name}"
        webbrowser.open(url)
    details_label = tk.Label(
        fav_window,
        text="tap on a movie to see details",
        bg="black",
        fg="white",
        justify="left",
        wraplength=400
    )
    details_label.pack(padx=10, pady=10)
    for fav in favorites:
        fav_listbox.insert(tk.END, fav)
    watch_button = tk.Button(
        fav_window,
        text="Want to Watch?",
        command=watch_movie_from_favorites,
        cursor="hand2"
    )


    def show_fav_details(event):
        selected_index = fav_listbox.curselection()
        if not selected_index:
            return

        movie_title = fav_listbox.get(selected_index)
        api_key = "8b8244b8"
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
        res = requests.get(url)
        data = res.json()
        if data.get("Response") == "True":
            title = data.get("Title")
            year = data.get("Year")
            rating = data.get("imdbRating")
            plot = data.get("Plot")
            message = f"Title: {title}\nYear: {year}\nRating: {rating}\nPlot: {plot}"
            watch_button.pack(
                padx=10,
                pady=10
            )
        else:
            message = "Movie details not found."
        details_label.config(text=message)

    fav_listbox.bind("<<ListboxSelect>>", show_fav_details)
    details_label.config(
        text="Select a favorite movie to see details.",
        wraplength=400
    )


def watch_movie():
    selected_movie = results_listbox.get(results_listbox.curselection())
    movie_name_before = selected_movie.replace(" ", "-").lower()
    movie_name = movie_name_before.replace(":", "")
    url = f"https://watch.plex.tv/movie/{movie_name}"
    webbrowser.open(url)
    results_listbox.delete(0, tk.END)
# ------------------UI SETUP------------------ #

window = tk.Tk()
window.title("Movie Finder App")
window.config(bg="black")

bg_image = Image.open("Movie App\\images\\3f54839dc63eeef1328f7f7652fc34ff.jpg")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

search_entry = tk.Entry(window, font=("Arial", 14), bg="orange", fg="white")
search_entry.grid(row=0, column=1, padx=10, pady=10)
search_button = tk.Button(window, text="Search", font=("Arial", 14), bg="Orange", fg="white", height=0, command=search_movies, cursor="hand2")
search_button.grid(row=0, column=2, padx=10, pady=10)

results_listbox = tk.Listbox(window, font=("Arial", 14), bg="Orange", fg="white", width=50, height=20,)
results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
results_listbox.bind("<<ListboxSelect>>", on_select)

details_label = tk.Label(window, text="", fg="orange", justify="left", font=("Arial", 12, "bold"))
details_label.grid(row=1, column=3)
details_label.config(
    text="Select a movie to see details.",
    wraplength=300,
    justify="left",
    bg= "#118bd6"
)

fav_button = tk.Button(window, text="Add to Favorites", command=add_favorite, cursor="hand2")
fav_button.grid(row=2, column=0, padx=10, pady=10)
fav_screen_button = tk.Button(
    window,
    text="View Favorites",
    command=open_favorites,
    cursor="hand2"
)

watch_button = tk.Button(
    window,
    text="Want to Watch?",
    command=watch_movie,
    cursor="hand2"
)


fav_screen_button.grid(row=2, column=1)


window.mainloop()