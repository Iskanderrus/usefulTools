# בס״ד
import datetime
import json
import random
import re
import string
import sys
from pathlib import Path
from tkinter import Tk, Label, Button, PhotoImage, Canvas, Entry, simpledialog, messagebox

import pyperclip
from PIL import Image, ImageTk

FONT_NAME = 'TkMenuFont'
DATA_FILE = Path('../../../Documents/password_manager_log.json')

def ensure_file_exists():
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w') as data_file:
            json.dump({}, data_file, indent=4)

ensure_file_exists()

# default values for the password
lower_case_number = 10
upper_case_number = 8
digits_number = 5
symbols_number = 5


def search_button_func():
    try:
        with open(DATA_FILE, 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo("File does not exists",
                            f"Please make your first entry and save it.")

    else:
        website = website_entry.get()
        try:
            username = data[website]['username']
            password = data[website]['password']
        except KeyError:
            messagebox.showinfo("Entry does not exists",
                                f"This website is not found in your database")
        else:
            pyperclip.copy(password)
            messagebox.showinfo("Entry exists",
                                f"Saved username: {username}\n"
                                f"Saved password: {password}\n\n"
                                f"This password is copied to clipboard.")


def exit_app():
    """
    Function to exit from the app saving the password if generated to ensure that the password is not get lost
    :return:
    """
    if password_entry.get():
        adding_password()

    sys.exit()


def special_requirements():
    """
    Function to adjust the default password settings according to user requirements.
    """
    global lower_case_number, upper_case_number, digits_number, symbols_number

    def ask_for_number(prompt):
        user_input = simpledialog.askstring(
            title="Number required!", prompt=prompt
        )
        if user_input is None:
            return None
        try:
            return int(user_input)
        except ValueError:
            messagebox.showinfo("Invalid input", "Please enter a valid number")
            return None

    lower_case_number = ask_for_number("How many lowercase characters are required?")
    if lower_case_number is None:
        return
    upper_case_number = ask_for_number("How many uppercase characters are required?")
    if upper_case_number is None:
        return
    digits_number = ask_for_number("How many digits are required?")
    if digits_number is None:
        return
    symbols_number = ask_for_number("How many symbols are required?")
    if symbols_number is None:
        return


def check_credentials():
    """Function to check if user entered a valid website URL and username/email."""
    website = website_entry.get()
    email = email_entry.get()

    # Regex for a basic URL validation
    url_pattern = re.compile(
        r'^(https?://)?'           
        r'([a-zA-Z0-9_\-]+\.)?'     
        r'[a-zA-Z0-9_\-]+\.[a-zA-Z]{2,}'  
        r'(/[^\s]*)?$'
    )

    if not url_pattern.match(website):
        messagebox.showinfo("Invalid Website", "Please enter a valid website URL.")
        return False

    if not email:
        messagebox.showinfo("Missing Email", "Please enter an email/username.")
        return False

    return True


def create_password():
    """
    Main function to generate password.
    :return:
    """
    global lower_case_number, upper_case_number, digits_number, symbols_number
    # empty the field in case user wants to regenerate the password
    password_entry.delete(0, 'end')

    if check_credentials():
        try:
            new_password = (
                    random.sample(string.ascii_lowercase, k=lower_case_number) +
                    random.sample(string.ascii_uppercase, k=upper_case_number) +
                    random.sample(string.digits, k=digits_number) +
                    random.sample(string.punctuation, k=symbols_number))
        except (TypeError, ValueError):
            sys.exit()
        else:
            random.shuffle(new_password)
            random.shuffle(new_password)
            password_str = ''.join(new_password)
            # insert the generated password into the entry field
            password_entry.insert(0, password_str)


def adding_password():
    """
    Function aiming two goals:
    1. Add the new website, user data and password to the file for storing
    2. Copying the newly generated password to clipboard for immediate use after saving
    :return:
    """
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    date = datetime.datetime.now()
    current_date = date.strftime('%d.%m.%Y')

    new_entry = {
        website: {
            "username": email,
            "password": password,
            "logged_date": current_date
        }
    }
    if check_credentials():
        try:
            with open(DATA_FILE, 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(DATA_FILE, 'w') as data_file:
                json.dump(new_entry, data_file, indent=4)
        else:
            data.update(new_entry)

            with open(DATA_FILE, 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            pyperclip.copy(password_entry.get())
            messagebox.showinfo("Success", "Saved and copied to clipboard")
            password_entry.delete(0, 'end')
            website_entry.delete(4, 'end')


# create main window
window = Tk()
window.title('Password manager')
window.config(padx=20, pady=20, bg='#BEFBFF')

# add icon
image_path = './images/logo_image.png'

ico = Image.open(image_path)
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

# create and setup canvas
canvas = Canvas(
    window,
    bg='#BEFBFF',
    width=400,
    height=400,
    highlightthickness=0
)

filename = PhotoImage(file="images/bg_image.png")
canvas.create_image(225, 230, image=filename)
canvas.create_text(
    220, 30,
    text='Create, save, manage and securely use safe passwords',
    width=360,
    font=(FONT_NAME, 13, 'bold'),
    fill='#281713',
    justify='center'
)
canvas.grid(row=1, column=1)

# add buttons
exit_img = Image.open('images/exit.png')
exit_photo = ImageTk.PhotoImage(exit_img)
exit_button = Button(
    window,
    image=exit_photo,
    bg='#BEFBFF',
    height=30,
    width=65,
    highlightthickness=0,
    command=exit_app,
    anchor='se'
)
exit_button.grid(row=0, column=2, sticky='se')

generate_button = Button(
    window,
    font=FONT_NAME,
    height=1,
    bg='#0089B4',
    fg='#F9E3E2',
    activebackground='#169700',
    activeforeground='#F9E3E2',
    highlightthickness=0,
    text='Generate Password',
    command=create_password,
)
generate_button.grid(row=4, column=2)

search_button = Button(
    window,
    font=FONT_NAME,
    height=1,
    width=15,
    bg='#0089B4',
    fg='#F9E3E2',
    activebackground='#169700',
    activeforeground='#F9E3E2',
    highlightthickness=0,
    text='Search',
    command=search_button_func
)
search_button.grid(row=2, column=2)

special_requirements_button = Button(
    window,
    font=FONT_NAME,
    height=1,
    bg='#C06600',
    fg='#F9E3E2',
    activebackground='#169700',
    activeforeground='#F9E3E2',
    highlightthickness=0,
    text='Requirements',
    command=special_requirements,
)
special_requirements_button.grid(row=0, column=0)

add_button = Button(
    window,
    font=FONT_NAME,
    width=51,
    bg='#0089B4',
    fg='#F9E3E2',
    activebackground='#169700',
    activeforeground='#F9E3E2',
    highlightthickness=0,
    text='Add Password',
    command=adding_password,
)

add_button.grid(row=5, column=1, columnspan=2)

# Labels
website_label = Label(
    window,
    padx=1,
    text='Website:',
    font=(FONT_NAME, 10),
    bg='#BEFBFF',
    fg='#281713',
)

website_label.grid(row=2, column=0)

email_label = Label(
    window,
    padx=1,
    text='Email/Username:',
    font=(FONT_NAME, 10),
    bg='#BEFBFF',
    fg='#281713',
)
email_label.grid(row=3, column=0)

password_label = Label(
    window,
    padx=1,
    text='Password:',
    font=(FONT_NAME, 10),
    bg='#BEFBFF',
    fg='#281713',
)
password_label.grid(row=4, column=0)

# text fields
website_entry = Entry(window, width=35)
website_entry.focus()
website_entry.insert(0, 'www.')
website_entry.grid(row=2, column=1, ipady=3, pady=5)

email_entry = Entry(window, width=52)
email_entry.insert(0, '@')
email_entry.grid(row=3, column=1, columnspan=2, ipady=3, pady=5)

password_entry = Entry(window, width=35)
password_entry.grid(row=4, column=1, ipady=3, pady=5)

window.mainloop()
