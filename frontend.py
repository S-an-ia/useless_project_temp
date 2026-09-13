import os
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageDraw, ImageTk
import winsound


# ============================================================
# CONFIG & DYNAMIC ASSET REGISTRY
# ============================================================

W, H = 1280, 720

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def find_image(name_keywords):
    """
    Dynamically search local images directory and project root for an image matching
    any of the provided name keywords. Allows adding new pictures anytime!
    """
    search_dirs = [IMAGES_DIR, BASE_DIR, r"C:\SANIN\Images"]
    for s_dir in search_dirs:
        if not os.path.exists(s_dir):
            continue
        try:
            files = os.listdir(s_dir)
        except Exception:
            continue
        for kw in name_keywords:
            for f in files:
                fname, ext = os.path.splitext(f.lower())
                if ext in ('.jpg', '.jpeg', '.png', '.avif', '.webp') and kw.lower() in fname:
                    return os.path.join(s_dir, f)
    return None


def get_image_path(filename, fallback_path):
    local_path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(local_path):
        return local_path
    found = find_image([os.path.splitext(filename)[0]])
    if found:
        return found
    return fallback_path


def get_sound_path(filename):
    local_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(local_path):
        return local_path
    return filename


HOME_IMAGE_PATH = get_image_path("home.jpg", r"C:\SANIN\Images\home.jpg")
BASE_IMAGE_PATH = get_image_path("base.png", r"C:\SANIN\Images\base.png")
TIME_IMAGE_PATH = get_image_path("time.jpg", r"C:\SANIN\Images\time.jpg")

# PAGE 3 IMAGES
CLOCK_IMAGE_PATH = get_image_path("CLOCK.png", r"C:\SANIN\Images\CLOCK.png")
RING_IMAGE_PATH = get_image_path("RING.jpg", r"C:\SANIN\Images\RING.jpg")


# ============================================================
# PAGE 1 GEOMETRY
# ============================================================

CIRCLE_CX_FRAC = 0.2077
CIRCLE_CY_FRAC = 0.3409
CIRCLE_R_FRAC = 0.1518

TEXT_X_FRAC = 0.2125
TEXT_LINE1_Y_FRAC = 0.2983
TEXT_LINE2_Y_FRAC = 0.3849

FONT_SIZE_FRAC = 0.0649

BTN_LEFT_FRAC = 0.0671
BTN_RIGHT_FRAC = 0.3738
BTN_TOP_FRAC = 0.6619
BTN_BOTTOM_FRAC = 0.7813


# ============================================================
# PAGE 1 COLORS
# ============================================================

BTN_NORMAL = "#c3dff5"
BTN_HOVER = "#c4c4c4"
BTN_PRESSED = "#3c3c3c"

BTN_TEXT_LIGHT = "#141414"
BTN_TEXT_DARK = "#e8e8e8"

CIRCLE_COLOR_TOP = (160, 238, 248, 191)
CIRCLE_COLOR_BOTTOM = (218, 222, 214, 191)


# ============================================================
# IMAGE HELPERS
# ============================================================

def load_cover_image(path, w, h):
    """
    Resize an image to cover the whole canvas
    without distortion. Excess is cropped.
    """

    img = Image.open(path).convert("RGB")

    src_ratio = img.width / img.height
    dst_ratio = w / h

    if src_ratio > dst_ratio:
        new_h = h
        new_w = int(new_h * src_ratio)
    else:
        new_w = w
        new_h = int(new_w / src_ratio)

    img = img.resize(
        (new_w, new_h),
        Image.LANCZOS
    )

    left = (new_w - w) // 2
    top = (new_h - h) // 2

    img = img.crop(
        (left, top, left + w, top + h)
    )

    return img


