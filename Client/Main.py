import window
import login
import fail_window
from tkinter import *
from networking import Network, run_background

# Creating the window
window.window = Tk()
window.window.title('Sign In')

# Configure window dimensions
WIDTH, HEIGHT = window.WIDTH, window.HEIGHT
window.window.geometry(f"{WIDTH}x{HEIGHT}")
window.window.configure(bg="white")

# Mock Window
window.canvas = Canvas(
    window.window,
    bg="#FFFFFF",
    height=window.HEIGHT,
    width=window.WIDTH,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

# Thread for networking
window.NET = Network() # MockNetwork( True | False )
run_background (window.NET.connect_to, *('localhost', 9848))

# Wait for a response
while (window.NET.status == 0): pass

# Process response
if (window.NET.status == 1):
    # Failed, show fail screen
    fail_window.fail_window()

elif (window.NET.status == 2):
    # Starting Screen
    login.login()


# Start program
window.window.resizable(False, False)
window.window.mainloop()