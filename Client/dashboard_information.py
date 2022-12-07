from tkinter import *
import window
import functions
import protocol
from networking import run_background
import datetime

# Global vars
popup_window = None
input_string = None

personal_data_indexes = ["last_name", "first_name", "middle_name", "date_of_birth", "age", "address", "phone_number", "height", "weight", "bmi", "current_prescriptions_str", "current_medical_conditions_str", "family_medical_history_str"]
personal_data = {
    "last_name" : '',
    "first_name" : '',
    "middle_name" : '',

    "date_of_birth" : '',

    "address" : '',
    "phone_number" : '',

    "height" : '',
    "weight" : '',

    "current_prescriptions_str" : '',
    "current_medical_conditions_str" : '',
    "family_medical_history_str" : '',
}


# Update the data in a field
def updateData(num : int):
    # Resetting error messages
    error_text.config(text='')

    # Get the new user input
    new_data = input_string.get()

    # Check proper input
    match (functions.check_data_input(new_data)):
        case protocol.INVALID_INPUT:
            error_text.config(text='Bad input! Too long or contains bad character...')
            return

        case protocol.VALID_INPUT:
            pass

    # Update data locally
    personal_data[personal_data_indexes[num]] = new_data
    window.DATA[protocol.DATA_INDEXES[protocol.INFORMATION]] = personal_data

    # Update on server
    run_background(window.NET.updatePersonalData, window.DATA, protocol.INFORMATION)

    # Close the popup and reset screen
    popup_window.destroy()
    dashboard()


# Adding date of birth entry
def updateDataBirth():
    # Resetting error messages
    error_text.config(text='')

    # Get the new user input
    new_data = input_string.get()

    # Check proper input
    match (functions.check_birthdate(new_data)):
        case protocol.INVALID_INPUT:
            error_text.config(text='Incorrect format or incorrect date, please enter a valid date')
            return

        case protocol.VALID_INPUT:
            pass

    # Update data locally
    personal_data["date_of_birth"] = new_data
    window.DATA[protocol.DATA_INDEXES[protocol.INFORMATION]] = personal_data

    # Close the popup and reset screen
    popup_window.destroy()
    dashboard()


