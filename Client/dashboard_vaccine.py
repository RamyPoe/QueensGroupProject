from ast import Delete
from tkinter import *
from networking import run_background
import window, protocol
from math import floor
import functions, time

# If send thread already exists
sendThreadExists = False
sendQueue = []

# Sends vaccine info to server
def sendVaccineThread():
    # Don't spawn more than one
    global sendThreadExists, sendQueue
    if sendThreadExists: return
    sendThreadExists = True

    # Don't want to send to server many times
    time.sleep(2)

    # For every instance we wanted to send
    if len(sendQueue) > 0:
        # Send the latest one from those to the server
        info = sendQueue[-1]
        window.DATA[protocol.DATA_INDEXES[protocol.VACCINES]] = functions.compress_vaccine_data(info)
        window.NET.updatePersonalData(window.DATA, protocol.VACCINES)
        sendQueue = []

    sendThreadExists = False


# Draws table image over to hide previous symbols
def clear_vaccine_table():
    window.canvas.delete("symbol")

# Draws a square on the canvas given coord and size
def draw_square(x : int, y : int, r:int = 6):
    window.canvas.create_rectangle(x-r, y-r, x+r, y+r, fill="#FF8888", outline = "#FF8888", tags=("symbol"))
def draw_square_tile(row : int, col : int):
    draw_square(268 + col*tile_w+tile_w//2, 309 + row*tile_h+tile_h//2)

# Draws a circle on the canvas given coord and size
def draw_circle(x : int, y: int, r:int = 6):
    return window.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#FF8888", outline = "#FF8888", tags=("symbol"))
def draw_circle_tile(row : int, col : int):
    draw_circle(268 + col*tile_w+tile_w//2, 309 + row*tile_h+tile_h//2)


# Draws a square on the canvas given coord and size
def draw_square(x: int, y: int, r: int = 6):
    window.canvas.create_rectangle(x - r, y - r, x + r, y + r, fill="#FF8888", outline="#FF8888", tags=("symbol"))


def draw_square_tile(row: int, col: int):
    draw_square(268 + col * tile_w + tile_w // 2, 309 + row * tile_h + tile_h // 2)


# Draws a circle on the canvas given coord and size
def draw_circle(x: int, y: int, r: int = 6):
    return window.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#FF8888", outline="#FF8888", tags=("symbol"))


def draw_circle_tile(row: int, col: int):
    draw_circle(268 + col * tile_w + tile_w // 2, 309 + row * tile_h + tile_h // 2)


# Draws all symbols based on data
def drawFromData(data):
    # "N" : Nothing, "U" : Upcoming, "C" : completed
    for i in range(len(data)):
        s = data[i]

        if s == "N": continue
        if s == "U": draw_circle_tile(i // 18, i % 18)
        if s == "C": draw_square_tile(i // 18, i % 18)

""" (268, 309) x (1172, 681) """
# Functon which changes the symbol when clicked
def onClickChange(event=None):
    global sendThreadExists, sendQueue

    # Subtract padding for grid calc
    event.x -= 268
    event.y -= 309

    # Ensure click was in box
    if event.x < 0 or event.y < 0: return
    if event.x > 904 or event.y > 372: return

    # Compute tile clicked (18x12)
    tile_col = event.x / tile_w;
    tile_col = floor(tile_col)
    tile_row = event.y / tile_h;
    tile_row = floor(tile_row)
    index = tile_row * 18 + tile_col

    # Affect change into data and server
    vaccine_list[index] = next_cycle(vaccine_list[index])
    sendQueue.append(vaccine_list)
    if not sendThreadExists: run_background(sendVaccineThread)

    # Draw change locally
    clear_vaccine_table()
    drawFromData(vaccine_list)


# Cycle between three options, NUC
def next_cycle(s: str):
    if s == "N": return "U"
    if s == "U": return "C"
    if s == "C": return "N"


# Function which displays the vaccine tab
def dashboard():
    # Used for grid calcs
    global tile_w, tile_h
    tile_h = (372 / 12)
    tile_w = (904 / 18)

    # Setting the window
    functions.create_canvas('Vaccines')

    # Bind function to mouseclick
    window.canvas.bind("<Button 1>", onClickChange)

    # Draw static elements
    functions.draw_tabs()

    # Creating the table
    global vaccine_table_image
    vaccine_table_image = PhotoImage(
        file='assets/vaccine_table.png')
    window.canvas.create_image(106, 200, anchor="nw", image=vaccine_table_image)

    # Adding legend
    window.canvas.create_text(
        1280 // 2,
        695,
        anchor="center",
        text="A dot symbolizes upcoming, a square symbolizes completed",
        fill="#FF8888",
        font=("Inter", 15)
    )

    # De-compress data (should be 216 long) (18x12)
    global vaccine_list
    vaccine_list = functions.decompress_vaccine_data(window.DATA[protocol.DATA_INDEXES[protocol.VACCINES]])
    if len(vaccine_list) != 216: print("[WARNING] Vaccine data is missing info!")

    drawFromData(vaccine_list)
