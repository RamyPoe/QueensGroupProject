import re, protocol, base64, datetime
from io import BytesIO
import PIL.Image
from tkinter import *
import window
import dashboard_vaccine, dashboard_healthcard, dashboard_appointments, dashboard_information


# Functon that verifies if the email is valid
# https://www.c-sharpcorner.com/article/how-to-validate-an-email-address-in-python/
def check_email(email):
    if len(email) > 25: return protocol.TOO_LONG
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return protocol.VALID_INPUT if re.search(regex, email) else protocol.INVALID_INPUT


# Function that verifies if that password is formatted correctly
# https://stackoverflow.com/questions/89909/how-do-i-verify-that-a-string-only-contains-letters-numbers-underscores-and-da """
def check_password(password):
    if len(password) > 20: return protocol.TOO_LONG
    regex = "^[A-Za-z0-9!@#$%&]+$"
    return protocol.VALID_INPUT if re.search(regex, password) else protocol.INVALID_INPUT

# Make sure input data has no special characters
def check_data_input(input):
    if len(input) > 40: return protocol.INVALID_INPUT
    regex = "^[A-Za-z0-9!@#$%&, ]+$"
    return protocol.VALID_INPUT if re.search(regex, input) else protocol.INVALID_INPUT


# Checks if date input from user was valid
def check_birthdate(date : str):
    if len(date) != 10: return protocol.INVALID_INPUT
    try:
        datetime.datetime.strptime(date, '%Y/%m/%d')
        return protocol.VALID_INPUT
    except Exception as e:
        print(e)
        return protocol.INVALID_INPUT

# Function that checks if the date input from the user is valid
def check_date(date: str):
    if len(date) != 16: return protocol.INVALID_INPUT
    try:
        datetime.datetime.strptime(date, '%Y/%m/%d %H:%M')
        return protocol.VALID_INPUT
    except Exception as e:
        print(e)
        return protocol.INVALID_INPUT


# Returns PIL Image from base64 string
def base64_to_Image(data: str):
    im_bytes = base64.b64decode(data.encode())  # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    return PIL.Image.open(im_file)  # img is now PIL Image object


# Return base64 string from PIL image
def Image_to_base64(img):
    img = img.convert('RGB')
    im_file = BytesIO()
    img.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64.decode()


# Takes vaccine data, de-compresses into list
def decompress_vaccine_data(data: str):
    # Output var
    out = []

    # Outer vars
    data = data
    num = None
    ltr = None
    i = 1

    while data != "":
        # Do while
        while True:
            num = data[:i]
            if not num.isnumeric():
                ltr = data[i - 1]
                data = data[i:]
                i = 1
                break
            i += 1

        num = int(num[:-1])
        for _ in range(num):
            out.append(ltr)

    return out


# Takes de-compressed list, compresses into string
def compress_vaccine_data(data):
    # Output string
    out = ""

    # Outer vars
    key = data[0]
    length = 0

    # Loop
    for i in range(len(data)):
        if key != data[i]:
            out += f"{length}{key}"
            length = 1
            key = data[i]
        else:
            length += 1
    out += f"{length}{key}"

    # Return output string
    return out


# Draws tab for all the tabs
def draw_tabs():
    # Adding "myHealth Dashboard" text to top left
    window.canvas.create_text(
        106.0,
        52.99999999999999,
        anchor="nw",
        text="myHealth Dashboard",
        fill="#FF8888",
        font=("Inter Medium", 52 * -1)
    )

    # Creating information tab button on top
    global healthcard_button_image
    healthcard_button_image = PhotoImage(
        file='assets/healthcard_button.png')
    healthcard_button = Button(
        image=healthcard_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=dashboard_healthcard.dashboard,
        relief="flat"
    )
    healthcard_button.place(
        x=107.31511688232422,
        y=125.3313980102539,
        width=266.31109619140625,
        height=59.18022918701172
    )

    # Creating vaccine tab button on top
    global vaccine_button_image
    vaccine_button_image = PhotoImage(
        file='assets/vaccine_button.png')
    vaccine_button = Button(
        image=vaccine_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=dashboard_vaccine.dashboard,
        relief="flat"
    )
    vaccine_button.place(
        x=639.9371948242188,
        y=125.3313980102539,
        width=266.31103515625,
        height=59.18022918701172
    )

    # Creating appointments tab button on top
    global appointments_button_image
    appointments_button_image = PhotoImage(
        file='assets/appointments_button.png')
    appointments_button = Button(
        image=appointments_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=dashboard_appointments.dashboard,
        relief="flat"
    )
    appointments_button.place(
        x=373.62615966796875,
        y=125.3313980102539,
        width=266.31103515625,
        height=59.18022918701172
    )

    # Creating records tab button on top
    global information_button_image
    information_button_image = PhotoImage(
        file='assets/information_button.png')
    information_button = Button(
        image=information_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=dashboard_information.dashboard,
        relief="flat"
    )
    information_button.place(
        x=906.2482299804688,
        y=125.3313980102539,
        width=266.31103515625,
        height=59.18022918701172
    )


# Function which creates the canvas
def create_canvas(window_title: str):
    # Clearing the window
    window.canvas.delete(all)

    # Setting window title
    window.window.title(window_title)

    # Creating a canvas within the window to place items onto
    window.canvas = Canvas(
        window.window,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    window.canvas.place(x=0, y=0)
