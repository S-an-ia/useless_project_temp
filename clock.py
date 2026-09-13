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
    text="Wanna wake up? \n ENTER SECONDS",
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

    if snooze_count == 0:
        ringing_title.config(
            text="⏰ RISE AND SHINE PRINCESS"
        )
        winsound.PlaySound("Alarm Beeps.wav",winsound.SND_FILENAME | winsound.SND_ASYNC)

    elif snooze_count == 1:
        ringing_title.config(
            text="SIKE YOU SNOOZED HEHE"
        )
        winsound.PlaySound("Alarm Beeps.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    elif snooze_count == 2:
        ringing_title.config(
            text="Okay I'll dismiss next time"
        )
        winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    elif snooze_count == 3:
        ringing_title.config(
            text="Next time for sure"

        )
        winsound.PlaySound("Alarm Clock.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    elif snooze_count == 4:
        ringing_title.config(
            text="Get Up Plis"
        )
        winsound.PlaySound("Trumpets.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    else:
        ringing_title.config(
            text="ACHIEVEMENT UNLOCKED!! \n SUCCESSFULLY DISAPPOINTED THE ENTIRE BLOODLINE"
        )
        winsound.PlaySound("Loud alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
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
    text="⏰ RISE AND SHINE PRINCESS",
    font=("Arial", 40, "bold"),
    bg="#111111",
    fg="white"
)
ringing_title.pack(pady=(80, 20))





# This is the ACTUAL snooze function
def actual_snooze():
    global snooze_count

    snooze_count += 1

    winsound.PlaySound(None, winsound.SND_PURGE)




    root.after(2000, alarm_ringing)


# This is the ACTUAL dismiss function
# This is the ACTUAL dismiss function
# This is the ACTUAL dismiss function
def actual_dismiss():
    math_page = tk.Toplevel(root)
    math_page.title("PROVE IT")
    math_page.geometry("500x350")
    math_page.configure(bg="#111111")

    # Difficulty increases with snooze count
    if snooze_count == 0:
        question_text = "What is 7 + 4?"
        options = ["9", "10", "11", "12"]
        answer = "11"

    elif snooze_count == 1:
        question_text = "How many pigeons are needed to carry a refrigerator?"
        options = ["3", "17", "42", "Obviously 900"]
        answer = "42"

    elif snooze_count == 2:
        question_text = "What is the emotional temperature of a confused spoon?"
        options = ["37°C", "Tuesday", "42°C", "Cold"]
        answer = "42°C"

    elif snooze_count == 3:
        question_text = "How many bananas fit inside the concept of Tuesday?"
        options = ["7", "∞", "Tuesday bananas", "None"]
        answer = "∞"

    elif snooze_count == 4:
        question_text = "What is the GPA of a mosquito that never attended college?"
        options = ["0.0", "4.0", "69.0", "It dropped out"]
        answer = "It dropped out"

    else:
        question_text = "What is the square root of your current regret?"
        options = ["2", "7", "69", "Yes"]
        answer = "Yes"

    question = tk.Label(
        math_page,
        text=question_text,
        font=("Arial", 17, "bold"),
        bg="#111111",
        fg="white",
        wraplength=450,
        justify="center"
    )
    question.pack(pady=20)



    selected_answer = tk.StringVar(value="")

    option_circles = {}

    def select_option(value):
        selected_answer.set(value)

        # Reset all circles
        for circle in option_circles.values():
            circle.config(text="○")

        # Fill selected circle
        option_circles[value].config(text="●")

    for option in options:
        option_frame = tk.Frame(
            math_page,
            bg="#111111"
        )
        option_frame.pack(anchor="center", pady=3)

        circle = tk.Label(
            option_frame,
            text="○",
            font=("Arial", 18),
            bg="#111111",
            fg="white"
        )
        circle.pack(side="left")

        option_label = tk.Label(
            option_frame,
            text=option,
            font=("Arial", 14),
            bg="#111111",
            fg="white"
        )
        option_label.pack(side="left", padx=5)

        option_circles[option] = circle

        circle.bind(
            "<Button-1>",
            lambda event, value=option: select_option(value)
        )

        option_label.bind(
            "<Button-1>",
            lambda event, value=option: select_option(value)
        )

        option_frame.bind(
            "<Button-1>",
            lambda event, value=option: select_option(value)
        )

    def check_answer():
        global snooze_count

        user_answer = selected_answer.get()

        if user_answer == answer:

            math_page.destroy()

            winsound.PlaySound(
                None,
                winsound.SND_PURGE
            )

            ringing_title.config(
                font=("Arial", 25, "bold"),
                text="CORRECT.\n\n"
                     "We have absolutely no idea why."
            )

            root.after(2000, show_sleep_report)

        else:

            math_page.destroy()

            snooze_count += 1

            winsound.PlaySound(
                None,
                winsound.SND_PURGE
            )
            dismiss_button.pack_forget()
            snooze_button.pack_forget()

            if snooze_count == 1:

                message = (
                    "INCORRECT.\n\n"
                    "LOL LOSER"
                )

            elif snooze_count == 2:

                message = (
                    "INCORRECT.\n\n"
                    "We made the question.\n"
                    "We still don't know."
                )

            elif snooze_count == 3:

                message = (
                    "INCORRECT.\n\n"
                    "The answer has been\n"
                    "classified as confidential."
                )

            else:

                message = (
                    "INCORRECT.\n\n"
                    "At this point, nobody knows.\n"
                    "Including the alarm."
                )

            ringing_title.config(
                font=("Arial", 25, "bold"),
                text=message
            )

            root.after(3000, alarm_ringing)

    submit_button = tk.Button(
        math_page,
        text="SUBMIT",
        font=("Arial", 14, "bold"),
        command=check_answer
    )
    submit_button.pack(pady=10)

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



# ---------------- FINAL SLEEP REPORT ----------------

def show_sleep_report():

    # Remove the old buttons
    for widget in ringing_page.winfo_children():
        if widget != ringing_title:
            widget.destroy()

    bloodline = min(100, snooze_count * 17 + 5)
    productivity = max(0, 100 - snooze_count * 13)

    filled = productivity // 5
    empty = 20 - filled

    ringing_title.config(
        font=("Arial", 16, "bold"),
        text=f"📊 YOUR SLEEP REPORT\n\n"
             f"Snoozes: {snooze_count}   "
             f"Math Problems: {snooze_count + 1}\n"
             f"Wrong Answers: {snooze_count}\n"
             f"Brain Cells Used: {max(1, 10 - snooze_count)}\n"
             f"Bloodline Disappointment: {bloodline}%\n\n"
             f"PRODUCTIVITY\n"
             f"[{'█' * filled}{'░' * empty}] "
             f"{productivity}%\n\n"
             f"Scientific Significance: NONE"
    )

    awake_button = tk.Button(
        ringing_page,
        text="I'M AWAKE",
        font=("Arial", 14, "bold"),
        command=finish_alarm
    )
    awake_button.pack(pady=10)


# ---------------- FINISH ALARM ----------------


def finish_alarm():
    global snooze_count

    snooze_count = 0

    for widget in ringing_page.winfo_children():
        if widget != ringing_title:
            widget.destroy()

    ringing_page.pack_forget()
    clock_page.pack(fill="both", expand=True)

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