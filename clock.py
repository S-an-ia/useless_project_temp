import tkinter as tk
from datetime import datetime

root = tk.Tk()

root.title("Useless Alarm Clock")
root.geometry("600x400")
root.configure(bg="#111111")


# ---------------- PAGE 1 : CLOCK ----------------

clock_page = tk.Frame(root, bg="#111111")
clock_page.pack(fill="both", expand=True)


def update_clock():
    current_time = datetime.now()

    time_text = current_time.strftime("%I:%M:%S %p")
    date_text = current_time.strftime("%A, %d %B %Y")

    clock_label.config(text=time_text)
    date_label.config(text=date_text)

    root.after(1000, update_clock)


clock_label = tk.Label(
    clock_page,
    text="00:00:00",
    font=("Arial", 50, "bold"),
    bg="#111111",
    fg="white"
)
clock_label.pack(pady=(70, 10))


date_label = tk.Label(
    clock_page,
    text="",
    font=("Arial", 16),
    bg="#111111",
    fg="white"
)
date_label.pack()


def open_alarm_page():
    clock_page.pack_forget()
    alarm_page.pack(fill="both", expand=True)


set_alarm_button = tk.Button(
    clock_page,
    text="SET ALARM",
    font=("Arial", 14, "bold"),
    command=open_alarm_page
)
set_alarm_button.pack(pady=40)


# ---------------- PAGE 2 : SET ALARM ----------------

alarm_page = tk.Frame(root, bg="#111111")


title = tk.Label(
    alarm_page,
    text="⏰ SET YOUR ALARM",
    font=("Arial", 25, "bold"),
    bg="#111111",
    fg="white"
)
title.pack(pady=(60, 30))


instruction = tk.Label(
    alarm_page,
    text="Wanna wake up? \n DO THE MATH",
    font=("Arial", 15),
    bg="#111111",
    fg="white"
)
instruction.pack(pady=10)


time_entry = tk.Entry(
    alarm_page,
    font=("Arial", 20),
    justify="center"
)
time_entry.pack(pady=15)

time_entry.insert(0, "08:00 AM")


def set_alarm():
    alarm_time = time_entry.get()

    print("Alarm set for:", alarm_time)

    confirmation.config(
        text=f"Alarm set for {alarm_time}!"
    )


set_button = tk.Button(
    alarm_page,
    text="SET ALARM",
    font=("Arial", 14, "bold"),
    command=set_alarm
)
set_button.pack(pady=15)


confirmation = tk.Label(
    alarm_page,
    text="",
    font=("Arial", 13),
    bg="#111111",
    fg="white"
)
confirmation.pack(pady=10)


def back_to_clock():
    alarm_page.pack_forget()
    clock_page.pack(fill="both", expand=True)


back_button = tk.Button(
    alarm_page,
    text="← BACK",
    font=("Arial", 12),
    command=back_to_clock
)
back_button.pack(pady=20)


# Start the clock
update_clock()

root.mainloop()