from tkinter import *
from tkinter import filedialog
import window
from PIL import Image, ImageTk
import functions, protocol
from networking import run_background

# For displaying images
label_image1 = None
label_image2 = None


# Change healthcard image
def uploadNewImage(image_num=-1):
    # Popup for user to select image
    filename = filedialog.askopenfilename(filetypes=[("PNG", ".png"), ("JPG", ".jpg"), ("JPEG", ".jpeg")])
    if not filename: return
    if image_num == -1: return

    # Open image and resize
    image = Image.open(filename)
    image = image.resize((470, 350))
    image = image.convert('RGB')

    # Show change locally
    _image = ImageTk.PhotoImage(image)
    if image_num == 0:
        # Image #1
        window.canvas.create_image(111, 310, anchor="nw", image=_image)

    elif image_num == 1:
        # Image #2
        window.canvas.create_image(698, 310, anchor="nw", image=_image)

    # Write new data to server
    image = image.resize( (470 // 2, 350 // 2) )
    window.DATA[protocol.DATA_INDEXES[protocol.HEALTHCARD]] [image_num] = functions.Image_to_base64(image)
    run_background ( window.NET.updatePersonalData, window.DATA, protocol.HEALTHCARD )
    


# Function which displays the dashboard window
def dashboard():
    # Setting the main window
    functions.create_canvas('Healthcard')

    # Health card text label
    window.canvas.create_text(
        1280 // 2,
        247.37673950195312,
        anchor="center",
        text="Health Card",
        fill="#FF8888",
        font=("Inter Regular", 32 * -1)
    )

    # Creating health card slot for image
    window.canvas.create_rectangle(
        106.0,
        305.0,
        587.0,
        667.0,
        fill="#FFFFFF",
        outline="#FF8888")

    # Creating additional box for second image
    window.canvas.create_rectangle(
        693.0,
        305.0,
        1174.0,
        667.0,
        fill="#FFFFFF",
        outline="#FF8888")

    # Draw static elements
    functions.draw_tabs()

    # Creating upload button to upload healthcard #1
    global upload_button_image
    upload_button_image = PhotoImage(
        file='assets/upload_button.png')
    upload_button1 = Button(
        image=upload_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: uploadNewImage(image_num=0),
        relief="flat"
    )
    upload_button1.place(
        x=317.567444,
        y=220,
        width=57.8651123046875,
        height=57.8651123046875
    )
    window.canvas.create_text(
        346.5,
        280.0,
        anchor="n",
        text="Upload",
        fill="#FF8888",
        font=("Inter Regular", 13 * -1)
    )

    # Creating upload button to upload healthcard #2
    upload_button2 = Button(
        image=upload_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: uploadNewImage(image_num=1),
        relief="flat"
    )
    upload_button2.place(
        x=904.567444,
        y=220,
        width=57.8651123046875,
        height=57.8651123046875
    )
    window.canvas.create_text(
        933.5,
        280.0,
        anchor="n",
        text="Upload",
        fill="#FF8888",
        font=("Inter Regular", 13 * -1)
    )

    # Converting base64 to tkinter image
    global label_image1, label_image2
    label_image1 = ImageTk.PhotoImage(
        functions.base64_to_Image(window.DATA[protocol.DATA_INDEXES[protocol.HEALTHCARD]][0]).resize((470, 350)))
    label_image2 = ImageTk.PhotoImage(
        functions.base64_to_Image(window.DATA[protocol.DATA_INDEXES[protocol.HEALTHCARD]][1]).resize((470, 350)))

    # Image #1
    window.canvas.create_image(
        111,
        310,
        anchor="nw",
        image=label_image1
    )

    # Image #2
    window.canvas.create_image(
        698,
        310,
        anchor="nw",
        image=label_image2
    )