# Popup that asks user for info
def userInputPopup(num : int):
    global popup_window

    popup_window = Toplevel(window.window)
    popup_window.title('Edit data')
    popup_window.geometry("500x400")
    popup_window.configure(bg="white")

    # Setting the date and title string variables for the entry fields
    global input_string
    input_string = StringVar()

    # Canvas to draw on
    canvas = Canvas(
        popup_window,
        bg="#FFFFFF",
        height=600,
        width=500,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Add appointment text
    canvas.create_text(
        40.0,
        50.0,
        anchor="nw",
        text="Edit data",
        fill="#FF8888",
        font=("Inter Medium", 50 * -1)
    )

    # Adding the add button
    global add_button_image
    add_button_image = PhotoImage(
        file='assets/add_button.png')
    
    # Date Of Birth num
    if num == 3:
        add_button = Button(
            popup_window,
            image=add_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=updateDataBirth,
            relief="flat"
        )
    else:
        add_button = Button(
            popup_window,
            image=add_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: updateData(num),
            relief="flat"
        )
    add_button.place(
        x=50.0,
        y=300.0,
        width=400.0,
        height=50.0
    )

    # Adding the date and time entry field
    global input_image

    # Date Of Birth num
    if num == 3:
        input_image = PhotoImage(
            file='assets/date_time_entry.png')
        canvas.create_image(
            (50, 163),
            anchor="nw",
            image=input_image
        )

        # Adding format text
        canvas.create_text(
            50.0,
            239.0,
            anchor="nw",
            text="Please format YYYY/MM/DD",
            fill="#FF8888",
            font=("Inter Medium", 15)
        )

    else:
        input_image = PhotoImage(
            file='assets/text_box.png')
        canvas.create_image(
            (50, 163),
            anchor="nw",
            image=input_image
        )

    global input_entry
    input_entry = Entry(
        popup_window,
        bd=0,
        bg="#FFFFFF",
        fg='black',
        font=('Inter', '20'),
        highlightthickness=0,
        textvariable=input_string
    )
    input_entry.place(
        x=60.0,
        y=190.0,
        width=380.0,
        height=30.0
    )

    # Setting up the error text
    global error_text
    error_text = Label(popup_window, text='', fg='red', bg='white')
    error_text.place(x=50, y=141)


# Function which displays the information dashboard window
def dashboard():
    global personal_data

    # Setting the window
    functions.create_canvas('Information')

    # Adding the tabs
    functions.draw_tabs()

    # Update data with server
    personal_data = window.DATA[protocol.DATA_INDEXES[protocol.INFORMATION]]

    # Calc BMI
    try:
        BMI = (int(personal_data["weight"]) / int(personal_data["height"]) / int(personal_data["height"])) * 10_000
        BMI = round(BMI, 2)
    except:
        BMI = "<Unable to Calculate>"

    # Calc age
    try:
        dob = datetime.datetime.strptime ( personal_data["date_of_birth"], '%Y/%m/%d')
        AGE = ( datetime.datetime.utcnow() - dob ).days // 365
    except:
        AGE = "<Unable to Calculate>"


    # Adding the main rectangle
    window.canvas.create_rectangle(
        107.0,
        200.0,
        1173.0,
        700.0,
        fill="#FFFFFF",
        outline="#FF8888")

    # Adding the last name text
    window.canvas.create_text(
        157.0,
        214,
        anchor="nw",
        text="Last name: " + personal_data["last_name"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the first name text
    window.canvas.create_text(
        157.0,
        251,
        anchor="nw",
        text="First name: " + personal_data["first_name"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the middle name text
    window.canvas.create_text(
        157.0,
        288,
        anchor="nw",
        text="Middle name: " + personal_data["middle_name"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the date of birth text
    window.canvas.create_text(
        157.0,
        324,
        anchor="nw",
        text="Date of birth: " + personal_data["date_of_birth"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the age text
    window.canvas.create_text(
        157.0,
        361,
        anchor="nw",
        text="Age: " + str(AGE),
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the address text
    window.canvas.create_text(
        157.0,
        398,
        anchor="nw",
        text="Address: " + personal_data["address"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the phone number text
    window.canvas.create_text(
        157.0,
        435,
        anchor="nw",
        text="Phone number: " + personal_data["phone_number"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the height text
    window.canvas.create_text(
        157.0,
        472,
        anchor="nw",
        text="Height: " + personal_data["height"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the weight text
    window.canvas.create_text(
        157.0,
        508,
        anchor="nw",
        text="Weight: " + personal_data["weight"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the BMI text
    window.canvas.create_text(
        157.0,
        545,
        anchor="nw",
        text="BMI: " + str(BMI),
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the current prescriptions text
    window.canvas.create_text(
        157.0,
        582,
        anchor="nw",
        text="Current prescriptions: " + personal_data["current_prescriptions_str"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the current medical conditions text
    window.canvas.create_text(
        157.0,
        619,
        anchor="nw",
        text="Current medical conditions: " + personal_data["current_medical_conditions_str"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )

    # Adding the family medical history text
    window.canvas.create_text(
        157.0,
        656,
        anchor="nw",
        text="Family medical history: " + personal_data["family_medical_history_str"],
        fill="#FF8888",
        font=("Inter Medium", 20)
    )


    # ==================================
    # BUTTONS
    # ==================================


    # Image for edit icon
    global edit_button_image
    edit_button_image = PhotoImage(file='assets/edit_icon.png')


    # Adding the last name edit button
    last_name_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(0),
        bg='white',
        relief="flat"
    )
    last_name_button.place(
        x=121,
        y=214,
        width=20,
        height=20
    )


    # Adding the first name edit button
    first_name_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(1),
        bg='white',
        relief="flat"
    )
    first_name_button.place(
        x=121,
        y=251,
        width=20,
        height=20
    )


    # Adding the middle name edit button
    middle_name_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(2),
        bg='white',
        relief="flat"
    )
    middle_name_button.place(
        x=121,
        y=288,
        width=20,
        height=20
    )


    # Adding the date of birth edit button
    dob_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(3),
        bg='white',
        relief="flat"
    )
    dob_edit_button.place(
        x=121,
        y=324,
        width=20,
        height=20
    )


    # Adding the address edit button
    address_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(5),
        bg='white',
        relief="flat"
    )
    address_edit_button.place(
        x=121,
        y=398,
        width=20,
        height=20
    )
    

    # Adding the phone number edit button
    phone_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(6),
        bg='white',
        relief="flat"
    )
    phone_edit_button.place(
        x=121,
        y=435,
        width=20,
        height=20
    )


    # Adding the height edit button
    height_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(7),
        bg='white',
        relief="flat"
    )
    height_edit_button.place(
        x=121,
        y=472,
        width=20,
        height=20
    )


    # Adding the weight edit button
    weight_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(8),
        bg='white',
        relief="flat"
    )
    weight_edit_button.place(
        x=121,
        y=508,
        width=20,
        height=20
    )


    # Adding the prescriptions edit button
    prescriptions_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(10),
        bg='white',
        relief="flat"
    )
    prescriptions_edit_button.place(
        x=121,
        y=582,
        width=20,
        height=20
    )


    # Adding the current medical conditions edit button
    current_medical_conditions_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(11),
        bg='white',
        relief="flat"
    )
    current_medical_conditions_edit_button.place(
        x=121,
        y=619,
        width=20,
        height=20
    )


    # Adding the current medical conditions edit button
    family_medical_history_edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: userInputPopup(12),
        bg='white',
        relief="flat"
    )
    family_medical_history_edit_button.place(
        x=121,
        y=656,
        width=20,
        height=20
    )