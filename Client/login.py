from tkinter import *
import window, register, dashboard_healthcard
import protocol
import functions
from networking import run_background

# Used for displaying errors
email_small_text = None
password_small_text = None
bottom_text = None


# Function which verifies the login information
def login_verify():
    # Reset previous writings
    email_small_text.config(text="")
    password_small_text.config(text="")
    bottom_text.config(text="")

    # Get user input
    username = window.username_verify.get()
    password = window.password_verify.get()

    # Verify proper email
    match (functions.check_email(username)):
        case protocol.TOO_LONG:
            email_small_text.config(text="Email is too long!")
            return

        case protocol.INVALID_INPUT:
            email_small_text.config(text="Invalid Email input!")
            return

        case protocol.VALID_INPUT:
            pass

    # Verify proper password
    match (functions.check_password(password)):
        case protocol.TOO_LONG:
            password_small_text.config(text="Password is too long!")
            return

        case protocol.INVALID_INPUT:
            password_small_text.config(text="Invalid Password Input!")
            return

        case protocol.VALID_INPUT:
            pass

    # Send request to server
    print(f"[LOGIN] User: {username}    Pass: {password}")
    response = window.NET.login(username, password)

    # Process response
    if response == protocol.LOGIN_FAIL:
        # Display error to user
        bottom_text.config(text="Login Failed! Wrong password? User doesn't exist", fg='red')

    elif response == protocol.LOGIN_SUCCESS:
        # Save data from server
        bottom_text.config(text="Successfully Signed in!", fg='green')
        run_background(recvUserData)


# Receive user data after login and change to dashboard screen
def recvUserData():
    window.DATA = window.NET.recvPersonalData()
    window.window.after(100, goToDashboard)


# Ran in loop to check if we can move to dashboard
def goToDashboard():
    # Creating a new window
    window.window.destroy()
    window.window = Tk()
    window.window.geometry("1280x720")
    window.window.configure(bg="#FFFFFF")
    window.window.resizable(False, False)

    # Creating mock canvas to be destroyed
    window.canvas = Canvas(window.window)

    # Go to dashboard
    dashboard_healthcard.dashboard()


# Function which allows user to toggle password visibility in the entry field
def toggle_password_visible():
    if window.password_entry.cget('show') == '•':
        window.password_entry.config(show='')
    else:
        window.password_entry.config(show='•')


# Function for login screen
def login():
    # Defining variables
    window.username_verify = StringVar()
    window.password_verify = StringVar()

    # Resetting the window
    window.canvas.destroy()
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

    # Adding sign in text to top left of login window
    window.canvas.create_text(
        50.0,
        50.0,
        anchor="nw",
        text="SIGN IN",
        fill="#FF8787",
        font=("Inter Medium", 50 * -1)
    )

    # Adding the sign-in button
    global sign_in_button_img
    sign_in_button_img = PhotoImage(
        file='assets/sign_in_button.png')
    sign_in_btn = Button(
        image=sign_in_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=login_verify,
        relief="flat"
    )
    sign_in_btn.place(
        x=50.0,
        y=450.0,
        width=400.0,
        height=50.0
    )

    # Adding the or-register button
    global or_register_button_img
    or_register_button_img = PhotoImage(
        file='assets/or_register_button.png')
    or_register_btn = Button(
        image=or_register_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=register.register,
        relief="flat"
    )
    or_register_btn.place(
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

    # Adding the password visibility toggle button
    global eye_button_image
    eye_button_image = PhotoImage(
        file='assets/eye.png')
    password_toggle_button = Button(
        image=eye_button_image,
        borderwidth=0,
        bg="white",
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

    # Configuring error messages
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

    # Setting the password to hidden by default
    toggle_password_visible()
