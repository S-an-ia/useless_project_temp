import tkinter as tk
from datetime import datetime
import winsound

root = tk.Tk()

root.title("Useless Alarm Clock")
root.geometry("600x400")
root.configure(bg="#111111")

snooze_count = 0
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





seconds_entry = tk.Entry(
    alarm_page,
    font=("Arial", 20),
    justify="center"
)
seconds_entry.pack(pady=15)

def alarm_ringing():
    alarm_page.pack_forget()
    clock_page.pack_forget()

    ringing_page.pack(fill="both", expand=True)

    if snooze_count > 5:
        ringing_title.config(
            text="⏰ I'M DONE"
        )
    else:
        ringing_title.config(
            text="⏰ WAKE UP!!!"
        )

    winsound.Beep(1000, 1000)
def set_alarm():
    try:
        seconds = int(seconds_entry.get())

        if seconds <= 0:
            confirmation.config(
                text="Enter a positive number!"
            )
            return

        confirmation.config(
            text=f"Alarm set for {seconds} seconds!"
        )

        root.after(seconds * 1000, alarm_ringing)

    except ValueError:
        confirmation.config(
            text="Please enter seconds only!"
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

# ---------------- PAGE 3 : ALARM RINGING ----------------

ringing_page = tk.Frame(root, bg="#111111")

ringing_title = tk.Label(
    ringing_page,
    text="⏰ WAKE UP!!!",
    font=("Arial", 40, "bold"),
    bg="#111111",
    fg="white"
)
ringing_title.pack(pady=(80, 20))


ringing_message = tk.Label(
    ringing_page,
    text="YOUR ALARM IS RINGING",
    font=("Arial", 18),
    bg="#111111",
    fg="white"
)
ringing_message.pack(pady=10)


# This is the ACTUAL snooze function
def actual_snooze():
    global snooze_count

    snooze_count += 1

    winsound.PlaySound(None, winsound.SND_PURGE)

    if snooze_count == 1:
        message = "SIKE YOU SNOOZED HEHE"

    elif snooze_count == 2:
        message = "Okay I'll dismiss next time"

    elif snooze_count == 3:
        message = "Next time for sure"

    elif snooze_count == 4:
        message = "Get Up Plis"

    else:
        message = "ACHIEVEMENT UNLOCKED!! \n SUCCESSFULLY DISAPPOINTED THE ENTIRE BLOODLINE"

    ringing_message.config(text=message)

    root.after(5000, alarm_ringing)


# This is the ACTUAL dismiss function
def actual_dismiss():
    winsound.PlaySound(None, winsound.SND_PURGE)

    ringing_message.config(
        text="ALARM DEFEATED \n YOU WIN!!"
    )

    root.after(1500, go_to_clock)


# SWAPPED BUTTONS
dismiss_button = tk.Button(
    ringing_page,
    text="DISMISS",
    font=("Arial", 16, "bold"),
    command=actual_snooze
)
dismiss_button.pack(pady=15)


snooze_button = tk.Button(
    ringing_page,
    text="SNOOZE",
    font=("Arial", 16, "bold"),
    command=actual_dismiss
)
snooze_button.pack(pady=15)

def back_to_clock():
    alarm_page.pack_forget()
    clock_page.pack(fill="both", expand=True)

def go_to_clock():
    ringing_page.pack_forget()
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