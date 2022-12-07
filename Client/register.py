from tkinter import *
import window
import login
import protocol
from functions import check_email, check_password

# Used for displaying errors
email_small_text = None
password_small_text = None
bottom_text = None


# Functions which registers the user
def register_user():
    # Reset previous writings
    email_small_text.config(text="")
    password_small_text.config(text="")
    bottom_text.config(text="")

    # Get user input
    username = window.username_verify.get()
    password = window.password_verify.get()

    # Verify proper email
    match (check_email(username)):
        case protocol.TOO_LONG:
            email_small_text.config(text="Email is too long!")
            return

        case protocol.INVALID_INPUT:
            email_small_text.config(text="Invalid Email input!")
            return

        case protocol.VALID_INPUT:
            pass

    # Verify proper password
    match (check_password(password)):
        case protocol.TOO_LONG:
            password_small_text.config(text="Password is too long!")
            return

        case protocol.INVALID_INPUT:
            password_small_text.config(text="Invalid Password Input!")
            return

        case protocol.VALID_INPUT:
            pass

    # Send request to Server
    print(f"[REGISTER] User: {username}    Pass: {password}")
    response = window.NET.register(username, password)

    # Process response and display to user
    if response == protocol.REGISTER_SUCCESS:
        bottom_text.config(text="Successfully Registered! Please Sign in", fg='green')
    elif response == protocol.REGISTER_FAIL:
        bottom_text.config(text="Failed to Register, account already exists?", fg='red')


# Function which toggles the visibility of the password in the entry field
def toggle_password_visible():
    if window.password_entry.cget('show') == '•':
        window.password_entry.config(show='')
    else:
        window.password_entry.config(show='•')


# Function for registration screen
def register():
    # Configuring variables
    window.username_verify = StringVar()
    window.password_verify = StringVar()

    # Resetting the window
    window.canvas.destroy()
    window.window.title('Register')
    window.canvas = Canvas(
        window.window,
        bg="#FFFFFF",
        height=window.HEIGHT,
        width=window.WIDTH,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    window.canvas.place(x=0, y=0)

    # Adding register text to top left
    window.canvas.create_text(
        50.0,
        50.0,
        anchor="nw",
        text="REGISTER",
        fill="#FF8787",
        font=("Inter Medium", 50 * -1)
    )

    # Adding register button
    global register_button_img
    register_button_img = PhotoImage(
        file='assets/register_button.png')
    register_btn = Button(
        image=register_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=register_user,
        relief="flat"
    )
    register_btn.place(
        x=50.0,
        y=450.0,
        width=400.0,
        height=50.0
    )

    # Adding or sign-in button
    global or_sign_in_button_img
    or_sign_in_button_img = PhotoImage(
        file='assets/or_sign_in_button.png')
    or_sign_in_btn = Button(
        image=or_sign_in_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=login.login,
        relief="flat"
    )
    or_sign_in_btn.place(
        x=197.0,
        y=520.0,
        width=107.0,
        height=24.0
    )

    # Adding the password entry field
    global pass_entry_image
    pass_entry_image = PhotoImage(
        file='assets/pass_entry.png')
    window.canvas.create_image(
        250.0,
        343.0,
        image=pass_entry_image
    )
    window.password_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg='black',
        font=('Inter', '20'),
        highlightthickness=0,
        textvariable=window.password_verify
    )
    window.password_entry.place(
        x=60.0,
        y=333.0,
        width=380.0,
        height=30.0
    )

    # Adding the email entry field
    global user_entry_image
    user_entry_image = PhotoImage(
        file='assets/user_entry.png')
    window.canvas.create_image(
        250.0,
        198.0,
        image=user_entry_image
    )
    window.username_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg='black',
        font=('Inter', '20'),
        highlightthickness=0,
        textvariable=window.username_verify
    )
    window.username_entry.place(
        x=60.0,
        y=185.0,
        width=380.0,
        height=30.0
    )

    # Adding the toggle password visibility button
    global eye_button_image
    eye_button_image = PhotoImage(
        file='assets/eye.png')
    password_toggle_button = Button(
        image=eye_button_image,
        borderwidth=0,
        background="white",
        highlightthickness=0,
        command=toggle_password_visible,
        relief="flat"
    )
    password_toggle_button.place(
        x=390.0,
        y=325.0,
        width=50,
        height=50
    )

    # Configuring error messages text
    global email_small_text, password_small_text, bottom_text

    email_small_text = Label(window.window, text='', fg='red', bg='white')
    email_small_text.place(x=60, y=235)

    password_small_text = Label(window.window, text='', fg='red', bg='white')
    password_small_text.place(x=60, y=383)

    bottom_text = Label(window.window, text='', fg='white', bg='white', font="MS_Sans_Serif 14")
    bottom_text.place(x=window.WIDTH//2, y=570, anchor="center")

    email_small_text = Label(window.window, text='', fg='red', bg='white');
    email_small_text.place(x=60, y=235)

    password_small_text = Label(window.window, text='', fg='red', bg='white');
    password_small_text.place(x=60, y=383)

    bottom_text = Label(window.window, text='', fg='white', bg='white', font="MS_Sans_Serif 14");
    bottom_text.place(x=window.WIDTH // 2, y=570, anchor="center")

    # Setting the password visibility to hidden by default
    toggle_password_visible()
