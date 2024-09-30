from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)

    # Insert the generated password into the Passwordtext field
    Passwordtext.delete(0, END)
    Passwordtext.insert(0, password)

    # Copy the generated password to the clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add():
    Website = Websitetext.get()
    User = Usertext.get()
    Password = Passwordtext.get()
    new_data = {
        Website: {
            "email": User,
            "password": Password
        }
    }

    if len(Website) == 0 or len(Password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            # Attempt to open and load the existing data from the JSON file
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            Websitetext.delete(0, END)
            Passwordtext.delete(0, END)

# ---------------------------- Find Password ------------------------------- #
def find_password():
    website = Websitetext.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            print(data)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message= f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} exists.")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
lockImage = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lockImage)
canvas.grid(column=1, row=0)

Websitelabel = Label(text="Website: ")
Websitelabel.grid(column=0, row=1)

Userlabel = Label(text="Username/Email: ")
Userlabel.grid(column=0, row=2)

Passwordlabel = Label(text="Password: ")
Passwordlabel.grid(column=0, row=3)

Websitetext = Entry(width=35)
Websitetext.grid(column=1, row=1)
Websitetext.focus()

Usertext = Entry(width=35)
Usertext.grid(column=1, row=2, columnspan=2)
Usertext.insert(0, "diddy@gmail.com")

Passwordtext = Entry(width=21)
Passwordtext.grid(column=1, row=3)

Genbutton = Button(text="Generate Password", command=generate_password)
Genbutton.grid(column=2, row=3)

Addbutton = Button(text="Add", width=36, command=add)
Addbutton.grid(column=1, row=4, columnspan=2)

SearchButton = Button(text="Search", width=13, command=find_password)
SearchButton.grid(column=2, row=1)

window.mainloop()
