import tkinter as tk
import tkinter.ttk as ttk
import flaskRecieve

window = tk.Tk()
window.title("Attack of the Clones!")

titleBar = tk.Frame(
    master=window,
    height=40,
    bg="dimgrey"
)

titleBar.config(
    highlightthickness=2,
    highlightbackground="black"
    )

titleBar.pack(
    fill="x"
)

titleLabel = tk.Label(
    master=titleBar,
    text="Attack Of The Clones!",
    fg="white",
    bg="dimgrey",
    font=("Helvetica", 16, "bold")
)
titleLabel.pack(
    side="left",
    padx=(100, 50)
)

nav_bar = tk.Frame(
    master=window,
    bg="black",
    width=100,
    height=600
)

nav_bar.pack(
    side="left",
    fill="y"
)
nav_bar.pack_propagate(False)

button = tk.Button(
    master=nav_bar,
    text="Run",
    width=10,
    height=2,
    command=lambda: flaskRecieve.runFlaskReceiver(button, progress, progressLabel)
)

button.pack(
    pady=10
)

photo = tk.PhotoImage(file="AttackOfTheClones.png")
resized_photo = photo.subsample(6) 
imageLabel = tk.Label(
    master=titleBar,
    image=resized_photo,
    bg="black"
)

imageLabel.image = resized_photo
imageLabel.pack(
    padx=(100, 50),
    pady=10
)

contentBox = tk.Frame(
    master=window,
    bg="white",
    width=600,
    height=600
)

contentBox.pack(
    side="right",
    fill="both",
    expand=True
)

# create the label widget for the text field
progressLabel = tk.Label(
    bg="white",
    master=contentBox,
    text="",
    font=("Helvetica", 12)
)

# add the label widget to the content_box frame
progressLabel.pack(pady=10)

# create the progress bar widget
progress = ttk.Progressbar(
    master=contentBox,
    orient="horizontal",
    mode="determinate",
    length=0,
)

# add the progress bar to the content_box frame
progress.pack(pady=10)

window.mainloop()