def make_circle(diameter):

    img = Image.new(
        "RGBA",
        (diameter, diameter),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(img)

    for y in range(diameter):

        t = y / diameter

        r = int(
            CIRCLE_COLOR_TOP[0]
            +
            (
                CIRCLE_COLOR_BOTTOM[0]
                -
                CIRCLE_COLOR_TOP[0]
            ) * t
        )

        g = int(
            CIRCLE_COLOR_TOP[1]
            +
            (
                CIRCLE_COLOR_BOTTOM[1]
                -
                CIRCLE_COLOR_TOP[1]
            ) * t
        )

        b = int(
            CIRCLE_COLOR_TOP[2]
            +
            (
                CIRCLE_COLOR_BOTTOM[2]
                -
                CIRCLE_COLOR_TOP[2]
            ) * t
        )

        a = int(
            CIRCLE_COLOR_TOP[3]
            +
            (
                CIRCLE_COLOR_BOTTOM[3]
                -
                CIRCLE_COLOR_TOP[3]
            ) * t
        )

        draw.line(
            [(0, y), (diameter, y)],
            fill=(r, g, b, a)
        )

    mask = Image.new(
        "L",
        (diameter, diameter),
        0
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse(
        (0, 0, diameter - 1, diameter - 1),
        fill=255
    )

    img.putalpha(mask)

    return img


def make_rounded_image(
    path,
    width,
    height,
    radius
):

    original = Image.open(path).convert("RGB")

    src_ratio = original.width / original.height
    dst_ratio = width / height

    if src_ratio > dst_ratio:

        new_height = height
        new_width = int(
            new_height * src_ratio
        )

    else:

        new_width = width
        new_height = int(
            new_width / src_ratio
        )

    original = original.resize(
        (new_width, new_height),
        Image.LANCZOS
    )

    left = (new_width - width) // 2
    top = (new_height - height) // 2

    original = original.crop(
        (
            left,
            top,
            left + width,
            top + height
        )
    )

    result = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    mask = Image.new(
        "L",
        (width, height),
        0
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.rounded_rectangle(
        (
            0,
            0,
            width - 1,
            height - 1
        ),
        radius=radius,
        fill=255
    )

    result.paste(
        original,
        (0, 0),
        mask
    )

    return result


# ============================================================
# MAIN APPLICATION
# ============================================================

class AlarmPanel(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Alarm")

        self.geometry(
            f"{W}x{H}"
        )

        self.resizable(
            False,
            False
        )

        # ----------------------------------------------------
        # ALARM VARIABLES
        # ----------------------------------------------------

        self.alarm_seconds = 0
        self.remaining_seconds = 0
        self.alarm_running = False
        self.alarm_job = None
        self.snooze_count = 0
        self.awake_button = None
        self._bg_cache = {}

        # ----------------------------------------------------
        # MAIN CONTAINER
        # ----------------------------------------------------

        self.container = tk.Frame(
            self,
            width=W,
            height=H
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.container.pack_propagate(False)

        # ----------------------------------------------------
        # PAGES
        # ----------------------------------------------------

        self.page1 = tk.Frame(
            self.container,
            width=W,
            height=H
        )

        self.page2 = tk.Frame(
            self.container,
            width=W,
            height=H
        )

        self.page3 = tk.Frame(
            self.container,
            width=W,
            height=H
        )

        self.page1.place(
            x=0,
            y=0,
            width=W,
            height=H
        )

        self.page2.place(
            x=0,
            y=0,
            width=W,
            height=H
        )

        self.page3.place(
            x=0,
            y=0,
            width=W,
            height=H
        )

        # ----------------------------------------------------
        # BUILD PAGES
        # ----------------------------------------------------

        self.build_page1()
        self.build_page2()
        self.build_page3()

        # Start on Page 1
        self.show_page1()


    # ========================================================
    # PAGE 1
    # ========================================================

    def build_page1(self):

        self.canvas1 = tk.Canvas(
            self.page1,
            width=W,
            height=H,
            highlightthickness=0,
            bd=0
        )

        self.canvas1.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        if not os.path.exists(
            HOME_IMAGE_PATH
        ):

            raise FileNotFoundError(
                f"Home image not found:\n"
                f"{HOME_IMAGE_PATH}"
            )

        bg = load_cover_image(
            HOME_IMAGE_PATH,
            W,
            H
        )

        self.page1_bg = ImageTk.PhotoImage(
            bg
        )

        self.canvas1.create_image(
            0,
            0,
            image=self.page1_bg,
            anchor="nw"
        )

        # ----------------------------------------------------
        # CLOCK CIRCLE
        # ----------------------------------------------------

        radius = CIRCLE_R_FRAC * W

        diameter = int(
            round(radius * 2)
        )

        cx = CIRCLE_CX_FRAC * W
        cy = CIRCLE_CY_FRAC * H

        circle = make_circle(
            diameter
        )

        self.circle_photo = ImageTk.PhotoImage(
            circle
        )

        self.canvas1.create_image(
            int(round(cx - radius)),
            int(round(cy - radius)),
            image=self.circle_photo,
            anchor="nw"
        )

        # ----------------------------------------------------
        # CURRENT TIME
        # ----------------------------------------------------

        self.time_text = self.canvas1.create_text(
            TEXT_X_FRAC * W,
            TEXT_LINE1_Y_FRAC * H,
            text="00 : 00 : 00",
            font=(
                "Segoe UI",
                max(
                    8,
                    int(
                        round(
                            H * FONT_SIZE_FRAC
                        )
                    )
                )
            ),
            fill="#141414",
            anchor="center"
        )

        # ----------------------------------------------------
        # DAY
        # ----------------------------------------------------

        self.day_text = self.canvas1.create_text(
            TEXT_X_FRAC * W,
            TEXT_LINE2_Y_FRAC * H,
            text="(day)",
            font=(
                "Segoe UI",
                max(
                    8,
                    int(
                        round(
                            H * FONT_SIZE_FRAC
                        )
                    )
                )
            ),
            fill="#141414",
            anchor="center"
        )

        # Start live clock
        self.update_clock()

        # ----------------------------------------------------
        # SET ALARM BUTTON
        # ----------------------------------------------------

        x0 = int(
            round(
                BTN_LEFT_FRAC * W
            )
        )

        x1 = int(
            round(
                BTN_RIGHT_FRAC * W
            )
        )

        y0 = int(
            round(
                BTN_TOP_FRAC * H
            )
        )

        y1 = int(
            round(
                BTN_BOTTOM_FRAC * H
            )
        )

        btn_w = x1 - x0
        btn_h = y1 - y0

        radius = btn_h // 2

        self.btn_w = btn_w
        self.btn_h = btn_h

        self.btn_x0 = x0
        self.btn_y0 = y0

        # ----------------------------------------------------
        # BUTTON STATES
        # ----------------------------------------------------

        self.btn_images = {}

        for state, color, text_color in [

            (
                "normal",
                BTN_NORMAL,
                BTN_TEXT_LIGHT
            ),

            (
                "hover",
                BTN_HOVER,
                BTN_TEXT_LIGHT
            ),

            (
                "pressed",
                BTN_PRESSED,
                BTN_TEXT_DARK
            )

        ]:

            img = Image.new(
                "RGBA",
                (btn_w, btn_h),
                (0, 0, 0, 0)
            )

            draw = ImageDraw.Draw(img)

            draw.rounded_rectangle(
                (
                    0,
                    0,
                    btn_w - 1,
                    btn_h - 1
                ),
                radius=radius,
                fill=color
            )

            photo = ImageTk.PhotoImage(
                img
            )

            self.btn_images[state] = (
                photo,
                text_color
            )

        # ----------------------------------------------------
        # NORMAL BUTTON
        # ----------------------------------------------------

        normal_photo, text_color = (
            self.btn_images["normal"]
        )

        self.btn_image_id = self.canvas1.create_image(
            x0,
            y0,
            image=normal_photo,
            anchor="nw"
        )

        self.btn_text_id = self.canvas1.create_text(
            x0 + btn_w / 2,
            y0 + btn_h / 2,
            text="set alarm",
            font=(
                "Segoe UI",
                max(
                    8,
                    int(
                        round(
                            H * FONT_SIZE_FRAC
                        )
                    )
                )
            ),
            fill=text_color,
            anchor="center"
        )

        # ----------------------------------------------------
        # BUTTON EVENTS
        # ----------------------------------------------------

        for item in (
            self.btn_image_id,
            self.btn_text_id
        ):

            self.canvas1.tag_bind(
                item,
                "<Enter>",
                self.button_enter
            )

            self.canvas1.tag_bind(
                item,
                "<Leave>",
                self.button_leave
            )

            self.canvas1.tag_bind(
                item,
                "<ButtonPress-1>",
                self.button_press
            )

            self.canvas1.tag_bind(
                item,
                "<ButtonRelease-1>",
                self.button_release
            )


    # ========================================================
    # CLOCK
    # ========================================================

    def update_clock(self):

        now = datetime.now()

        current_time = now.strftime(
            "%I : %M : %S"
        )

        current_day = now.strftime(
            "(%A)"
        )

        self.canvas1.itemconfig(
            self.time_text,
            text=current_time
        )

        self.canvas1.itemconfig(
            self.day_text,
            text=current_day
        )

        self.after(
            1000,
            self.update_clock
        )


    # ========================================================
    # PAGE 1 BUTTON STATES
    # ========================================================

    def set_button_state(self, state):

        photo, text_color = (
            self.btn_images[state]
        )

        self.canvas1.itemconfig(
            self.btn_image_id,
            image=photo
        )

        self.canvas1.itemconfig(
            self.btn_text_id,
            fill=text_color
        )


    def button_enter(self, event):

        self.set_button_state(
            "hover"
        )


    def button_leave(self, event):

        self.set_button_state(
            "normal"
        )


    def button_press(self, event):

        self.set_button_state(
            "pressed"
        )


    def button_release(self, event):

        x = event.x
        y = event.y

        inside = (
            self.btn_x0 <= x <=
            self.btn_x0 + self.btn_w
            and
            self.btn_y0 <= y <=
            self.btn_y0 + self.btn_h
        )

        if inside:

            self.set_button_state(
                "hover"
            )

            # Go to Page 2
            self.show_page2()

        else:

            self.set_button_state(
                "normal"
            )


    # ========================================================
    # PAGE 2
    # ========================================================

    def build_page2(self):

        self.canvas2 = tk.Canvas(
            self.page2,
            width=W,
            height=H,
            highlightthickness=0,
            bd=0
        )

        self.canvas2.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # BASE BACKGROUND
        # ----------------------------------------------------

        if not os.path.exists(
            BASE_IMAGE_PATH
        ):

            raise FileNotFoundError(
                f"Base image not found:\n"
                f"{BASE_IMAGE_PATH}"
            )

        base = load_cover_image(
            BASE_IMAGE_PATH,
            W,
            H
        )

        self.page2_bg = ImageTk.PhotoImage(
            base
        )

        self.canvas2.create_image(
            0,
            0,
            image=self.page2_bg,
            anchor="nw"
        )

        # ----------------------------------------------------
        # BACK BUTTON
        # ----------------------------------------------------

        self.back_id = self.canvas2.create_text(
            55,
            50,
            text="↩",
            font=(
                "Segoe UI",
                34
            ),
            fill="black",
            anchor="center",
            tags="back"
        )

        self.canvas2.tag_bind(
            self.back_id,
            "<Button-1>",
            lambda event: self.show_page1()
        )

        # ----------------------------------------------------
        # TIME IMAGE
        # ----------------------------------------------------

        card_w = 735
        card_h = 415

        card_x = 600
        card_y = 360

        time_image = make_rounded_image(
            TIME_IMAGE_PATH,
            card_w,
            card_h,
            40
        )

        self.time_photo = ImageTk.PhotoImage(
            time_image
        )

        self.time_image_id = self.canvas2.create_image(
            card_x,
            card_y,
            image=self.time_photo,
            anchor="center"
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.title1_id = self.canvas2.create_text(
            W / 2,
            60,
            text="Set Alarm",
            font=(
                "Segoe UI",
                40
            ),
            fill="black",
            anchor="center"
        )

        self.title3_id = self.canvas2.create_text(
            W / 2,
            180,
            text="WANNA WAKE UP?",
            font=(
                "Segoe UI",
                20
            ),
            fill="GREEN",
            anchor="center"
        )

        self.title2_id = self.canvas2.create_text(
            W / 2,
            110,
            text="ENTER SECONDS",
            font=(
                "Segoe UI",
                38
            ),
            fill="black",
            anchor="center"
        )

        # ----------------------------------------------------
        # ENTER BUTTON
        # ----------------------------------------------------

        self.create_page2_button(
            center_x=560,
            center_y=405,
            width=305,
            height=64,
            color="#5d0808",
            text="enter",
            text_color="white",
            command=self.enter_pressed
        )

        # ----------------------------------------------------
        # SET BUTTON
        # ----------------------------------------------------

        self.create_page2_button(
            center_x=560,
            center_y=478,
            width=150,
            height=58,
            color="#8acbd4",
            text="set",
            text_color="black",
            command=self.set_pressed
        )

        # ----------------------------------------------------
        # FORCE IMPORTANT ELEMENTS TO FRONT
        # ----------------------------------------------------

        self.canvas2.tag_raise(
            self.back_id
        )

        self.canvas2.tag_raise(
            self.title1_id
        )

        self.canvas2.tag_raise(
            self.title2_id
        )

        self.canvas2.tag_raise(
            self.title3_id
        )


    # ========================================================
    # PAGE 2 BUTTON CREATOR
    # ========================================================

    def create_page2_button(
        self,
        center_x,
        center_y,
        width,
        height,
        color,
        text,
        text_color,
        command
    ):

        x0 = int(
            center_x - width / 2
        )

        y0 = int(
            center_y - height / 2
        )

        # ----------------------------------------------------
        # BUTTON IMAGE
        # ----------------------------------------------------

        img = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(img)

        draw.rounded_rectangle(
            (
                0,
                0,
                width - 1,
                height - 1
            ),
            radius=height // 2,
            fill=color
        )

        photo = ImageTk.PhotoImage(
            img
        )

        # Keep PhotoImage alive
        if not hasattr(
            self,
            "page2_button_photos"
        ):

            self.page2_button_photos = []

        self.page2_button_photos.append(
            photo
        )

        # ----------------------------------------------------
        # BUTTON BACKGROUND
        # ----------------------------------------------------

        image_id = self.canvas2.create_image(
            x0,
            y0,
            image=photo,
            anchor="nw"
        )

        # ----------------------------------------------------
        # BUTTON TEXT
        # ----------------------------------------------------

        text_id = self.canvas2.create_text(
            center_x,
            center_y,
            text=text,
            font=(
                "Segoe UI",
                30
            ),
            fill=text_color,
            anchor="center"
        )

        # ----------------------------------------------------
        # BRING BUTTON ABOVE TIME IMAGE
        # ----------------------------------------------------

        self.canvas2.tag_raise(
            image_id
        )

        self.canvas2.tag_raise(
            text_id
        )

        # ----------------------------------------------------
        # HOVER EFFECT
        # ----------------------------------------------------

        def hover_enter(event):

            self.canvas2.itemconfig(
                image_id,
                state="normal"
            )

            # Slight visual feedback
            self.canvas2.itemconfig(
                text_id,
                fill="#ffffff"
                if text_color == "black"
                else text_color
            )

        def hover_leave(event):

            self.canvas2.itemconfig(
                text_id,
                fill=text_color
            )

        self.canvas2.tag_bind(
            image_id,
            "<Enter>",
            hover_enter
        )

        self.canvas2.tag_bind(
            text_id,
            "<Enter>",
            hover_enter
        )

        self.canvas2.tag_bind(
            image_id,
            "<Leave>",
            hover_leave
        )

        self.canvas2.tag_bind(
            text_id,
            "<Leave>",
            hover_leave
        )

        # ----------------------------------------------------
        # CLICK EVENTS
        # ----------------------------------------------------

        self.canvas2.tag_bind(
            image_id,
            "<Button-1>",
            command
        )

        self.canvas2.tag_bind(
            text_id,
            "<Button-1>",
            command
        )


    # ========================================================
    # PAGE 2 ACTIONS
    # ========================================================

    def enter_pressed(self, event=None):

        # ----------------------------------------------------
        # CREATE INPUT BOX OVER THE ENTER BUTTON
        # ----------------------------------------------------

        if hasattr(self, "seconds_entry"):
            self.seconds_entry.destroy()

        self.seconds_entry = tk.Entry(
            self.page2,
            font=(
                "Segoe UI",
                24
            ),
            justify="center",
            bg="white",
            fg="black",
            relief="flat"
        )

        # Same location as ENTER button
        self.seconds_entry.place(
            x=408,
            y=373,
            width=305,
            height=64
        )

        self.seconds_entry.focus_set()

        # Allow ENTER key to confirm input
        self.seconds_entry.bind(
            "<Return>",
            self.confirm_seconds
        )


    def confirm_seconds(self, event=None):

        value = self.seconds_entry.get().strip()

        if not value.isdigit():

            self.seconds_entry.delete(
                0,
                tk.END
            )

            self.seconds_entry.insert(
                0,
                "ENTER NUMBER"
            )

            return

        seconds = int(value)

        if seconds <= 0:

            self.seconds_entry.delete(
                0,
                tk.END
            )

            self.seconds_entry.insert(
                0,
                "1 OR MORE"
            )

            return

        self.alarm_seconds = seconds

        self.seconds_entry.destroy()

        del self.seconds_entry

        # Pressing Enter immediately sets the alarm — no need to click Set
        self.remaining_seconds = self.alarm_seconds
        self.alarm_running = True
        self.countdown()


    def set_pressed(self, event=None):

        # ----------------------------------------------------
        # IF ENTRY STILL EXISTS, READ IT
        # ----------------------------------------------------

        if hasattr(self, "seconds_entry"):

            value = self.seconds_entry.get().strip()

            if value.isdigit():

                seconds = int(value)

                if seconds > 0:
                    self.alarm_seconds = seconds

                    self.seconds_entry.destroy()
                    del self.seconds_entry

            else:

                return

        # ----------------------------------------------------
        # CHECK WHETHER TIME WAS ENTERED
        # ----------------------------------------------------

        if self.alarm_seconds <= 0:

            # If no time entered, activate input
            self.enter_pressed()
            return

        # ----------------------------------------------------
        # START ALARM COUNTDOWN
        # ----------------------------------------------------

        self.remaining_seconds = self.alarm_seconds
        self.alarm_running = True

        self.countdown()


    # ========================================================
    # ALARM COUNTDOWN
    # ========================================================

    def countdown(self):

        if not self.alarm_running:
            return

        if self.remaining_seconds <= 0:

            self.alarm_running = False

            self.alarm_ringing()

            return

        print(
            "Alarm in:",
            self.remaining_seconds,
            "seconds"
        )

        self.remaining_seconds -= 1

        self.alarm_job = self.after(
            1000,
            self.countdown
        )


    # ========================================================
    # PAGE 3
    # ========================================================

    def build_page3(self):

        self.canvas3 = tk.Canvas(
            self.page3,
            width=W,
            height=H,
            highlightthickness=0,
            bd=0,
            bg="#202020"
        )

        self.canvas3.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # RING IMAGE / DYNAMIC BACKGROUND
        # ----------------------------------------------------

        if not os.path.exists(
            RING_IMAGE_PATH
        ):

            raise FileNotFoundError(
                f"Ring image not found:\n"
                f"{RING_IMAGE_PATH}"
            )

        ring_bg = load_cover_image(
            RING_IMAGE_PATH,
            W,
            H
        )

        self.ring_bg_photo = ImageTk.PhotoImage(
            ring_bg
        )

        self.page3_bg_id = self.canvas3.create_image(
            0,
            0,
            image=self.ring_bg_photo,
            anchor="nw"
        )

        # ----------------------------------------------------
        # CLOCK IMAGE
        # ----------------------------------------------------

        if not os.path.exists(
            CLOCK_IMAGE_PATH
        ):

            raise FileNotFoundError(
                f"Clock image not found:\n"
                f"{CLOCK_IMAGE_PATH}"
            )

        clock_img = Image.open(
            CLOCK_IMAGE_PATH
        ).convert("RGBA")

        # Resize clock image
        clock_size = 55

        clock_img.thumbnail(
            (clock_size, clock_size),
            Image.LANCZOS
        )

        self.clock_ring_photo = ImageTk.PhotoImage(
            clock_img
        )

        self.canvas3.create_image(
            120,
            120,
            image=self.clock_ring_photo,
            anchor="center"
        )

        # ----------------------------------------------------
        # ALARM TITLE / MESSAGE CANVAS TEXT
        # ----------------------------------------------------

        self.ring_title_id = self.canvas3.create_text(
            335,
            120,
            text="RISE AND SHINE\nPRINCESS",
            font=(
                "Segoe UI",
                22,
                "bold"
            ),
            fill="black",
            anchor="center",
            justify="center",
            width=380
        )

        # ----------------------------------------------------
        # SNOOZE BUTTON
        # ----------------------------------------------------

        self.snooze_button = tk.Button(
            self.page3,
            text="SNOOZE",
            font=(
                "Segoe UI",
                18
            ),
            bg="#59c878",
            fg="black",
            activebackground="#4db76d",
            activeforeground="black",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.snooze_alarm
        )

        self.snooze_button.place(
            x=163,
            y=180,
            width=130,
            height=45
        )

        # ----------------------------------------------------
        # DISMISS BUTTON
        # ----------------------------------------------------

        self.dismiss_button = tk.Button(
            self.page3,
            text="DISMISS",
            font=(
                "Segoe UI",
                18
            ),
            bg="#59c878",
            fg="black",
            activebackground="#4db76d",
            activeforeground="black",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.dismiss_alarm
        )

        self.dismiss_button.place(
            x=163,
            y=230,
            width=130,
            height=45
        )

        # ----------------------------------------------------
        # HOVER EFFECTS
        # ----------------------------------------------------

        self.add_hover(
            self.snooze_button,
            "#59c878",
            "#75dc91"
        )

        self.add_hover(
            self.dismiss_button,
            "#59c878",
            "#75dc91"
        )


    # ========================================================
    # PAGE 3 HOVER
    # ========================================================

    def add_hover(
        self,
        button,
        normal_color,
        hover_color
    ):

        button.bind(
            "<Enter>",
            lambda event:
            button.config(
                bg=hover_color
            )
        )

        button.bind(
            "<Leave>",
            lambda event:
            button.config(
                bg=normal_color
            )
        )


    # ========================================================
    # DYNAMIC BACKGROUND & BACKEND LOGIC INTEGRATION
    # ========================================================

    def update_ringing_title(self, text, font_size=20):
        if hasattr(self, "ring_title_id"):
            self.canvas3.itemconfig(
                self.ring_title_id,
                text=text,
                font=("Segoe UI", font_size, "bold")
            )

    def update_stage_background(self, stage_name):
        """
        Dynamically updates Page 3 full background image based on stage_name or keywords.
        Automatically picks up any new images added by the user!
        """
        if not hasattr(self, "page3_bg_id"):
            return

        keywords_map = {
            "snoozing": ["snoozing", "snooze"],
            "loser": ["loser"],
            "trumpet": ["trumpet"],
            "we_made_question": ["we made question", "we made"],
            "confidential": ["confidential"],
            "alarm_doesnt_know": ["at this point", "even alarm", "doesnt know"],
            "bloodline": ["bloodline", "disappointed", "report"],
            "ring": ["ring", "alarm", "default"]
        }

        kws = keywords_map.get(stage_name, [stage_name])
        img_path = find_image(kws)

        if not img_path:
            img_path = RING_IMAGE_PATH

        if img_path in self._bg_cache:
            photo = self._bg_cache[img_path]
        else:
            try:
                img = load_cover_image(img_path, W, H)
                photo = ImageTk.PhotoImage(img)
                self._bg_cache[img_path] = photo
            except Exception as e:
                print("Failed to update background image:", e)
                return

        self.canvas3.itemconfig(self.page3_bg_id, image=photo)
        self.canvas3.tag_lower(self.page3_bg_id)

    def alarm_ringing(self):
        self.show_page3()

        # Restore Snooze and Dismiss buttons
        self.snooze_button.place(
            x=163,
            y=180,
            width=130,
            height=45
        )
        self.dismiss_button.place(
            x=163,
            y=230,
            width=130,
            height=45
        )

        if hasattr(self, "awake_button") and self.awake_button:
            self.awake_button.place_forget()

        if self.snooze_count == 0:
            title_text = "⏰ RISE AND SHINE PRINCESS"
            sound_file = "Alarm Beeps.wav"
            self.update_stage_background("ring")
        elif self.snooze_count == 1:
            title_text = "SIKE YOU SNOOZED HEHE"
            sound_file = "Alarm Beeps.wav"
            self.update_stage_background("ring")
        elif self.snooze_count == 2:
            title_text = "Okay I'll dismiss next time"
            sound_file = "Alarm Clock.wav"
            self.update_stage_background("ring")
        elif self.snooze_count == 3:
            title_text = "Next time for sure"
            sound_file = "Alarm Clock.wav"
            self.update_stage_background("ring")
        elif self.snooze_count == 4:
            title_text = "Get Up Plis"
            sound_file = "Trumpets.wav"
            self.update_stage_background("trumpet")
        else:
            title_text = "ACHIEVEMENT UNLOCKED!!\nSUCCESSFULLY DISAPPOINTED\nTHE ENTIRE BLOODLINE"
            sound_file = "Loud alarm.wav"
            self.update_stage_background("bloodline")

        self.update_ringing_title(title_text, font_size=18)

        try:
            sound_path = get_sound_path(sound_file)
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print("Sound playback error:", e)

    # SWAPPED BUTTONS
    # SNOOZE button actually calls actual_dismiss (Math Quiz)
    def snooze_alarm(self):
        self.actual_dismiss()

    # DISMISS button actually calls actual_snooze (Snooze + Re-ring)
    def dismiss_alarm(self):
        self.actual_snooze()

    def actual_snooze(self):
        self.snooze_count += 1
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

        self.update_ringing_title("SNOOZING... HEHE", font_size=22)
        self.update_stage_background("snoozing")
        self.after(2000, self.alarm_ringing)

    def actual_dismiss(self):
        self.open_math_modal()

    def open_math_modal(self):
        math_page = tk.Toplevel(self)
        math_page.title("PROVE IT")
        math_page.geometry("500x380")
        math_page.configure(bg="#111111")
        math_page.grab_set()

        if self.snooze_count == 0:
            question_text = "What is 7 + 4?"
            options = ["9", "10", "11", "12"]
            answer = "11"
        elif self.snooze_count == 1:
            question_text = "How many pigeons are needed to carry a refrigerator?"
            options = ["3", "17", "42", "Obviously 900"]
            answer = "42"
        elif self.snooze_count == 2:
            question_text = "What is the emotional temperature of a confused spoon?"
            options = ["37°C", "Tuesday", "42°C", "Cold"]
            answer = "42°C"
        elif self.snooze_count == 3:
            question_text = "How many bananas fit inside the concept of Tuesday?"
            options = ["7", "∞", "Tuesday bananas", "None"]
            answer = "∞"
        elif self.snooze_count == 4:
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
            font=("Arial", 15, "bold"),
            bg="#111111",
            fg="white",
            wraplength=450,
            justify="center"
        )
        question.pack(pady=20)

        selected_answer = tk.StringVar(value="")
        option_circles = {}

        def select_option(val):
            selected_answer.set(val)
            for c in option_circles.values():
                c.config(text="○")
            option_circles[val].config(text="●")

        for option in options:
            option_frame = tk.Frame(math_page, bg="#111111")
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

            for w in (circle, option_label, option_frame):
                w.bind("<Button-1>", lambda event, v=option: select_option(v))

        def check_answer():
            user_ans = selected_answer.get()

            if user_ans == answer:
                math_page.destroy()
                try:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    pass

                self.update_ringing_title("CORRECT.\n\nWe have absolutely no idea why.", font_size=18)
                self.update_stage_background("ring")
                self.after(2000, self.show_sleep_report)

            else:
                math_page.destroy()
                self.snooze_count += 1
                try:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    pass

                self.snooze_button.place_forget()
                self.dismiss_button.place_forget()

                if self.snooze_count == 1:
                    message = "INCORRECT.\n\nLOL LOSER"
                    self.update_stage_background("loser")
                elif self.snooze_count == 2:
                    message = "INCORRECT.\n\nWe made the question.\nWe still don't know."
                    self.update_stage_background("we_made_question")
                elif self.snooze_count == 3:
                    message = "INCORRECT.\n\nThe answer has been\nclassified as confidential."
                    self.update_stage_background("confidential")
                else:
                    message = "INCORRECT.\n\nAt this point, nobody knows.\nIncluding the alarm."
                    self.update_stage_background("alarm_doesnt_know")

                self.update_ringing_title(message, font_size=18)
                self.after(3000, self.alarm_ringing)

        submit_button = tk.Button(
            math_page,
            text="SUBMIT",
            font=("Arial", 14, "bold"),
            command=check_answer
        )
        submit_button.pack(pady=15)

    def show_sleep_report(self):
        self.snooze_button.place_forget()
        self.dismiss_button.place_forget()

        bloodline = min(100, self.snooze_count * 17 + 5)
        productivity = max(0, 100 - self.snooze_count * 13)

        filled = productivity // 5
        empty = 20 - filled
        bar = "█" * filled + "░" * empty

        report_msg = (
            f"📊 YOUR SLEEP REPORT\n\n"
            f"Snoozes: {self.snooze_count}   Math Problems: {self.snooze_count + 1}\n"
            f"Wrong Answers: {self.snooze_count}\n"
            f"Brain Cells Used: {max(1, 10 - self.snooze_count)}\n"
            f"Bloodline Disappointment: {bloodline}%\n\n"
            f"PRODUCTIVITY\n"
            f"[{bar}] {productivity}%\n\n"
            f"Scientific Significance: NONE"
        )

        self.update_ringing_title(report_msg, font_size=13)
        self.update_stage_background("bloodline")

        if not hasattr(self, "awake_button") or not self.awake_button:
            self.awake_button = tk.Button(
                self.page3,
                text="I'M AWAKE",
                font=("Segoe UI", 14, "bold"),
                bg="#59c878",
                fg="black",
                activebackground="#4db76d",
                activeforeground="black",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=self.finish_alarm
            )
            self.add_hover(self.awake_button, "#59c878", "#75dc91")

        self.awake_button.place(x=163, y=290, width=130, height=45)

    def finish_alarm(self):
        self.snooze_count = 0
        self.stop_alarm()
        self.update_stage_background("ring")
        if hasattr(self, "awake_button") and self.awake_button:
            self.awake_button.place_forget()
        self.show_page1()

    def stop_alarm(self):
        self.alarm_running = False
        if self.alarm_job is not None:
            try:
                self.after_cancel(self.alarm_job)
            except Exception:
                pass
            self.alarm_job = None

        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

        self.remaining_seconds = 0
        self.alarm_seconds = 0

    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    def show_page1(self):

        self.page1.lift()


    def show_page2(self):

        self.page2.lift()


    def show_page3(self):

        self.page3.lift()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = AlarmPanel()

    app.mainloop()