import window
from tkinter import *


# Function which displays if app fails to connect to the server
def fail_window():
    window.canvas = Canvas(
        window.window,
        bg="#FFFFFF",
        height=window.HEIGHT,
        width=window.WIDTH,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    # Adding the text which says failed to connect
    Label(window.window, text='Failed to\nConnect!', fg='#ff8787', bg='white', font="MS_Sans_Serif 40").place(x=window.WIDTH//2, y=window.HEIGHT//2, anchor="center")
