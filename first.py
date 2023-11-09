import tkinter as tk
import tkinter.messagebox as msg
from tkinter import *
from tkinter import Label, Button
import time
import datetime
import sqlite3
from ttkthemes import ThemedTk

# Connect to the SQLite database
conn = sqlite3.connect('MemoriesDiary.db')
cursor = conn.cursor()

# Define the student table schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS modiary (
        id INTEGER PRIMARY KEY,
        tdate TEXT,
        message TEXT    
    )
''')

date = ""
message = ""

# Main menu function
def mainmenu():
    mtk = Tk()
    mtk.title("Menu")
    mtk.geometry('200x300')
    mtk.configure(bg="#ffde03")

    # Labels for spacing
    l1 = Label(mtk, bg="#ffde03")
    l2 = Label(mtk, bg="#ffde03")
    l3 = Label(mtk, bg="#ffde03")
    l4 = Label(mtk, bg="#ffde03")
    l5 = Label(mtk, bg="#ffde03")

    # Buttons for diary operations
    Write = Button(mtk, text="Write", width=7, bg="white", fg="brown", font=("monospace", 10), command=diary)
    Read = Button(mtk, text="View", width=7, bg="white", fg="brown", font=("monospace", 10), command=Dread)
    update = Button(mtk, text="Update", width=7, fg="brown", bg="white", font=("monospace", 10), command=Dupdate)
    Delete = Button(mtk, text="Delete", width=7, fg="brown", bg="white", font=("monospace", 10), command=Ddelete)
    Close = Button(mtk, text="Close", width=7, fg="brown", bg="white", font=("monospace", 10), command=mtk.destroy)

    Write.pack()
    l1.pack()
    Read.pack()
    l2.pack()
    Write.pack()
    l3.pack()
    update.pack()
    l4.pack()
    Delete.pack()
    l5.pack()
    Close.pack()
    mtk.mainloop()

# Read (View) function
def Dread():
    Vd = Tk()
    vf = Label(Vd, text="")  # Initialize the label with an empty string
    Vd.geometry('600x600')
    Vd.title("Diary - Written")
    Vd.configure(bg="black")
    cursor.execute("SELECT * FROM modiary")
    students = cursor.fetchall()

    if students:
        text = "\n".join([f"Page No: {student[0]}\nDate: {student[1]}\nMessage: {student[2]}\n" for student in students])
        vf.config(text=text)
    else:
        msg.showinfo("Error", "No records found")

    vf.pack()
    conn.close()
    Vd.mainloop()

# Update function
def Dupdate():
    # Create a tkinter window
    Mv = Tk()
    Mv.title("Update Diary Entry")
    Mv.geometry("300x300")

    # Create a frame to organize widgets
    frame = Frame(Mv)
    frame.pack(padx=10, pady=10)

    Label(frame, text="Page No. :").grid(row=0, column=0, sticky='w')
    Id = Entry(frame, width=25)
    Id.grid(row=0, column=1, padx=(0, 10))

    # Label and Entry for the new date
    Label(frame, text="New Date (dd/mm/yyyy):").grid(row=1, column=0, sticky='w')
    new_date = Entry(frame, width=25)
    new_date.grid(row=1, column=1, padx=(0, 10))

    # Label and Text widget for the new message
    Label(frame, text='Note', font=("courier", 10), fg="black", bg="white").grid(row=2, column=0, sticky='w')
    new_message = Text(frame, width=25, height=10)
    new_message.grid(row=2, column=1, padx=(0, 10))

    def update_entry():
        id1 = Id.get()
        new_date1 = new_date.get()
        new_message1 = new_message.get("1.0", "end-1c")  # Get the text from the Text widget
        cursor.execute(f"UPDATE modiary SET tdate = '{new_date1}', message = '{new_message1}' WHERE id = {id1}")
        conn.commit()
        if cursor.rowcount > 0:
            msg.showinfo("Success", "Record updated successfully!")
        else:
            msg.showinfo("Failed", "Update was unsuccessful")

    # Button to trigger the update
    update_button = Button(frame, text="Update Entry", command=update_entry)
    update_button.grid(row=3, columnspan=2)
    close = Button(Mv, text="Close", command=Mv.destroy, width=7, bg="red", fg="white", font=("monospace", 10))
    close.pack(side=BOTTOM, anchor='se')
    Mv.mainloop()

# Delete function
def Ddelete():
    Mv = Tk()
    Mv.title("Erase the day")
    frame = Frame(Mv, bg="black")
    frame.pack(padx=10, pady=10)
    Lab = Label(Mv, text="Erase the memory")
    Label(frame, text="Page No. :").grid(row=0, column=0, sticky='w')
    Id = Entry(frame, width=25)
    Id.grid(row=0, column=1, padx=(0, 10))

    def rgb_hack(rgb):
        return "#%02x%02x%02x" % rgb
    Mv.config(bg=rgb_hack((0, 0, 0)))

    def Remove():
        id1 = Id.get()
        cursor.execute(f"DELETE FROM modiary WHERE id = {id1}")
        conn.commit()
        if cursor.rowcount > 0:
            msg.showinfo("Success", "Memory Removed Successfully!")
        else:
            msg.showinfo("Failed", "Unsuccessful")

    Remove = Button(frame, text="Remove", command=Remove)
    Remove.grid(row=3, columnspan=2)

# Diary label window (Writing)
def diary():
    tk1 = Tk()
    tk1.title("Diary")
    tk1.geometry('600x450')
    tk1.configure(bg="black")
    tk1.configure(borderwidth=5)

    # Get the current date
    def dat():
        x = datetime.datetime.now()
        Day = x.strftime("%A - %d/%m/%Y")
        D.config(text=Day)

    D = Label(tk1, font=("cosmos", 10, "bold"), bg="black", fg="white")
    D.pack(side=TOP, anchor='se')
    dat()

    # Page number
    cursor.execute("SELECT * FROM modiary")
    students = cursor.fetchall()
    vf = Label(tk1, font=("cosmos", 10, "bold"), bg="black", fg="white")
    if students:
        for student in students:
            vf.config(text="Last page No: " + str(student[0]))
    else:
        msg.showinfo("Error", "No records found")

    vf.pack(side=TOP, anchor='se')

    # Create and pack labels and input fields
    Label(tk1, text="Write down your Memories", font=("courier", 12), fg="black", bg="white").pack()
    frame = Frame(tk1)
    frame.pack(padx=10, pady=10)

    Label(frame, text="Enter the Date (dd/mm/yyyy):", font=("courier", 10), fg="black", bg="white").grid(row=1, column=0, sticky='w')
    Dintput = Entry(frame, width=25)
    Dintput.grid(row=1, column=1, padx=(0, 10))

    Label(frame, text='').grid(row=1, column=0, sticky='w')
    Label(frame, text='Note', font=("courier", 10), fg="black", bg="white").grid(row=2, column=0, sticky='w')
    Dnote = Text(frame, width=25, height=10)
    Dnote.grid(row=2, column=1, padx=(0, 10))

    Label(frame, text='Page No.:', font=("courier", 10), fg="black", bg="white").grid(row=0, column=0, sticky='w')
    pg = Entry(frame, width=25)
    pg.grid(row=0, column=1, padx=(0, 10))

    close = Button(tk1, text="Close", command=tk1.destroy, width=7, bg="brown", fg="white", font=("monospace", 10))
    close.pack(side=BOTTOM, anchor='se')

    back = Button(tk1, text="Back", command=mainmenu, width=7, bg="BLACK", fg="white", font=("monospace", 10))
    back.pack(side=LEFT, anchor='nw')

    # Submit function to add a diary entry
    def submit():
        Id = pg.get()
        date = Dintput.get()
        message = Dnote.get("1.0", "end-1c")  # Get the text from the Text widget

        # Connect to the database
        conn = sqlite3.connect('MemoriesDiary.db')
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute(f"INSERT INTO modiary (id, tdate, message) VALUES ({Id}, '{date}', '{message}')")
        conn.commit()

        # Check if the insert was successful
        if cursor.rowcount > 0:
            msg.showinfo("Success", "Memory Recorded Successfully!")
            msg.showinfo("Written in", date)
        else:
            msg.showinfo("Failed", "Unsuccessful")

        # Close the database connection
        conn.close()

    Submit = Button(tk1, text="Submit", width=7, bg="green", fg="white", font=("monospace", 10), command=submit)
    Submit.pack(side="bottom")

    tk1.mainloop()

# About function
def about():
    tk2 = Tk()
    tk2.geometry('200x200')
    tk2.configure(borderwidth=7)
    lab = Label(tk2, text="About the author")
    lab1 = Label(tk2, text="Passionate in program language")
    lab2 = Label(tk2, text="Digital Diary - Note your days in a secured way")
    lab3 = Label(tk2, text="am_not_a_scientist")
    btn = Button(tk2, text='Close', command=tk2.destroy)  # Use tk1.destroy to close the about window
    lab.pack()
    lab1.pack()
    lab2.pack()
    lab3.pack()
    btn.pack()
    tk2.mainloop()

# Back function
def back():
    tk1.destroy()
    main()

# Main function
def main():
    root = Tk()
    root.geometry('300x300')
    root.title("Digital Diary")
    l1 = Label(root, text="", fg="black", bg="black")
    l2 = Label(root, text="", fg="black", bg="black")
    l3 = Label(root, text="", fg="black", bg="black")
    L = Label(root, text="D i a r y", fg="white", bg="black", font=("Times New Roman", 20))
    L.pack()
    l1.pack()
    button = Button(root, text="Open diary", command=mainmenu, font=("monospace"), width=10)
    abt_btn = Button(root, text="About_author", command=about, font=("monospace"), width=10)
    close = Button(root, text="Close", command=root.destroy, font=("monospace"), width=10)
    button.pack()
    l2.pack()
    abt_btn.pack()
    l3.pack()
    close.pack()
    
    def tick():
        time2 = time.strftime("%I:%M:%S:%p")
        clock.config(text=time2)
        clock.after(200, tick)
    clock = Label(root, font=("cosmos", 10, "bold"), bg="black", fg="white")
    tick()

    def dat():
        x = datetime.datetime.now()
        Day = x.strftime("%A - %d/%m/%Y")
        D.config(text=Day)
    D = Label(root, font=("cosmos", 10, "bold"), bg="black", fg="white")
    clock.pack()
    D.pack()
    dat()

    def rgb_hack(rgb):
        return "#%02x%02x%02x" % rgb
    root.config(bg=rgb_hack((0, 0, 0)))
    root.mainloop()


def intro():
    window = Tk()
    window.title("Login form")
    window.geometry('340x440')
    window.configure(bg='#333333')

    def login():
        username = "amnot"
        password = "2428"
        if username_entry.get() == username and password_entry.get() == password:
            msg.showinfo(title="Login Success", message="You have successfully logged in.")
            main()
        else:
            msg.showerror(title="Error", message="Invalid login.")

    frame = Frame(bg='#333333')

    # Creating widgets
    login_label = Label(
        frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
    username_label = Label(
        frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username_entry = Entry(frame, font=("Arial", 16))
    password_entry = Entry(frame, show="*", font=("Arial", 16))
    password_label = Label(
        frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    login_button = Button(
        frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

    # Placing widgets on the screen
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    frame.pack()

    window.mainloop()


if __name__ == "__main__":
    intro()
    cursor.close()
    conn.close()
